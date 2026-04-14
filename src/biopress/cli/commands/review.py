"""Review command - Review and edit content visually."""

import json
import os
import threading
import time
import webbrowser

import typer
from rich.console import Console
from rich.table import Table

command = typer.Typer(
    name="review",
    help="Review and edit content visually",
)


def open_browser(url: str, delay: float = 1.0) -> None:
    """Open browser after a delay."""
    time.sleep(delay)
    webbrowser.open(url)


def generate_preview_summary(data: dict) -> str:
    """Generate a text summary preview of the questions."""
    console = Console()
    items = data.get("items", [])
    question_count = len(items)

    table = Table(title="Question Preview Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Questions", str(question_count))

    topics = set()
    for item in items:
        if "topic" in item:
            topics.add(item["topic"])
    table.add_row("Topics Covered", ", ".join(topics) if topics else "N/A")

    question_types = {}
    for item in items:
        qtype = item.get("type", "unknown")
        question_types[qtype] = question_types.get(qtype, 0) + 1
    type_summary = ", ".join(f"{k}: {v}" for k, v in question_types.items())
    table.add_row("Question Types", type_summary if type_summary else "N/A")

    valid_count = 0
    for item in items:
        if "question" in item and "options" in item:
            valid_count += 1
    validation_status = "Valid" if valid_count == question_count else f"Partial ({valid_count}/{question_count})"
    table.add_row("Validation Status", validation_status)

    console.print(table)

    console.print("\n[bold]Sample Questions:[/bold]")
    for i, item in enumerate(items[:3], 1):
        q_text = item.get("question", "N/A")[:80]
        console.print(f"  {i}. {q_text}...")

    return f"Preview complete: {question_count} questions, {len(topics)} topics"


@command.command()
def launch(
    load: str = typer.Option(None, "--load", help="Load a JSON file for review"),
    preview: bool = typer.Option(False, "--preview", help="Show text preview summary"),
    port: int = typer.Option(8080, "--port", help="Port for the web interface"),
) -> None:
    """Launch the visual review tool."""
    if preview and load:
        if not os.path.exists(load):
            typer.echo(f"Error: File not found: {load}", err=True)
            raise typer.Exit(1)

        with open(load) as f:
            data = json.load(f)

        summary = generate_preview_summary(data)
        typer.echo(summary)
        return

    if preview and not load:
        typer.echo("Error: --preview requires --load to specify a JSON file", err=True)
        raise typer.Exit(1)

    from biopress.visual.app import get_app_state

    app_state = get_app_state()

    if load and os.path.exists(load):
        with open(load) as f:
            app_state.content = json.load(f)
        app_state.current_file = load
        typer.echo(f"Loaded: {load}")
    elif load:
        typer.echo(f"Error: File not found: {load}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Starting BioPress Review Tool at http://localhost:{port}")
    typer.echo("Press Ctrl+C to stop")

    browser_thread = threading.Thread(target=open_browser, args=(f"http://localhost:{port}",))
    browser_thread.daemon = True
    browser_thread.start()

    from nicegui import ui

    ui.run(port=port, reload=False, show=False)


@command.command()
def run(
    load: str = typer.Option(None, "--load", help="Load a JSON file for review"),
    preview: bool = typer.Option(False, "--preview", help="Show text preview summary"),
    port: int = typer.Option(8080, "--port", help="Port for the web interface"),
) -> None:
    """Run the visual review tool (alias for launch)."""
    ctx = typer.Context(launch)
    ctx.invoke(launch, load=load, preview=preview, port=port)


@command.command()
def preview(
    load: str = typer.Argument(..., help="Load a JSON file for preview"),
) -> None:
    """Show text preview summary of questions."""
    if not os.path.exists(load):
        typer.echo(f"Error: File not found: {load}", err=True)
        raise typer.Exit(1)

    with open(load) as f:
        data = json.load(f)

    summary = generate_preview_summary(data)
    typer.echo(summary)


@command.callback(invoke_without_command=True)
def review_main(
    ctx: typer.Context,
    load: str = typer.Option(None, "--load", help="Load a JSON file"),
    preview: bool = typer.Option(False, "--preview", help="Show text preview summary"),
) -> None:
    """Review and edit content visually."""
    if ctx.invoked_subcommand:
        return

    if preview and load:
        ctx.invoke(launch, load=load, preview=True, port=8080)
    elif preview:
        typer.echo("Error: --preview requires --load to specify a JSON file", err=True)
        raise typer.Exit(1)
    else:
        ctx.invoke(launch, load=load, preview=False, port=8080)
