"""Element list component showing questions."""

from typing import Callable

from nicegui import ui


def create_element_list(app_state, on_select: Callable = None):
    """Create the element list showing all questions."""
    with ui.card().classes("w-full h-full"):
        ui.label("Questions").classes("text-h6")
        
        items = app_state.content.get("items", [])
        
        if not items:
            ui.label("No questions loaded")
            return
        
        with ui.column().classes("w-full gap-2"):
            for idx, item in enumerate(items):
                question_text = item.get("question", "")[:60]
                if len(item.get("question", "")) > 60:
                    question_text += "..."
                
                is_selected = idx == app_state.selected_index
                
                with ui.card().classes("cursor-pointer").on_click(lambda i=idx: select_element(i)):
                    if is_selected:
                        ui.label(f"Q{idx + 1}").classes("text-subtitle-2 font-bold text-primary")
                    else:
                        ui.label(f"Q{idx + 1}").classes("text-subtitle-2 font-bold")
                    
                    ui.label(question_text).classes("text-body-2")
                    
                    correct = item.get("correct_answer", "")
                    if correct:
                        ui.label(f"Answer: {correct}").classes("text-caption text-green")
                
                ui.element("div").classes("h-2")

    def select_element(index: int):
        app_state.selected_index = index
        if on_select:
            on_select(index)