"""CLI interface for brick project."""
import typer

from brick.cmd import config, version

app = typer.Typer()
app.add_typer(version.app, name="version")
app.add_typer(config.app, name="config")


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m brick` and `$ brick `.
    """
    app()
