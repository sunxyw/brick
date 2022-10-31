"""CLI interface for brick project."""
import typer

from brick.cmd import config, pseudo, version

app = typer.Typer()
app.add_typer(version.app, name="version")
app.add_typer(config.app, name="config")
app.add_typer(pseudo.app, name="pseudo")


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m brick` and `$ brick `.
    """
    app()
