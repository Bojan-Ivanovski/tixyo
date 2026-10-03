"""Shared descriptor definitions used across projects.

The registry is deliberately independent of GitHub. A project can use the
canonical label names directly or map them to another issue tracker.
"""

from typing import Any

TICKET_DESCRIPTORS: dict[str, Any] = {
    "type": {
        "description": "The primary nature of the work.",
        "color": "#0052cc",
        "labels": {
            "Type: Bug": "Something existing behaves incorrectly or fails.",
            "Type: Feature": "A request for new user-visible functionality.",
            "Type: Enhancement": "An improvement to existing functionality.",
            "Type: Documentation": "Documentation-only work.",
            "Type: Question": "A request for help or clarification.",
            "Type: Maintenance": "Refactoring, dependencies, CI, tooling, or cleanup.",
            "Type: Other": "Work that does not fit another issue type.",
            "Type: Epic": "A large body of work that should be decomposed into multiple related issues.",
        },
    },
    "component": {
        "description": "The repository areas most directly involved.",
        "color": "#fbca04",
        "labels": {
            "Component: User Documentation": "User-facing guides, tutorials, and usage documentation.",
            "Component: Dev Documentation": "Developer-facing documentation, reference material, and contribution guides.",
            "Component: Unit Tests": "Unit tests and their supporting test utilities.",
            "Component: Source Code": "Application or library source code and implementation behavior.",
            "Component: Build": "Build configuration, packaging, dependencies, and release tooling.",
        },
    },
    "priority": {
        "description": "Impact and urgency of the work.",
        "labels": {
            "Priority: P0": "Emergency: severe production, data, or security impact.",
            "Priority: P1": "High impact: a major workflow is broken.",
            "Priority: P2": "Normal importance: useful or important, with limited impact or a workaround.",
            "Priority: P3": "Low urgency: polish, cleanup, or a non-urgent request.",
        },
    },
    "status": {
        "description": "The current delivery state of the issue.",
        "labels": {
            "Status: Backlog": "Accepted work that has not started yet.",
            "Status: Ready": "Actionable and sufficiently clear for engineering.",
            "Status: In Progress": "Work is actively being implemented.",
            "Status: In Review": "The implementation is awaiting review or approval.",
            "Status: Done": "The work is complete and requires no further action.",
        },
    },
    "size": {
        "description": "The relative effort, scope, and allowed work-item hierarchy.",
        "labels": {
            "Size: S": "Small, well-understood leaf change with limited scope and no sub-issues.",
            "Size: M": "Moderate leaf change involving several related edits, with no sub-issues.",
            "Size: L": "Large work item that may contain one layer of M or S sub-issues.",
            "Size: XL": "A complete tree of work containing multiple L or XL work items, with L branches decomposed into M or S sub-issues.",
        },
        "hierarchy": {
            "Size: XL": {
                "can_contain": ["Size: L", "Size: XL", "Size: M", "Size: S"],
                "description": "Top-level work tree containing multiple large work items.",
            },
            "Size: L": {
                "can_contain": ["Size: M", "Size: S"],
                "max_sub_issue_depth": 1,
                "description": "Large work item with at most one layer of sub-issues.",
            },
            "Size: M": {
                "can_contain": [],
                "max_sub_issue_depth": 0,
                "description": "Leaf work item with no sub-issues.",
            },
            "Size: S": {
                "can_contain": [],
                "max_sub_issue_depth": 0,
                "description": "Leaf work item with no sub-issues.",
            },
        },
    },
    "signal": {
        "description": "Additional routing signals produced during triage.",
        "labels": {
            "security-sensitive": "The issue may involve a security vulnerability or exposure.",
            "privacy-sensitive": "The issue involves personal, confidential, or otherwise sensitive data.",
            "compliance": "The issue relates to legal, regulatory, contractual, or policy requirements.",
        },
    },
}
