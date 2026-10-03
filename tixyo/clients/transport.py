"""Common transport interface."""

from abc import ABC, abstractmethod
from typing import Any


class Transport(ABC):
    """Interface for authenticated service transports."""

    @abstractmethod
    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def post(self, path: str, *, payload: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def put(self, path: str, *, payload: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def patch(self, path: str, *, payload: dict[str, Any]) -> Any:
        raise NotImplementedError
