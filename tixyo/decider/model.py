"""Adapter for Mapika Decider."""

from typing import Any

from decider.infer import Decider


class DeciderModel:
    def __init__(self, model_name: str):
        self.model = Decider(model_name)

    def run(
        self,
        context: dict[str, Any],
        descriptors: dict[str, dict[str, Any]],
        assignees: list[str] | None = None,
    ) -> dict[str, Any]:
        questions: dict[str, dict[str, Any]] = {}
        for field, descriptor in descriptors.items():
            labels = descriptor.get("labels", {})
            if field == "component":
                for index, (name, value) in enumerate(labels.items()):
                    questions[f"component::{index}"] = {
                        "type": "noul",
                        "instructions": (
                            f"Does this ticket directly involve the component '{name}'? "
                            f"{self._description(value) or ''} Select independently of other components."
                        ),
                    }
                continue
            questions[field] = {
                "type": "choice",
                "instructions": f"Choose the single best {field} descriptor for this ticket.",
                "criteria": {
                    name: self._description(value) for name, value in labels.items()
                },
            }

        questions.update(
            {
                "needs_info": {
                    "type": "noul",
                    "instructions": "Is information needed before this ticket can be understood or acted on?",
                },
                "needs_reproduction": {
                    "type": "noul",
                    "instructions": "Is a reproducible example or procedure still needed?",
                },
                "security_sensitive": {
                    "type": "noul",
                    "instructions": "Could this ticket describe a security vulnerability or exposure?",
                },
                "privacy_sensitive": {
                    "type": "noul",
                    "instructions": "Could this ticket involve personal or confidential data?",
                },
                "compliance": {
                    "type": "noul",
                    "instructions": "Does this ticket involve legal, regulatory, or policy requirements?",
                },
            }
        )
        if assignees:
            questions["assignee"] = {
                "type": "choice",
                "instructions": "Choose the best initial owner, or choose unassigned when evidence is insufficient.",
                "criteria": {**{name: None for name in assignees}, "unassigned": "Do not assign a specific owner."},
            }
        result = self.model.system_one(context, questions)
        answers = result.get("answers", result)
        component_labels = list(descriptors.get("component", {}).get("labels", {}))
        component_probabilities = {
            name: float(answers.pop(f"component::{index}")["noul"])
            for index, name in enumerate(component_labels)
        }
        selected_components = [
            name for name, probability in component_probabilities.items() if probability >= 0.5
        ]
        if not selected_components and component_probabilities:
            selected_components = [max(component_probabilities, key=component_probabilities.get)]
        answers["component"] = {
            "type": "multi_choice",
            "choices": selected_components,
            "probabilities": component_probabilities,
        }
        return answers

    @staticmethod
    def _description(value: Any) -> str | None:
        if isinstance(value, dict):
            return str(value.get("description") or "") or None
        return str(value) or None
