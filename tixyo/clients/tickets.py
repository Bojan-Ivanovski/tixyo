"""Common ticket operations."""

from abc import ABC, abstractmethod
from typing import Any


class Tickets(ABC):
    """Interface for reading and writing work tickets."""

    @abstractmethod
    def get(
        self,
        number: int,
        *,
        comments: bool = True,
    ) -> dict[str, Any]:
        """Get a ticket, optionally including its comments."""
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        title: str,
        *,
        body: str | None = None,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new ticket."""
        raise NotImplementedError

    @abstractmethod
    def comments(self, number: int, *, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def add_comment(self, number: int, body: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, number: int, *, labels: list[str] | None = None, assignees: list[str] | None = None) -> dict[str, Any]:
        raise NotImplementedError
