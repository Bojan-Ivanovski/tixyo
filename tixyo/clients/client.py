"""Common client composition."""

from abc import ABC
from typing import Any

from .tickets import Tickets
from .transport import Transport
from .descriptors import Descriptors

class Client(ABC):
    """Common client holding ticket operations and transport."""

    def __init__(
        self,
        tickets: Tickets,
        transport: Transport,
        descriptors: Descriptors,
    ):
        self.tickets = tickets
        self.transport = transport
        self.descriptors = descriptors

    def assignees(self) -> list[dict[str, Any]]:
        """Return assignable users when the provider supports ownership."""
        return []
