"""Main CLI application entry point."""

import typer

from biopress import __version__
from biopress.cli.commands import api, config, export, generate, kb, review, validate

app = typer.Typer(
    name="biopress",
    help="BioPress Designer - Educational content generation tool for NEET/JEE exams",
    add_completion=False,
    invoke_without_command=True,
)

app.add_typer(generate.command, name="generate")
app.add_typer(validate.command, name="validate")
app.add_typer(review.command, name="review")
app.add_typer(export.command, name="export")
app.add_typer(config.command, name="config")
app.add_typer(kb.command, name="kb")
app.add_typer(api.command, name="api")


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
) -> None:
    """BioPress Designer - Generate practice questions and exams."""
    if version:
        typer.echo(f"BioPress Designer version {__version__}")
        raise typer.Exit()


def run() -> None:
    """Run the CLI application."""
    app()


if __name__ == "__main__":
    run()
