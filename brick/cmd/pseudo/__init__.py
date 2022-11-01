import typer

from brick.cmd.pseudo.converter import Converter, get_converter

app = typer.Typer()


@app.command()
def convert(source: str):
    """Convert a python file to a brick file."""
    get_converter()(source, source + ".brick").convert_file()
