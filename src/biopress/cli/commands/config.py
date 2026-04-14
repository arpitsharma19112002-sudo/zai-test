"""Config command - Manage BioPress configuration."""

import typer

from biopress.core.config import get_config_manager
from biopress.core.cost_manager import get_cost_manager

command = typer.Typer(
    name="config",
    help="Manage BioPress configuration",
)

VALID_KEYS = ["provider", "output_dir", "language", "budget", "budget_reset", "memory", "memory_limit"]
VALID_PROVIDERS = ["ollama", "grok", "claude", "openai"]
VALID_LANGUAGES = ["english", "hindi"]
VALID_BUDGET_RESETS = ["true", "false"]
VALID_MEMORY = ["enabled", "disabled"]


@command.command("set")
def config_set(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a configuration value."""
    if key not in VALID_KEYS:
        typer.echo(
            f"Error: Invalid key '{key}'. Valid keys: {', '.join(VALID_KEYS)}",
            err=True,
        )
        raise typer.Exit(1)

    if key == "provider" and value not in VALID_PROVIDERS:
        typer.echo(
            f"Error: Invalid provider '{value}'. Valid providers: {', '.join(VALID_PROVIDERS)}",
            err=True,
        )
        raise typer.Exit(1)

    if key == "language" and value not in VALID_LANGUAGES:
        typer.echo(
            f"Error: Invalid language '{value}'. Valid languages: {', '.join(VALID_LANGUAGES)}",
            err=True,
        )
        raise typer.Exit(1)

    if key == "budget":
        try:
            float(value)
        except ValueError:
            typer.echo(
                f"Error: Invalid budget '{value}'. Must be a number.",
                err=True,
            )
            raise typer.Exit(1)

    if key == "budget_reset" and value not in VALID_BUDGET_RESETS:
        typer.echo(
            f"Error: Invalid budget_reset '{value}'. Valid values: {', '.join(VALID_BUDGET_RESETS)}",
            err=True,
        )
        raise typer.Exit(1)

    if key == "memory" and value not in VALID_MEMORY:
        typer.echo(
            f"Error: Invalid memory '{value}'. Valid values: {', '.join(VALID_MEMORY)}",
            err=True,
        )
        raise typer.Exit(1)

    if key == "memory_limit":
        try:
            limit = int(value)
            if limit < 1:
                raise ValueError()
        except ValueError:
            typer.echo(
                f"Error: Invalid memory_limit '{value}'. Must be a positive integer.",
                err=True,
            )
            raise typer.Exit(1)

    config_manager = get_config_manager()
    config_manager.set(key, value)
    typer.echo(f"Set {key} = {value}")


@command.command("get")
def config_get(
    key: str = typer.Argument(..., help="Configuration key"),
) -> None:
    """Get a configuration value."""
    if key not in VALID_KEYS:
        typer.echo(
            f"Error: Invalid key '{key}'. Valid keys: {', '.join(VALID_KEYS)}",
            err=True,
        )
        raise typer.Exit(1)

    config_manager = get_config_manager()
    value = config_manager.get(key)
    if value is None:
        typer.echo(f"Error: Key '{key}' not set", err=True)
        raise typer.Exit(1)
    typer.echo(value)


@command.command("list")
def config_list() -> None:
    """List all configuration values."""
    config_manager = get_config_manager()
    config = config_manager.list()

    if not config:
        typer.echo("No configuration found.")
        return

    for key, value in config.items():
        typer.echo(f"{key} = {value}")


@command.command("report")
def config_report() -> None:
    """Show cost usage report."""
    cost_manager = get_cost_manager()
    report = cost_manager.get_report()

    typer.echo("=== Cost Report ===")
    typer.echo(f"Total Cost: ${report.total_cost:.4f}")
    typer.echo(f"Total Requests: {report.requests}")
    typer.echo(f"Tokens In: {report.total_tokens_in}")
    typer.echo(f"Tokens Out: {report.total_tokens_out}")
    typer.echo("By Provider:")
    for provider, cost in report.by_provider.items():
        typer.echo(f"  {provider}: ${cost:.4f}")

    budget = cost_manager.get_budget()
    if budget:
        remaining = budget - report.total_cost
        pct = (report.total_cost / budget) * 100 if budget > 0 else 0
        typer.echo(f"\nBudget: ${budget:.2f}")
        typer.echo(f"Remaining: ${remaining:.2f} ({pct:.1f}% used)")
