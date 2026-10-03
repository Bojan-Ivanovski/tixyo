"""Common descriptor interface."""

from abc import ABC, abstractmethod
from typing import Any


class Descriptors(ABC):
    """Interface for descriptor CRUD operations."""

    @abstractmethod
    def get_types(self) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def get_components(self) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def get_priority(self) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def get_status(self) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def get_size(self) -> dict[str, Any]: raise NotImplementedError

    @abstractmethod
    def create_types(self, name: str, description: str, *, color: str) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def create_components(self, name: str, description: str, *, color: str) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def create_priority(self, name: str, description: str, *, color: str) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def create_status(self, name: str, description: str, *, color: str) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def create_size(self, name: str, description: str, *, color: str) -> dict[str, Any]: raise NotImplementedError

    @abstractmethod
    def update_types(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def update_components(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def update_priority(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def update_status(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]: raise NotImplementedError
    @abstractmethod
    def update_size(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]: raise NotImplementedError

    @abstractmethod
    def delete_types(self, name: str) -> None: raise NotImplementedError
    @abstractmethod
    def delete_components(self, name: str) -> None: raise NotImplementedError
    @abstractmethod
    def delete_priority(self, name: str) -> None: raise NotImplementedError
    @abstractmethod
    def delete_status(self, name: str) -> None: raise NotImplementedError
    @abstractmethod
    def delete_size(self, name: str) -> None: raise NotImplementedError
