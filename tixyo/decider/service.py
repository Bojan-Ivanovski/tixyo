"""Provider-neutral confidence-gated ticket triage."""

import os
from typing import Any

from ..clients.client import Client
from .context import build_ticket_context
from .model import DeciderModel
from .models import Decision, TriageResult

DEFAULT_MODEL = os.getenv("DECIDER_MODEL", "Mapika/decider-2b")
DEFAULT_THRESHOLD = 0.90
SECURITY_THRESHOLD = 0.95


class TriageService:
    def __init__(
        self,
        client: Client,
        model_name: str = DEFAULT_MODEL,
        model: DeciderModel | None = None,
    ):
        self.client = client
        self.model = model or DeciderModel(model_name)

    def triage(self, number: int, *, apply: bool = False) -> TriageResult:
        ticket = self.client.tickets.get(number, comments=True)
        descriptors = self._descriptors()
        candidate_assignees = [
            str(user["login"])
            for user in self.client.assignees()[:25]
            if user.get("login")
        ]
        answers = self.model.run(
            build_ticket_context(ticket),
            descriptors,
            candidate_assignees,
        )
        decisions = [self._parse(field, answer) for field, answer in answers.items()]
        by_field = {decision.field: decision for decision in decisions}
        previous = [label["name"] for label in ticket.get("labels", [])]
        proposed = previous.copy()
        warnings: list[str] = []

        security = by_field.get("security_sensitive")
        if security and security.value is True and security.auto_apply:
            warnings.append("Security-sensitive ticket detected; automatic changes were suppressed.")
        else:
            for field, descriptor in descriptors.items():
                decision = by_field.get(field)
                if not decision or not decision.auto_apply:
                    continue
                known = descriptor.get("labels", {})
                selected = decision.value if isinstance(decision.value, list) else [decision.value]
                if not all(isinstance(value, str) and value in known for value in selected):
                    warnings.append(f"Unknown {field} descriptor: {decision.value}")
                    continue
                prefixes = self._prefixes(known)
                proposed = [
                    label
                    for label in proposed
                    if not any(label.lower().startswith(prefix) for prefix in prefixes)
                ]
                for value in selected:
                    if value not in proposed:
                        proposed.append(value)

        assignee = by_field.get("assignee")
        proposed_assignees = [
            user.get("login") for user in ticket.get("assignees", []) if user.get("login")
        ]
        if (
            assignee
            and assignee.auto_apply
            and isinstance(assignee.value, str)
            and assignee.value != "unassigned"
        ):
            proposed_assignees = [assignee.value]

        changed = proposed != previous
        assignees_changed = proposed_assignees != [
            user.get("login") for user in ticket.get("assignees", []) if user.get("login")
        ]
        if apply and (changed or assignees_changed) and not warnings:
            self.client.tickets.update(
                number,
                labels=proposed if changed else None,
                assignees=proposed_assignees if assignees_changed else None,
            )

        return TriageResult(
            ticket_number=number,
            ticket_title=str(ticket["title"]),
            decisions=decisions,
            previous_labels=previous,
            proposed_labels=proposed,
            applied=apply and (changed or assignees_changed) and not warnings,
            warnings=warnings,
        )

    def _descriptors(self) -> dict[str, dict[str, Any]]:
        return {
            "type": self.client.descriptors.get_types(),
            "component": self.client.descriptors.get_components(),
            "priority": self.client.descriptors.get_priority(),
            "status": self.client.descriptors.get_status(),
            "size": self.client.descriptors.get_size(),
        }

    @staticmethod
    def _parse(field: str, answer: dict[str, Any]) -> Decision:
        if answer.get("type") == "multi_choice":
            value = list(answer.get("choices") or [])
            probabilities = {
                str(name): float(probability)
                for name, probability in (answer.get("probabilities") or {}).items()
            }
            selected_probabilities = [probabilities[name] for name in value]
            probability = min(selected_probabilities, default=0.0)
            return Decision(
                field,
                value,
                probability,
                probabilities,
                bool(value) and probability >= DEFAULT_THRESHOLD,
            )
        if answer.get("type") == "noul" or "noul" in answer:
            yes = float(answer["noul"])
            value: Any = yes >= 0.5
            probabilities = {"yes": yes, "no": 1.0 - yes}
        else:
            value = answer.get("choice")
            probabilities = {
                str(name): float(probability)
                for name, probability in (answer.get("probabilities") or {}).items()
            }
        probability = float(answer.get("x_p_max")) if answer.get("x_p_max") is not None else max(probabilities.values(), default=0.0)
        threshold = SECURITY_THRESHOLD if field == "security_sensitive" else DEFAULT_THRESHOLD
        return Decision(field, value, probability, probabilities, probability >= threshold)

    @staticmethod
    def _prefixes(labels: dict[str, Any]) -> tuple[str, ...]:
        return tuple({f"{name.split(':', 1)[0].lower()}:" for name in labels if ":" in name})
