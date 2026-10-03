"""Shared CLI dependencies."""

import os

import typer

from ..clients.client import Client
from ..clients.github import GithubClient


def build_client(token: str | None, repo: str | None) -> Client:
    resolved_token = token or os.getenv("GITHUB_TOKEN")
    resolved_repo = repo or os.getenv("GITHUB_REPOSITORY")
    if not resolved_token or not resolved_repo:
        raise typer.BadParameter(
            "Provide --token and --repo, or set GITHUB_TOKEN and GITHUB_REPOSITORY."
        )
    return GithubClient(resolved_token, resolved_repo)
