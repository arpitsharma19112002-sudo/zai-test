"""PDF viewer component using pdf.js."""

from nicegui import ui


def create_pdf_viewer(app_state):
    """Create the PDF viewer component."""
    with ui.card().classes("w-full h-full"):
        ui.label("PDF Preview").classes("text-h6")
        
        with ui.tabs().classes("w-full") as tabs:
            preview_tab = ui.tab("Preview")
            source_tab = ui.tab("Source")
        
        with ui.tab_panels(tabs, value=preview_tab).classes("w-full h-full"):
            with ui.tab_panel(preview_tab).classes("w-full h-full"):
                if app_state.pdf_path:
                    ui.html(
                        f'<iframe src="/static/pdfjs/web/viewer.html?file={app_state.pdf_path}" '
                        f'width="100%" height="100%" style="border:none;"></iframe>'
                    ).classes("w-full h-96")
                else:
                    with ui.column().classes("w-full items-center justify-center h-64"):
                        ui.icon("picture_as_pdf").props("size=xl")
                        ui.label("No PDF loaded").classes("mt-4")
                        ui.label("Export from editor to view PDF").classes("text-caption")
            
            with ui.tab_panel(source_tab).classes("w-full"):
                ui.label("PDF Source").classes("text-subtitle-1")
                if app_state.pdf_path:
                    ui.label(app_state.pdf_path)
                else:
                    ui.label("No PDF available")


def set_pdf_path(app_state, path: str):
    """Set the PDF path for the viewer."""
    app_state.pdf_path = path