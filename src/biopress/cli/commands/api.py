"""API command - Start the BioPress REST API server."""

import typer
import uvicorn

command = typer.Typer(
    name="api",
    help="Start BioPress REST API server",
)


@command.command()
def start(
    host: str = typer.Option(
        "0.0.0.0",
        "--host",
        "-h",
        help="Host to bind the server",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to bind the server",
    ),
    reload: bool = typer.Option(
        False,
        "--reload",
        "-r",
        help="Enable auto-reload for development",
    ),
) -> None:
    """Start the BioPress API server on port 8000."""
    typer.echo(f"Starting BioPress API server on {host}:{port}")
    typer.echo(f"Swagger UI available at http://{host}:{port}/docs")

    uvicorn.run(
        "biopress.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@command.command()
def docs() -> None:
    """Show information about API documentation."""
    typer.echo("BioPress API Documentation")
    typer.echo("=" * 40)
    typer.echo("Swagger UI: http://localhost:8000/docs")
    typer.echo("ReDoc: http://localhost:8000/redoc")
    typer.echo("Health: http://localhost:8000/health")
    typer.echo("")
    typer.echo("Endpoints:")
    typer.echo("  POST /api/v1/generate - Generate questions")
    typer.echo("  POST /api/v1/validate - Validate questions")
    typer.echo("  POST /api/v1/pdf - Generate PDF")