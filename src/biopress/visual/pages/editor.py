"""Editor page component for editing questions."""

from typing import Callable
import tempfile

from nicegui import ui


def create_editor_page(app_state, on_save: Callable = None):
    """Create the editor page for editing question content."""
    from biopress.core.memory import get_memory
    with ui.card().classes("w-full h-full"):
        with ui.row().classes("w-full justify-between items-center"):
            ui.label("Editor").classes("text-h6")
            with ui.row():
                ui.button(icon="add", on_click=lambda: add_new_question()).props("flat round color=positive")
                ui.button(icon="delete", on_click=lambda: delete_question()).props("flat round color=negative")
                ui.button(icon="refresh", on_click=lambda: show_replace_dialog()).props("flat round")
                ui.button(icon="picture_as_pdf", on_click=lambda: export_to_pdf()).props("flat round color=accent")

        if not app_state.content.get("items"):
            ui.label("No content loaded")
            return

        idx = app_state.selected_index
        if idx >= len(app_state.content.get("items", [])):
            ui.label("Invalid selection")
            return

        item = app_state.content["items"][idx]

        with ui.column().classes("w-full gap-2"):
            with ui.row().classes("w-full justify-between"):
                ui.label(f"Question {idx + 1}").classes("text-subtitle-1 font-bold")
                if item.get("diagram"):
                    ui.label(f"📊 Diagram: {item.get('diagram', 'None')}").classes("text-caption")

            question_input = ui.input(
                label="Question",
                value=item.get("question", "")
            ).classes("w-full")

            with ui.tabs().classes("w-full") as tabs:
                options_tab = ui.tab("Options")
                diagram_tab = ui.tab("Diagram")
                dashboard_tab = ui.tab("Dashboard")

            with ui.tab_panels(tabs, value=options_tab).classes("w-full"):
                with ui.tab_panel(options_tab):
                    ui.label("Options").classes("text-subtitle-2")
                    options = item.get("options", {})

                    option_a = ui.input(
                        label="A",
                        value=options.get("A", "")
                    ).classes("w-full")

                    option_b = ui.input(
                        label="B",
                        value=options.get("B", "")
                    ).classes("w-full")

                    option_c = ui.input(
                        label="C",
                        value=options.get("C", "")
                    ).classes("w-full")

                    option_d = ui.input(
                        label="D",
                        value=options.get("D", "")
                    ).classes("w-full")

                    correct = ui.select(
                        label="Correct Answer",
                        options=["A", "B", "C", "D"],
                        value=item.get("correct_answer", "A")
                    ).classes("w-full")

                    explanation = ui.textarea(
                        label="Explanation",
                        value=item.get("explanation", "")
                    ).classes("w-full")

                with ui.tab_panel(diagram_tab):
                    ui.label("Diagram Replacement").classes("text-subtitle-2 mb-2")
                    current_diagram = item.get("diagram", "")
                    diagram_input = ui.input(
                        label="Diagram Path/URL",
                        value=current_diagram,
                        placeholder="Enter diagram file path or URL"
                    ).classes("w-full")
                    with ui.row():
                        ui.button("Browse", icon="folder_open", on_click=lambda: browse_diagram()).props("flat")
                        ui.button("Clear", icon="clear", on_click=lambda: clear_diagram(_diagram_input_ref)).props("flat")
                    if current_diagram:
                        ui.label(f"Current: {current_diagram}").classes("text-caption")
                    
                    _diagram_input_ref = diagram_input

                with ui.tab_panel(dashboard_tab):
                    create_progress_dashboard(app_state)

            ui.button(
                "Save Changes",
                icon="save",
                on_click=lambda: save_changes(
                    question_input.value,
                    option_a.value,
                    option_b.value,
                    option_c.value,
                    option_d.value,
                    correct.value,
                    explanation.value,
                    diagram_input.value if 'diagram_input' in dir() else item.get("diagram", "")
                )
            ).props("color=primary")

    def save_changes(
        question: str,
        a: str,
        b: str,
        c: str,
        d: str,
        correct: str,
        explanation: str,
        diagram: str = ""
    ):
        item = app_state.content["items"][app_state.selected_index]
        original = f"{item.get('question', '')}:{item.get('explanation', '')}"
        corrected = f"{question}:{explanation}"

        app_state.content["items"][app_state.selected_index] = {
            "question": question,
            "options": {"A": a, "B": b, "C": c, "D": d},
            "correct_answer": correct,
            "explanation": explanation,
            "diagram": diagram
        }
        if on_save:
            on_save()

        memory = get_memory()
        if memory.enabled:
            memory.track_correction(original, corrected, "editor_save")

        ui.notify("Changes saved", type="positive")

    def add_new_question():
        """Add a new question to the content."""
        new_question = {
            "question": "New Question",
            "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
            "correct_answer": "A",
            "explanation": "Explanation for the correct answer."
        }
        app_state.content["items"].append(new_question)
        app_state.selected_index = len(app_state.content["items"]) - 1
        if on_save:
            on_save()
        ui.notify("New question added", type="positive")

    def delete_question():
        """Delete the current question with confirmation."""
        items = app_state.content.get("items", [])
        if len(items) <= 1:
            ui.notify("Cannot delete the last question", type="warning")
            return

        with ui.dialog() as dialog, ui.card():
            ui.label(f"Delete Question {app_state.selected_index + 1}?")
            ui.label("This action cannot be undone.")
            with ui.row():
                ui.button("Cancel", on_click=dialog.close).props("flat")
                ui.button("Delete", on_click=lambda: confirm_delete(dialog)).props("color=negative")

        dialog.open()

    def confirm_delete(dialog):
        """Confirm and execute question deletion."""
        idx = app_state.selected_index
        app_state.content["items"].pop(idx)
        if idx >= len(app_state.content["items"]):
            app_state.selected_index = max(0, len(app_state.content["items"]) - 1)
        if on_save:
            on_save()
        dialog.close()
        ui.notify("Question deleted", type="info")

    def show_replace_dialog():
        """Show dialog to replace entire question."""
        with ui.dialog() as dialog, ui.card().classes("w-96"):
            ui.label("Replace Question").classes("text-h6 mb-4")
            new_question = ui.input(label="New Question Text").classes("w-full")
            new_options = {
                "A": ui.input(label="Option A").classes("w-full"),
                "B": ui.input(label="Option B").classes("w-full"),
                "C": ui.input(label="Option C").classes("w-full"),
                "D": ui.input(label="Option D").classes("w-full"),
            }
            new_correct = ui.select(
                label="Correct Answer",
                options=["A", "B", "C", "D"],
                value="A"
            ).classes("w-full")
            new_explanation = ui.textarea(label="Explanation").classes("w-full")

            with ui.row():
                ui.button("Cancel", on_click=dialog.close).props("flat")
                ui.button("Replace", on_click=lambda: do_replace(dialog)).props("color=primary")

        dialog.open()

        def do_replace(dialog):
            """Execute the question replacement."""
            app_state.content["items"][app_state.selected_index] = {
                "question": new_question.value or "New Question",
                "options": {
                    "A": new_options["A"].value or "Option A",
                    "B": new_options["B"].value or "Option B",
                    "C": new_options["C"].value or "Option C",
                    "D": new_options["D"].value or "Option D",
                },
                "correct_answer": new_correct.value,
                "explanation": new_explanation.value or ""
            }
            if on_save:
                on_save()
            dialog.close()
            ui.notify("Question replaced", type="positive")

    def browse_diagram():
        """Browse for diagram file."""
        ui.notify("Diagram browser - enter file path in the input field", type="info")

    def clear_diagram(diagram_input):
        """Clear the diagram field."""
        diagram_input.value = ""

    def export_to_pdf():
        """Export current editor content as PDF via PDFBuilder."""
        from biopress.pdf.builder import PDFBuilder
        items = app_state.content.get("items", [])
        if not items:
            ui.notify("No content to export", type="warning")
            return

        try:
            output_path = tempfile.mktemp(suffix=".pdf", prefix="biopress_export_")
            builder = PDFBuilder()
            builder.build_from_data(
                quiz_data=items,
                output_path=output_path,
                style="default",
                title="BioPress Export",
            )
            ui.download(output_path)
            ui.notify("PDF exported successfully", type="positive")
        except Exception as e:
            ui.notify(f"Export failed: {e}", type="negative")


