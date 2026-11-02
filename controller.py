# controller.py

from tkinter   import messagebox
from frontend  import MainWindow
from typing    import Any
from protocols import PlanProvider, PlanExecuter, ControllerCallbacks
from collections.abc import Callable
import config.theme as theme



class App:
    def __init__(self, main_window: Callable[..., MainWindow], ui_compounds: dict[str, Any], factories: dict[str, Any]) -> None:
        
        self.factories    = factories
        self.current_data = None

        self.current_mode = "rename"
        self.current_plan = []
        
        operation: ControllerCallbacks = {
            "preview" : self.preview,
            "execute" : self.execute }
 
        self.main_window = main_window(self.current_mode, ui_compounds, operation)

        self.execute_data = {
            "rename":   ("Rename",   "This will change the original filenames."),
            "organize": ("Organize", "Organize the listed files into category folders?"),
            "copy" :    ("Copy",     "Copy the listed files? Originals will remain unchanged."),
            "move" :    ("Move",     "Move the listed files? They will leave their original locations.") }

    # =============================================================
    # Preview WorkFlow
    # =============================================================

    def preview(self, current_mode: str, data: dict[str, Any]) -> list[dict[str, Any]] | None:

        self.current_data = self.factories[current_mode](data)

        try:
            return self._preview(self.current_data, current_mode)
        
        except (OSError, ValueError) as error:
            if current_mode != "search":
                self._error(f"{current_mode.capitalize()} preview failed", error)
            else:
                self._error("Search failed", error)
            return None

            
    def _preview(self, backend: PlanProvider, operation: str) -> list[dict[str, Any]]:
        plan = backend.create_plan()
        self.current_mode = operation

        self._display(plan)
        if operation != "search":
            self._set_status(f"Preview ready: {len(plan)} item(s).")
        else:
            self._set_status(f"Search found {len(plan)} file(s).")

        return plan
        
    # =============================================================
    # Execute WorkFlow
    # =============================================================

    def execute(self, current_mode: str) -> None:
        if current_mode not in self.execute_data:
            self._notice(f"Unsupported operation: {current_mode}")
            return
        
        self._execute(current_mode)

    def _execute(self, mode: str)-> list[dict[str, Any]] | None:

        title, confirmation = self.execute_data[mode]
        backend: PlanExecuter = self.current_data
        if backend is None or not getattr(backend, "plan", None):
            self._notice(f"Create a {title.lower()} preview first.")
            return None

        plan = backend.plan
        ready = sum(item["status"] == "Ready" for item in plan)

        if not ready:
            self._notice(f"No eligible files to {title.lower()}.")
            return plan

        confirmed = messagebox.askyesno(
            f"Confirm {title}",
            f"{confirmation}\n\nEligible items: {ready}",
            parent=self.main_window)

        if not confirmed:
            return None

        try:
            plan = backend.execute_plan()
            self._display(plan)

            failed = sum(x["status"] == "Error" for x in plan)
            completed = sum(x["status"] in {"Organized", "Copied", "Moved", "Finished"}
                        for x in plan)

            self._set_status(f"{title}: {completed} completed, {failed} failed.")
            return plan

        except OSError as error:
            self._display(backend.plan)
            self._error(f"{title} failed", error)
            return backend.plan
            
    # =============================================================
    # UI INTEGRATION
    # =============================================================

    def _display(self, plan: list[dict[str, Any]]) -> None:
        self.current_plan = plan or []

        # Your View should accept a list of dictionaries.
        view = getattr(self.main_window, "view", None)
        if view is not None and hasattr(view, "display_card"):
            view.display_card(self.current_plan)

        self._update_summary(self._summarize(self.current_plan))

    @staticmethod
    def _summarize(plan: list[dict[str, Any]]) -> dict[str, int]:
        return {
            "total": len(plan),
            "completed": sum(x.get("status") == "Finished" for x in plan),
            "skipped": sum( x.get("status") in {"Skipped", "Exist"} for x in plan),
            "failed": sum(x.get("status") == "Error" for x in plan) }
    
    def _update_summary(self, summary: dict[str, int]) -> None:
        status = self.main_window.status
    
        if hasattr(status, "update_from_result"):
            status.update_from_result(summary)
    
        # Keep the existing footer in sync during the transition.
        labels = {
        "status_total"  : f"Total: {summary.get('total', 0)}",
        "status_renamed": (f"Completed: {summary.get('completed')}"),
        "status_skipped": f"Skipped: {summary.get('skipped', 0)}",
        "status_failed" : f"Failed: {summary.get('failed', 0)}"}
    
        for attribute, text in labels.items():
            widget = getattr(self.main_window, attribute, None)
            if widget is not None:
                widget.configure(text=text)

    def _set_status(self, message: str) -> None:

        for attribute in ("status_label", "header_status_label"):
            widget = getattr(self.main_window, attribute, None)
            if widget is not None:
                widget.configure(
                    text=message,
                    text_color=theme.text_secondary)

        status = getattr(self.main_window, "status", None)
        if status is not None and hasattr(status, "set_status"):
            status.set_status(message, theme.info)

    def _notice(self, message: str) -> None:
        messagebox.showinfo(
            "File & Folder Manager",
            message,
            parent=self.main_window )
        return None

    def _error(self, title: str, error: str) -> None:

        message = str(error)
        widget = getattr(self.main_window, "status_label", None)

        if widget is not None:
            widget.configure(
                text=message,
                text_color=theme.error )

        messagebox.showerror(title, message, parent=self.main_window)
        return None

    def run(self) -> None:
        self.main_window.mainloop()