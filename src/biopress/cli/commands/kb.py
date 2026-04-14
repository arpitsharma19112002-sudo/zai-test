"""KB command - Manage knowledge base."""

from pathlib import Path
import json

import typer

from biopress.kb.manager import get_kb_manager
from biopress.kb.bootstrapper import KBBootstrapper
from biopress.kb.loader import KBLoader

command = typer.Typer(
    name="kb",
    help="Manage knowledge base",
)


@command.command("load")
def load(
    exam: str = typer.Option(..., "--exam", help="Exam name (e.g., NEET)"),
) -> None:
    """Load knowledge base for an exam."""
    kb_manager = get_kb_manager()
    success = kb_manager.load_exam(exam)

    if success:
        status = kb_manager.get_load_status(exam)
        if status:
            typer.echo(f"Successfully loaded knowledge base for {exam}")
            typer.echo(f"  Subjects: {', '.join(status.get('subjects', []))}")
            typer.echo(f"  Total topics: {status.get('total_topics', 0)}")
            typer.echo(f"  Loaded at: {status.get('loaded_at', 'unknown')}")
        else:
            typer.echo(f"Loaded knowledge base for {exam} but status unavailable")
    else:
        typer.echo(f"Failed to load knowledge base for {exam}", err=True)
        raise typer.Exit(code=1)


@command.command("list")
def list_kb() -> None:
    """List loaded knowledge bases."""
    kb_manager = get_kb_manager()
    loaded = kb_manager.get_loaded_exams()

    if not loaded:
        typer.echo("No knowledge bases loaded")
        return

    typer.echo("Loaded knowledge bases:")
    for exam in loaded:
        status = kb_manager.get_load_status(exam)
        if status:
            typer.echo(f"  - {exam}: {len(status.get('subjects', []))} subjects, {status.get('total_topics', 0)} topics")


@command.command("info")
def info(
    exam: str = typer.Option(None, "--exam", help="Exam name"),
) -> None:
    """Show knowledge base information."""
    kb_manager = get_kb_manager()

    if exam:
        kb_info = kb_manager.get_info(exam)
        if not kb_info:
            typer.echo(f"No knowledge base loaded for {exam}", err=True)
            raise typer.Exit(code=1)

        typer.echo(f"Knowledge Base Information: {exam}")
        typer.echo(f"  Subjects: {', '.join(kb_info['subjects'])}")
        typer.echo(f"  Total topics: {kb_info['total_topics']}")
        typer.echo("  Topics per subject:")
        for subject, count in kb_info["topics_per_subject"].items():
            typer.echo(f"    - {subject}: {count}")
        if kb_info.get("patterns"):
            typer.echo("  Question patterns:")
            for key, value in kb_info["patterns"].items():
                typer.echo(f"    - {key}: {value}")
    else:
        loaded = kb_manager.get_loaded_exams()
        if not loaded:
            typer.echo("No knowledge bases loaded")
            return
        for exam in loaded:
            kb_info = kb_manager.get_info(exam)
            if kb_info:
                typer.echo(f"{exam}: {len(kb_info['subjects'])} subjects, {kb_info['total_topics']} topics")


@command.command("query")
def query(
    exam: str = typer.Option(..., "--exam", help="Exam name"),
    subject: str = typer.Option(None, "--subject", help="Subject name"),
    topic_id: str = typer.Option(None, "--topic-id", help="Topic ID"),
) -> None:
    """Query the knowledge base."""
    kb_manager = get_kb_manager()
    results = kb_manager.query(exam, subject, topic_id)

    if not results:
        typer.echo("No results found")
        return

    typer.echo(f"Found {len(results)} topic(s):")
    for item in results:
        subject_prefix = f"[{item.get('subject', '')}] " if 'subject' in item else ""
        typer.echo(f"  - {subject_prefix}{item['name']} (ID: {item['id']}, Weightage: {item['weightage']}%)")


