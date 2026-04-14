"""Main NiceGUI application for the visual review tool."""

import json
import os
from typing import Optional

from nicegui import ui

from biopress.visual.pages.editor import create_editor_page


class AppState:
    """Global application state."""

    def __init__(self):
        self.current_file: Optional[str] = None
        self.content: dict = {"items": []}
        self.selected_index: int = 0
        self.modified: bool = False
        self.pdf_path: Optional[str] = None


app_state = AppState()


def get_app_state() -> AppState:
    """Get the global app state instance."""
    return app_state


def create_review_app() -> None:
    """Create the main review application UI."""

    @ui.page("/")
    def main_page():
        with ui.header(elevated=True).classes("items-center justify-between"):
            ui.label("BioPress Review Tool").classes("text-h5")
            with ui.row():
                ui.button("Load File", icon="folder_open", on_click=load_file).props("flat")
                ui.button("Save", icon="save", on_click=save_file).props("flat")
                ui.button("Export PDF", icon="picture_as_pdf", on_click=export_pdf).props("flat")

        with ui.row().classes("w-full h-full"):
            with ui.column().classes("w-1/4 h-full"):
                from biopress.visual.components.element_list import create_element_list
                create_element_list(app_state, select_element)
            
            with ui.column().classes("w-1/2 h-full"):
                create_editor_page(app_state, save_changes)
            
            with ui.column().classes("w-1/4 h-full"):
                from biopress.visual.components.pdf_viewer import create_pdf_viewer
                create_pdf_viewer(app_state)

    def select_element(index: int):
        """Handle element selection."""
        app_state.selected_index = index

    def save_changes():
        """Save changes to the content."""
        app_state.modified = True

    def load_file():
        """Load a JSON file for review."""
        ui.navigate.to("/load")

    def save_file():
        """Save the current content to file."""
        if app_state.current_file:
            with open(app_state.current_file, "w") as f:
                json.dump(app_state.content, f, indent=2)
            app_state.modified = False
            ui.notify("File saved successfully", type="positive")

    def export_pdf():
        """Export content to PDF."""
        ui.notify("Export to PDF - Use 'biopress export' command", type="info")

    @ui.page("/load")
    def load_page():
        with ui.header(elevated=True).classes("items-center"):
            ui.label("Load File").classes("text-h5")

        with ui.column().classes("w-full items-center"):
            ui.label("Enter the path to a JSON file").classes("mb-4")
            file_input = ui.input(
                label="File Path",
                placeholder="/path/to/content.json"
            ).classes("w-96")
            
            with ui.row():
                ui.button("Load", on_click=lambda: do_load(file_input.value)).props("color=primary")
                ui.button("Cancel", on_click=lambda: ui.navigate.to("/")).props("flat")

        def do_load(path: str):
            if path and os.path.exists(path):
                with open(path) as f:
                    app_state.content = json.load(f)
                app_state.current_file = path
                app_state.selected_index = 0
                app_state.modified = False
                ui.navigate.to("/")
                ui.notify(f"Loaded: {path}", type="positive")
            else:
                ui.notify("File not found", type="negative")

    ui.run(title="BioPress Review Tool", port=8080, reload=False)


def load_content_from_file(file_path: str) -> bool:
    """Load content from a JSON file."""
    try:
        with open(file_path) as f:
            app_state.content = json.load(f)
        app_state.current_file = file_path
        app_state.selected_index = 0
        app_state.modified = False
        return True
    except Exception as e:
        ui.notify(f"Error loading file: {e}", type="negative")
        return False


def run_app() -> None:
    """Run the visual review application."""
    create_review_app()


if __name__ == "__main__":
    create_review_app()