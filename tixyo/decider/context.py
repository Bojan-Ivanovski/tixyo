"""Build bounded model context from a generic ticket."""

from typing import Any


def build_ticket_context(ticket: dict[str, Any]) -> dict[str, Any]:
    comments = []
    for comment in ticket.get("comments", [])[-10:]:
        body = str(comment.get("body") or "").strip()
        if body:
            comments.append(
                {
                    "author": comment.get("user", {}).get("login", "unknown"),
                    "body": body[:4000],
                }
            )

    return {
        "ticket": {
            "number": ticket["number"],
            "title": ticket["title"],
            "body": str(ticket.get("body") or "").strip()[:12000],
            "author": ticket.get("user", {}).get("login"),
            "labels": [label["name"] for label in ticket.get("labels", [])],
            "state": ticket.get("state"),
        },
        "recent_comments": comments,
    }
