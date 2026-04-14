"""Validate command - Validate generated content."""

import typer

command = typer.Typer(
    name="validate",
    help="Validate generated content quality",
)


@command.callback(invoke_without_command=True)
def validate_main(ctx: typer.Context) -> None:
    """Validate generated content quality."""
    typer.echo(ctx.get_help())
