"""GitHub ticket operations."""

from typing import Any

from ..tickets import Tickets
from .transport import GithubTransport


class GithubIssues(Tickets):
    """Read and write GitHub issues."""

    def __init__(self, transport: GithubTransport):
        self.transport = transport

    def get(self, number: int, *, comments: bool = True) -> dict[str, Any]:
        ticket = self.transport.get(f"/issues/{number}")
        if comments:
            ticket["comments"] = self.comments(number)
        return ticket

    def create(
        self,
        title: str,
        *,
        body: str | None = None,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"title": title}
        if body is not None:
            payload["body"] = body
        if labels is not None:
            payload["labels"] = labels
        if assignees is not None:
            payload["assignees"] = assignees
        return self.transport.post("/issues", payload=payload)

    def comments(self, number: int, *, limit: int = 20) -> list[dict[str, Any]]:
        return self.transport.get(
            f"/issues/{number}/comments",
            params={"per_page": min(limit, 100)},
        )

    def add_comment(self, number: int, body: str) -> dict[str, Any]:
        return self.transport.post(f"/issues/{number}/comments", payload={"body": body})

    def update(
        self,
        number: int,
        *,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if labels is not None:
            payload["labels"] = labels
        if assignees is not None:
            payload["assignees"] = assignees
        if not payload:
            return {}
        return self.transport.patch(f"/issues/{number}", payload=payload)


__all__ = ["GithubIssues"]
