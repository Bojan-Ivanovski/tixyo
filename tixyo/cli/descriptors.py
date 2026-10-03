"""Descriptor CLI commands."""

from copy import deepcopy
from typing import Any

import typer

from ..clients.client import Client
from ..data.descriptors import TICKET_DESCRIPTORS
from .common import build_client

app = typer.Typer(name="descriptors", help="Manage shared descriptors")


def static_descriptors() -> dict[str, Any]:
    return {
        "types": deepcopy(TICKET_DESCRIPTORS["type"]),
        "components": deepcopy(TICKET_DESCRIPTORS["component"]),
        "priority": deepcopy(TICKET_DESCRIPTORS["priority"]),
        "status": deepcopy(TICKET_DESCRIPTORS["status"]),
        "size": deepcopy(TICKET_DESCRIPTORS["size"]),
    }


def client_descriptors(client: Client) -> dict[str, Any]:
    return {
        "types": client.descriptors.get_types(),
        "components": client.descriptors.get_components(),
        "priority": client.descriptors.get_priority(),
        "status": client.descriptors.get_status(),
        "size": client.descriptors.get_size(),
    }


@app.command("view")
def view(
    diff: bool = typer.Option(False, "--diff"),
    token: str | None = typer.Option(None, "--token"),
    repo: str | None = typer.Option(None, "--repo"),
) -> None:
    remote = client_descriptors(build_client(token, repo))
    for group, descriptor in remote.items():
        typer.echo(f"\n{group}")
        for name, value in descriptor.get("labels", {}).items():
            if isinstance(value, dict):
                typer.echo(
                    f"  {name}: {value.get('description', '')} ({value.get('color', '')})"
                )
            else:
                typer.echo(f"  {name}: {value}")

    if diff:
        expected = static_descriptors()
        typer.echo("\nDiff")
        for group in expected:
            expected_names = set(expected[group].get("labels", {}))
            remote_names = set(remote[group].get("labels", {}))
            for name in sorted(expected_names - remote_names):
                typer.echo(f"  missing {name}")
            for name in sorted(remote_names - expected_names):
                typer.echo(f"  extra {name}")


@app.command("apply")
def apply(
    force: bool = typer.Option(False, "--force"),
    token: str | None = typer.Option(None, "--token"),
    repo: str | None = typer.Option(None, "--repo"),
) -> None:
    client = build_client(token, repo)
    remote = client_descriptors(client)
    expected = static_descriptors()

    for group in ("types", "components"):
        delete = client.descriptors.delete_types if group == "types" else client.descriptors.delete_components
        create = client.descriptors.create_types if group == "types" else client.descriptors.create_components
        update = client.descriptors.update_types if group == "types" else client.descriptors.update_components
        current: dict[str, Any] = remote[group].get("labels", {})
        if force:
            for name in current:
                delete(name)
            current = {}

        color = str(expected[group].get("color", "#6f42c1"))
        for name, description in expected[group].get("labels", {}).items():
            existing = current.get(name)
            if existing is None:
                create(name, description, color=color)
                typer.echo(f"added {name}")
                continue
            remote_description = existing.get("description", "")
            remote_color = existing.get("color", "")
            if remote_description != description or remote_color.lower() != color.lower():
                update(name, description=description, color=color)
                typer.echo(f"updated {name}")
