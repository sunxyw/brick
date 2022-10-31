import typer

from brick.cmd.pseudo.converter import Converter

app = typer.Typer()


@app.command()
def convert(source: str):
    """Convert a python file to a brick file."""
    pseudo_converter = Converter(source, source + ".pseudo")
    lines = pseudo_converter.convert()
    pseudo_converter.write_target(lines)
