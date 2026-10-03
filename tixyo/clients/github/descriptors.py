"""GitHub descriptor operations."""

from copy import deepcopy
from typing import Any
from urllib.parse import quote

from ...data.descriptors import TICKET_DESCRIPTORS
from ..descriptors import Descriptors
from .transport import GithubTransport


class GithubDescriptors(Descriptors):
    """Create, retrieve, update, and delete GitHub label descriptors."""

    PREFIXES = {
        "types": ("type:", "kind:"),
        "components": ("component:", "area:"),
        "priority": ("priority:",),
        "status": ("status:", "triage:"),
        "size": ("size:",),
    }

    def __init__(self, transport: GithubTransport):
        self.transport = transport

    def _get(self, group: str) -> dict[str, Any]:
        labels = self.transport.get("/labels", params={"per_page": 100})
        prefixes = self.PREFIXES[group]
        return {
            "labels": {
                label["name"]: {
                    "description": label.get("description") or "",
                    "color": f"#{label.get('color', '')}",
                }
                for label in labels
                if any(label["name"].lower().startswith(prefix) for prefix in prefixes)
            }
        }

    def get_types(self) -> dict[str, Any]:
        return self._get("types")

    def get_components(self) -> dict[str, Any]:
        return self._get("components")

    def get_priority(self) -> dict[str, Any]:
        return deepcopy(TICKET_DESCRIPTORS["priority"])

    def get_status(self) -> dict[str, Any]:
        return deepcopy(TICKET_DESCRIPTORS["status"])

    def get_size(self) -> dict[str, Any]:
        return deepcopy(TICKET_DESCRIPTORS["size"])

    def _create(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        self._ensure_dynamic(name)
        return self.transport.post(
            "/labels",
            payload={"name": name, "description": description, "color": color.lstrip("#")},
        )

    def _update(
        self,
        name: str,
        *,
        description: str | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        self._ensure_dynamic(name)
        payload: dict[str, Any] = {}
        if description is not None:
            payload["description"] = description
        if color is not None:
            payload["color"] = color.lstrip("#")
        return self.transport.patch(f"/labels/{quote(name, safe='')}", payload=payload)

    def _delete(self, name: str) -> None:
        self._ensure_dynamic(name)
        self.transport.delete(f"/labels/{quote(name, safe='')}")

    def create_types(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        return self._create(name, description, color=color)

    def create_components(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        return self._create(name, description, color=color)

    def create_priority(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        return self._static()

    def create_status(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        return self._static()

    def create_size(self, name: str, description: str, *, color: str) -> dict[str, Any]:
        return self._static()

    def update_types(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]:
        return self._update(name, description=description, color=color)

    def update_components(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]:
        return self._update(name, description=description, color=color)

    def update_priority(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]:
        return self._static()

    def update_status(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]:
        return self._static()

    def update_size(self, name: str, *, description: str | None = None, color: str | None = None) -> dict[str, Any]:
        return self._static()

    def delete_types(self, name: str) -> None:
        self._delete(name)

    def delete_components(self, name: str) -> None:
        self._delete(name)

    def delete_priority(self, name: str) -> None:
        self._static()

    def delete_status(self, name: str) -> None:
        self._static()

    def delete_size(self, name: str) -> None:
        self._static()

    @staticmethod
    def _static():
        raise ValueError("Priority, status, and size descriptors are static")

    @staticmethod
    def _ensure_dynamic(name: str) -> None:
        if not name.lower().startswith(("type:", "kind:", "component:", "area:")):
            raise ValueError(
                "Only type and component descriptors can be created, updated, or deleted"
            )


__all__ = ["GithubDescriptors"]
