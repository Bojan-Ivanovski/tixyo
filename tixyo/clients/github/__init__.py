"""Composable GitHub client for issue triage."""

from typing import Any

from ..client import Client
from .descriptors import GithubDescriptors
from .tickets import GithubIssues
from .transport import GithubTransport

class GithubClient(Client):
    """Facade over focused GitHub API clients."""

    def __init__(
        self,
        token: str,
        repository: str,
        *,
        timeout: float = 30.0,
        descriptors: GithubDescriptors | None = None,
    ):
        transport = GithubTransport(token, repository, timeout=timeout)
        super().__init__(
            GithubIssues(transport),
            transport,
            descriptors or GithubDescriptors(transport),
        )

    def assignees(self) -> list[dict[str, Any]]:
        return self.transport.get("/assignees", params={"per_page": 100})

__all__ = [
    "GithubClient",
    "Client",
    "GithubIssues",
    "GithubDescriptors",
    "GithubTransport",
]
