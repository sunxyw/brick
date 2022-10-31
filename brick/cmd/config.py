import typer
from rich import print

from config import settings, write_config

app = typer.Typer()


@app.command(name="set")
def set_config(key: str, value: str):
    """Set configuration."""
    write_config(key, value)
    print(f"[bold green]Set {key} to {value}[/bold green]")


@app.command(name="get")
def get_config(key: str):
    """Get configuration."""
    value = settings.get(key)
    print(f"[bold green]{key} = {value}[/bold green]")


@app.command(name="list")
def list_config():
    """List all configuration."""
    for key, value in settings.as_dict().items():
        print(f"[bold green]{key} = {value}[/bold green]")
