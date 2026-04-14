"""Generate command - Create questions for exams."""

import json
import time
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from biopress.generators.questions.mcq import MCQGenerator
from biopress.generators.questions.numerical import NumericalGenerator
from biopress.generators.questions.case_based import CaseBasedGenerator
from biopress.generators.questions.assertion_reason import AssertionReasonGenerator
from biopress.generators.mimic import MimicGenerator
from biopress.generators.translator import Translator
from biopress.core.config import get_config_manager
from biopress.core.token_tracker import TokenTracker
from biopress.core.constants import (
    VALID_EXAMS,
    VALID_SUBJECTS,
    VALID_TYPES,
    VALID_LANGUAGES,
    VALID_MODES,
)

command = typer.Typer(
    name="generate",
    help="Generate questions for NEET/JEE exams",
)

STEPS = [
    "Loading templates",
    "Generating questions",
    "Validating",
    "Building output",
]


def display_step_status(console: Console, current_step: int) -> None:
    """Display the step status table."""
    table = Table(show_header=False, box=None)
    table.add_column(style="dim", width=30)
    table.add_column()

    for i, step in enumerate(STEPS):
        status = ""
        if i < current_step:
            status = "[green]✓[/green]"
        elif i == current_step:
            status = "[cyan]In progress...[/cyan]"
        else:
            status = "[dim]Waiting...[/dim]"
        table.add_row(f"Step {i+1}/4: {step}", status)

    console.print(table)


def get_generator(qtype: str):
    """Get the appropriate generator for the question type."""
    generators = {
        "mcq": MCQGenerator,
        "numerical": NumericalGenerator,
        "case-based": CaseBasedGenerator,
        "assertion-reason": AssertionReasonGenerator,
    }
    return generators.get(qtype, MCQGenerator)()


def _resolve_language(language: Optional[str]) -> str:
    """Resolve language from option or config."""
    if language:
        return language
    config_mgr = get_config_manager()
    saved_language = config_mgr.get("language")
    if saved_language:
        return saved_language
    return "english"


def _generate_questions(
    exam: str,
    subject: str,
    type: str,
    count: int,
    topic: str,
    language: str,
    console: Console,
):
    """Common question generation logic."""
    TokenTracker.start_tracking()
    
    translator = Translator(language)
    generator = get_generator(type)
    quiz = generator.generate(exam=exam, subject=subject, count=count, topic=topic)

    json_output = generator.to_json(quiz)
    if language == "hindi":
        TokenTracker.record_llm_translation(
            input_tokens=len(json_output) // 4,
            output_tokens=len(json_output) // 4,
        )
        quiz_data = json.loads(json_output)
        translated_data = translator.translate_quiz(quiz_data)
        json_output = json.dumps(translated_data, ensure_ascii=False, indent=2)

    if hasattr(quiz, "items"):
        valid_count = len(quiz.items)
    else:
        valid_count = 0

    return json_output, valid_count


