"""Export command - Export content to PDF."""

import typer
from pathlib import Path

from biopress.pdf.builder import PDFBuilder

command = typer.Typer(
    name="export",
    help="Export content to PDF",
)


@command.command()
def export(
    input: Path = typer.Option(..., "-i", "--input", help="Input JSON file with questions"),
    output: Path = typer.Option(..., "-o", "--output", help="Output PDF file"),
    style: str = typer.Option(
        "default",
        "-s",
        "--style",
        help="PDF style (default, neet-2column, ncert, bilingual, omr-ready)",
    ),
    title: str = typer.Option("BioPress Quiz", "-t", "--title", help="PDF title"),
    subject: str = typer.Option("", help="Subject name"),
    exam_type: str = typer.Option("", help="Exam type (NEET, JEE, CBSE)"),
    include_review: bool = typer.Option(
        False,
        "--include-review",
        help="Include editorial review section",
    ),
) -> None:
    """Export generated questions to PDF."""
    if not input.exists():
        typer.echo(f"Error: Input file '{input}' not found", err=True)
        raise typer.Exit(1)
    
    style_map = {
        "neet-2column": "neet-2column",
        "neet": "neet-2column",
        "ncert": "ncert",
        "bilingual": "bilingual",
        "omr-ready": "omr-ready",
        "omr": "omr-ready",
    }
    resolved_style = style_map.get(style.lower(), style)
    
    try:
        PDFBuilder.build(
            input_path=str(input),
            output_path=str(output),
            style=resolved_style,
            title=title if title != "BioPress Quiz" else None,
            subject=subject or None,
            exam_type=exam_type or None,
            include_review=include_review,
        )
        typer.echo(f"PDF exported successfully to: {output}")
    except Exception as e:
        typer.echo(f"Error exporting PDF: {e}", err=True)
        raise typer.Exit(1)


@command.command("create-style")
def create_style(
    description: str = typer.Argument(..., help="Natural language description of the style"),
    name: str = typer.Option("", "-n", "--name", help="Name for the style"),
    output: Path = typer.Option(None, "-o", "--output", help="Output file path"),
) -> None:
    """Create a PDF style from natural language description."""
    from biopress.pdf.style_system import StyleSystem, save_style_layout
    
    try:
        system = StyleSystem()
        layout = system.create_style(description, name or None)
        
        if output:
            filepath = save_style_layout(layout, f"{output.name}")
        else:
            filepath = system.save_layout(layout)
        
        typer.echo(f"Style layout created: {filepath}")
        typer.echo(f"Description: {layout.description}")
        typer.echo(f"Columns: {layout.columns}, Font: {layout.font_family}")
    except Exception as e:
        typer.echo(f"Error creating style: {e}", err=True)
        raise typer.Exit(1)