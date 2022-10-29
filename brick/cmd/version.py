import typer

app = typer.Typer()


@app.command()
def show():
    """Show version."""
    print("0.1.0")


if __name__ == "__main__":
    app()
