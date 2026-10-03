"""Ticket triage CLI command."""

import json
from dataclasses import asdict

import typer

from ..decider.service import DEFAULT_MODEL, TriageService
from .common import build_client


def triage(
    issue_number: int,
    apply: bool = typer.Option(False, "--apply", help="Apply high-confidence changes."),
    model: str = typer.Option(DEFAULT_MODEL, "--model"),
    json_output: bool = typer.Option(False, "--json"),
    token: str | None = typer.Option(None, "--token"),
    repo: str | None = typer.Option(None, "--repo"),
) -> None:
    result = TriageService(build_client(token, repo), model).triage(issue_number, apply=apply)
    if json_output:
        typer.echo(json.dumps(asdict(result), indent=2))
        return

    typer.echo(f"Issue: {result.ticket_title}")
    for decision in result.decisions:
        action = "AUTO" if decision.auto_apply else "REVIEW"
        typer.echo(
            f"{decision.field:20} {str(decision.value):24} "
            f"p={decision.probability:.3f} {action}"
        )
    typer.echo(f"old labels: {result.previous_labels}")
    typer.echo(f"new labels: {result.proposed_labels}")
    for warning in result.warnings:
        typer.echo(f"WARNING: {warning}", err=True)
    typer.echo("Applied changes." if result.applied else "DRY RUN: nothing was changed.")
