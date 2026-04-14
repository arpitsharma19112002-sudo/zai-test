"""Progress tracking utilities for BioPress."""

from typing import Optional
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TaskID,
)
from rich.console import Console
from rich.table import Table
import time


class ProgressTracker:
    """Reusable progress tracker for BioPress operations."""

    STEPS = [
        "Loading templates",
        "Generating questions",
        "Validating",
        "Building output",
    ]

    def __init__(self, show_eta_threshold: float = 2.0):
        self.console = Console()
        self.show_eta_threshold = show_eta_threshold
        self.start_time: Optional[float] = None
        self.step_start_time: Optional[float] = None
        self.current_step = 0
        self.progress: Optional[Progress] = None
        self.main_task: Optional[TaskID] = None
        self.step_tasks: dict[int, TaskID] = {}

    def start(self) -> None:
        """Start the progress tracking."""
        self.start_time = time.time()
        self.step_start_time = time.time()
        self.current_step = 0

    def create_progress_bar(self) -> Progress:
        """Create and return a Rich progress bar."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=self.console,
        )

    def start_progress(self) -> None:
        """Start the main progress bar."""
        self.progress = self.create_progress_bar()
        self.progress.start()
        self.main_task = self.progress.add_task(
            "Generating questions...", total=100
        )

    def update_progress(self, completed: int, total: int) -> None:
        """Update the main progress bar."""
        if self.progress and self.main_task is not None:
            percentage = int((completed / total) * 100) if total > 0 else 0
            self.progress.update(self.main_task, completed=percentage)

    def show_step_status(self) -> Table:
        """Show step status table."""
        table = Table(show_header=False, box=None)
        table.add_column(style="dim", width=30)
        table.add_column()

        for i, step in enumerate(self.STEPS):
            status = ""
            if i < self.current_step:
                status = "[green]✓[/green]"
            elif i == self.current_step:
                status = "[cyan]In progress...[/cyan]"
            else:
                status = "[dim]Waiting...[/dim]"
            table.add_row(f"Step {i+1}/4: {step}", status)

        return table

    def display_step_status(self) -> None:
        """Display the step status table."""
        table = self.show_step_status()
        self.console.print(table)

    def set_step(self, step: int) -> None:
        """Set the current step."""
        self.current_step = step
        self.step_start_time = time.time()

    def get_elapsed_time(self) -> float:
        """Get elapsed time since start."""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0

    def should_show_eta(self) -> bool:
        """Check if ETA should be shown based on elapsed time."""
        return self.get_elapsed_time() > self.show_eta_threshold

    def stop(self) -> None:
        """Stop the progress tracking."""
        if self.progress:
            self.progress.stop()
            self.progress = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
