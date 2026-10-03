"""Root Typer application."""

import typer

from .descriptors import app as descriptors_app
from .triage import triage

app = typer.Typer(name="tixyo", help="Ticket and issue classification tools")
app.add_typer(descriptors_app, name="descriptors")
app.command("triage")(triage)


def main() -> None:
    app()
