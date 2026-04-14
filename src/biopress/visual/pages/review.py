"""Review page component."""


from nicegui import ui


def create_review_page():
    """Create the review page showing element list and preview."""
    with ui.card().classes("w-full h-full"):
        ui.label("Review Panel").classes("text-h6")
        ui.label("Select a question from the list to view details")