def create_progress_dashboard(app_state):
    """Create progress dashboard with statistics."""
    items = app_state.content.get("items", [])
    total = len(items)

    if total == 0:
        ui.label("No questions to display")
        return

    with ui.column().classes("w-full gap-4"):
        with ui.row().classes("w-full justify-around"):
            with ui.card().classes("p-4 text-center"):
                ui.label(str(total)).classes("text-h4")
                ui.label("Total Questions").classes("text-caption")

            answered = sum(1 for i in items if i.get("correct_answer"))
            with ui.card().classes("p-4 text-center"):
                ui.label(str(answered)).classes("text-h4")
                ui.label("With Answers").classes("text-caption")

            with_diagram = sum(1 for i in items if i.get("diagram"))
            with ui.card().classes("p-4 text-center"):
                ui.label(str(with_diagram)).classes("text-h4")
                ui.label("With Diagrams").classes("text-caption")

        with ui.card().classes("w-full p-4"):
            ui.label("Question Status").classes("text-subtitle-1 font-bold mb-2")
            for idx, item in enumerate(items):
                status_icon = "✅" if item.get("correct_answer") else "⚪"
                diagram_icon = "📊" if item.get("diagram") else ""
                ui.label(f"{status_icon} Q{idx + 1}: {item.get('question', '')[:50]}... {diagram_icon}").classes("text-body-2")

        completion_pct = (answered / total * 100) if total > 0 else 0
        with ui.card().classes("w-full p-4"):
            ui.label(f"Completion: {completion_pct:.0f}%").classes("text-subtitle-1")
            with ui.linear_progress(value=completion_pct / 100).classes("w-full"):
                pass