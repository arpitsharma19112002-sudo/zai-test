"""Validate command - Validate generated content quality."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from biopress.validators.l2.validator import create_l2_validator
from biopress.core.config import get_config_manager

command = typer.Typer(
    name="validate",
    help="Validate generated content quality",
)


@command.callback(invoke_without_command=True)
def validate_main(
    ctx: typer.Context,
    path: Path = typer.Argument(..., help="Path to the JSON file to validate"),
    deep: bool = typer.Option(True, "--deep/--shallow", help="Run AI-based deep quality checks"),
    threshold: float = typer.Option(0.7, "--threshold", "-t", help="Minimum passing score (0-1.0)"),
) -> None:
    """Validate generated content quality."""
    if ctx.invoked_subcommand:
        return
        
    console = Console()
    
    if not path.exists():
        console.print(f"[red]Error: File not found: {path}[/red]")
        raise typer.Exit(1)

    try:
        with open(path, "r") as f:
            data = json.load(f)
        
        # Determine questions to validate
        if isinstance(data, dict) and "items" in data:
            questions = data["items"]
        elif isinstance(data, list):
            questions = data
        else:
            console.print("[red]Error: Invalid format. Expected a list of questions or a dict with 'items'[/red]")
            raise typer.Exit(1)

        if not questions:
            console.print("[yellow]Warning: No questions found to validate.[/yellow]")
            return

        console.print(f"Validating {len(questions)} questions (Deep: {deep}, Threshold: {threshold})...")
        
        # Initialize Validator
        validator = create_l2_validator(threshold=threshold, single_pass_mode=not deep)
        
        results = validator.validate_batch(questions)
        
        # Build Results Table
        table = Table(title=f"Validation Report: {path.name}")
        table.add_column("ID", style="cyan")
        table.add_column("Result", justify="center")
        table.add_column("Score", justify="right")
        table.add_column("Issues", style="dim")

        passed_count = 0
        for i, (q, res) in enumerate(zip(questions, results)):
            qid = q.get("id", f"#{i+1}")
            
            is_pass = res.overall_pass
            result_str = "[green]PASS[/green]" if is_pass else "[red]FAIL[/red]"
            if is_pass:
                passed_count += 1
                
            problems = ", ".join(res.relevance.issues + res.difficulty.issues + res.context.issues)
            if not problems and not is_pass:
                problems = "Fails combined score threshold"
            
            table.add_row(
                str(qid),
                result_str,
                f"{res.score:.2f}",
                problems[:50] + "..." if len(problems) > 50 else problems
            )

        console.print(table)
        console.print(f"\n[bold]Summary:[/bold] {passed_count}/{len(questions)} passed.")

        if passed_count < len(questions):
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error during validation: {str(e)}[/red]")
        raise typer.Exit(1)
