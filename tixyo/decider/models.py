"""Triage domain models."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Decision:
    field: str
    value: Any
    probability: float
    probabilities: dict[str, float]
    auto_apply: bool


@dataclass(frozen=True)
class TriageResult:
    ticket_number: int
    ticket_title: str
    decisions: list[Decision]
    previous_labels: list[str]
    proposed_labels: list[str]
    applied: bool
    warnings: list[str]
