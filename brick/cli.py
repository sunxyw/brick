"""CLI interface for brick project."""
import typer

from brick.cmd import version

app = typer.Typer()
app.add_typer(version.app, name="version")


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m brick` and `$ brick `.
    """
    app()
