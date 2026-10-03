"""Low-level authenticated GitHub API transport."""

from typing import Any

import requests

from ..errors import ClientConfigurationError, ClientRequestError
from ..transport import Transport


class GithubTransport(Transport):
    """Make authenticated requests against one GitHub repository API."""

    def __init__(self, token: str, repository: str, *, timeout: float = 30.0):
        if not token:
            raise ClientConfigurationError("A GitHub token is required")
        if repository.count("/") != 1 or any(not part for part in repository.split("/")):
            raise ClientConfigurationError("Repository must look like owner/repo")

        self.repository = repository
        self.base_url = f"https://api.github.com/repos/{repository}"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "tixyo",
            }
        )

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def patch(self, path: str, *, payload: dict[str, Any]) -> Any:
        return self._request("PATCH", path, json=payload)

    def post(self, path: str, *, payload: dict[str, Any]) -> Any:
        return self._request("POST", path, json=payload)

    def put(self, path: str, *, payload: dict[str, Any]) -> Any:
        return self._request("PUT", path, json=payload)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            detail = ""
            if exc.response is not None:
                try:
                    detail = f": {exc.response.json().get('message', exc.response.text)}"
                except ValueError:
                    detail = f": {exc.response.text}"
            raise ClientRequestError(f"GitHub request failed: {exc}{detail}") from exc



__all__ = ["GithubTransport"]