def _execute_generation(
    exam: str,
    subject: str,
    type: str,
    count: int,
    topic: str,
    language: Optional[str],
    output: Optional[Path],
    mode: str,
) -> None:
    """Core execution logic for generating questions."""
    if mode not in VALID_MODES:
        typer.echo(
            f"Error: Invalid mode '{mode}'. Valid options: {', '.join(VALID_MODES)}",
            err=True,
        )
        raise typer.Exit(1)

    if mode == "mimic":
        mimic = MimicGenerator()
        questions = mimic.generate(
            exam=exam,
            subject=subject,
            count=count,
        )
        json_output = mimic.to_json(questions)
        valid_count = len(questions)

        if output:
            output.write_text(json_output)
            typer.echo(f"Generated {valid_count} questions in mimic mode written to {output}")
        else:
            typer.echo(json_output)
        return

    if language and language not in VALID_LANGUAGES:
        typer.echo(
            f"Error: Invalid language '{language}'. Valid options: {', '.join(VALID_LANGUAGES)}",
            err=True,
        )
        raise typer.Exit(1)

    resolved_language = _resolve_language(language)

    if exam not in VALID_EXAMS:
        typer.echo(
            f"Error: Invalid exam '{exam}'. Valid options: {', '.join(VALID_EXAMS)}",
            err=True,
        )
        raise typer.Exit(1)

    if subject not in VALID_SUBJECTS:
        typer.echo(
            f"Error: Invalid subject '{subject}'. Valid options: {', '.join(VALID_SUBJECTS)}",
            err=True,
        )
        raise typer.Exit(1)

    if type not in VALID_TYPES:
        typer.echo(
            f"Error: Invalid type '{type}'. Valid options: {', '.join(VALID_TYPES)}",
            err=True,
        )
        raise typer.Exit(1)

    if count < 1 or count > 50:
        typer.echo("Error: Count must be between 1 and 50", err=True)
        raise typer.Exit(1)

    console = Console()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        main_task = progress.add_task("Generating questions...", total=100)
        current_step = 0

        try:
            # Step 1: Initialization
            progress.update(main_task, description=f"Step 1/4: {STEPS[0]}...", completed=5)
            display_step_status(console, current_step)
            current_step = 1

            # Step 2: Generation (The heavy lifter)
            progress.update(main_task, description=f"Step 2/4: {STEPS[1]}...", completed=15)
            display_step_status(console, current_step)
            
            json_output, valid_count = _generate_questions(
                exam, subject, type, count, topic, resolved_language, console
            )
            
            progress.update(main_task, completed=75)
            current_step = 2

            # Step 3: Validation
            progress.update(main_task, description=f"Step 3/4: {STEPS[2]}...", completed=85)
            display_step_status(console, current_step)
            current_step = 3

            # Step 4: Finalizing
            progress.update(main_task, description=f"Step 4/4: {STEPS[3]}...", completed=95)
            display_step_status(console, current_step)
            
            progress.update(main_task, completed=100)
            current_step = 4
            display_step_status(console, current_step)

            report = TokenTracker.finalize(valid_count)
            
            if output:
                output.write_text(json_output)
                typer.echo(f"Generated {valid_count} questions written to {output}")
            else:
                typer.echo(json_output)
            
            console.print()
            console.print(report.format_report())

        except Exception as e:
            typer.echo(f"Error generating questions: {e}", err=True)
            raise typer.Exit(1)


@command.command()
def generate_main(
    exam: str = typer.Option("NEET", "--exam", "-e", help="Exam type (NEET, JEE, CBSE)"),
    subject: str = typer.Option("Physics", "--subject", "-s", help="Subject (Physics, Chemistry, Biology)"),
    type: str = typer.Option("mcq", "--type", "-t", help="Question type (mcq, numerical, case-based, assertion-reason)"),
    count: int = typer.Option(10, "--count", "-c", help="Number of questions to generate"),
    topic: str = typer.Option("default", "--topic", help="Topic to generate questions for"),
    language: str = typer.Option(None, "--language", "-l", help="Language for content (english, hindi)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path (default: stdout)"),
    mode: str = typer.Option("standard", "--mode", "-m", help="Generation mode (standard, mimic)"),
) -> None:
    """Generate questions for NEET/JEE exams."""
    _execute_generation(exam, subject, type, count, topic, language, output, mode)


@command.callback(invoke_without_command=True)
def generate_default(
    ctx: typer.Context,
    exam: str = typer.Option("NEET", "--exam", "-e", help="Exam type"),
    subject: str = typer.Option("Physics", "--subject", "-s", help="Subject"),
    type: str = typer.Option("mcq", "--type", "-t", help="Question type"),
    count: int = typer.Option(10, "--count", "-c", help="Number of questions"),
    topic: str = typer.Option("default", "--topic", help="Topic"),
    language: str = typer.Option(None, "--language", "-l", help="Language"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    mode: str = typer.Option("standard", "--mode", "-m", help="Generation mode"),
) -> None:
    """Generate questions for NEET/JEE exams."""
    if ctx.invoked_subcommand:
        return
    _execute_generation(exam, subject, type, count, topic, language, output, mode)
