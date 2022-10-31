from pathlib import Path

import requests
import typer
from rich import print

app = typer.Typer()


@app.command()
def show():
    """Show version. Including current version and latest version."""
    current_version = get_current_version()
    latest_version = get_latest_version()
    print("[bold green]Current version:[/bold green] %s" % current_version)
    print("[bold green]Latest  version:[/bold green] %s" % latest_version)


def get_latest_version():
    """Get the latest version from GitHub."""
    url = "https://api.github.com/repos/sunxyw/brick/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    else:
        return "unknown"


def get_current_version():
    """Get the current version from the project."""
    path = Path(__file__).parent.parent / "VERSION"
    with open(path, "r") as f:
        return f.read().strip()


if __name__ == "__main__":
    app()