@command.command("search")
def search(
    exam: str = typer.Option(..., "--exam", help="Exam name"),
    query: str = typer.Argument(..., help="Search query"),
    max_results: int = typer.Option(20, "--max", help="Maximum results"),
) -> None:
    """Search the knowledge base."""
    kb_manager = get_kb_manager()

    if not kb_manager.is_loaded(exam):
        success = kb_manager.load_exam(exam)
        if not success:
            typer.echo(f"Failed to load knowledge base for {exam}", err=True)
            raise typer.Exit(code=1)

    results = kb_manager.search(exam, query, max_results)

    if not results:
        typer.echo(f"No topics found matching '{query}'")
        return

    typer.echo(f"Found {len(results)} matching topic(s):")
    for item in results:
        score_indicator = "*" * min(item.get("score", 0) // 5, 3)
        typer.echo(f"  [{item['subject']}] {item['name']} (ID: {item['id']}, Weightage: {item['weightage']}%) {score_indicator}")


@command.command("bootstrap")
def bootstrap(
    exam: str = typer.Option(..., "--exam", help="Exam name"),
    syllabus: Path = typer.Option(..., "--syllabus", help="Syllabus file path", exists=True),
    subject: str = typer.Option(None, "--subject", help="Subject name"),
    output: Path = typer.Option(None, "--output", help="Output directory"),
) -> None:
    """Bootstrap knowledge base from syllabus document."""
    bootstrapper = KBBootstrapper()

    if subject is None:
        subject = syllabus.stem.replace(exam.lower(), "").strip("_").title()
        if not subject:
            subject = "Physics"

    try:
        kb_syllabus = bootstrapper.bootstrap_from_file(exam, subject, syllabus)
        typer.echo(f"Generated syllabus for {exam} - {subject}")
        typer.echo(f"  Topics: {len(kb_syllabus.topics)}")

        if kb_syllabus.patterns:
            typer.echo(f"  Patterns: {kb_syllabus.patterns}")

        if output:
            saved_path = bootstrapper.save_bootstrap(kb_syllabus, output)
            typer.echo(f"  Saved to: {saved_path}")
        else:
            saved_path = bootstrapper.save_bootstrap(kb_syllabus)
            typer.echo(f"  Saved to: {saved_path}")

    except Exception as e:
        typer.echo(f"Bootstrap failed: {e}", err=True)
        raise typer.Exit(code=1)


@command.command("update")
def update(
    exam: str = typer.Option(..., "--exam", help="Exam name"),
    rules: Path = typer.Option(None, "--rules", help="Rules file (JSON)", exists=True),
    sync_dir: Path = typer.Option(None, "--sync-dir", help="Directory to sync from", exists=True),
    subject: str = typer.Option(None, "--subject", help="Subject to update"),
    topic_id: str = typer.Option(None, "--topic-id", help="Topic ID to update"),
) -> None:
    """Update and sync knowledge base."""
    loader = KBLoader()

    if rules:
        with open(rules, "r") as f:
            rules_data = json.load(f)
        typer.echo(f"Loaded {len(rules_data.get('rules', []))} rules from {rules}")

    if sync_dir:
        results = loader.sync_from_directory(sync_dir)
        typer.echo("Sync results:")
        typer.echo(f"  Added: {len(results['added'])}")
        typer.echo(f"  Updated: {len(results['updated'])}")
        if results["failed"]:
            typer.echo(f"  Failed: {len(results['failed'])}")
            for fail in results["failed"]:
                typer.echo(f"    - {fail}")

    kb_manager = get_kb_manager()
    if not kb_manager.is_loaded(exam):
        kb_manager.load_exam(exam)

    if subject and topic_id:
        typer.echo("Topic update requires interactive mode")
        raise typer.Exit(code=1)

    typer.echo(f"Knowledge base for {exam} is up to date")


@command.callback(invoke_without_command=True)
def kb_main(ctx: typer.Context) -> None:
    """Manage knowledge base."""
    typer.echo(ctx.get_help())