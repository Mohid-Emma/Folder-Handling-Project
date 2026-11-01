# controller.py

from tkinter  import messagebox
from frontend import MainWindow
from collections.abc import Callable
from typing   import Any
import config.theme as theme



class App:
    def __init__(self, main_window: MainWindow, ui_compounds: dict[str, Callable[..., Any]], factories: dict[str, Callable[..., Any]]) -> None:
        
        self.factories    = factories
        self.current_data = None

        self.current_mode = "rename"
        self.current_plan = []
        
        operation = {
            "preview" : self.preview,
            "execute" : self.execute,
            "result"  : self.show_result }
        self.main_window = main_window(self.current_mode, ui_compounds, operation)

        self.execute_data = {
            "rename":   ("Rename", "rename_files", "This will change the original filenames."),
            "organize": ("Organize", "organize_files", "Organize the listed files into category folders?"),
            "copy" :    ("Copy", "copy_files", "Copy the listed files? Originals will remain unchanged."),
            "move" :    ("Move", "move_files", "Move the listed files? They will leave their original locations.") }

    # --------------------------------------------------
    # Preview WorkFlow
    # --------------------------------------------------

    def preview(self, current_mode: str, data: dict[str, Callable[..., Any]]) -> list[dict[str, Callable[..., Any]]] | None:

        self.current_data = self.factories[current_mode](data)

        if current_mode != "search":
            try:
                return self._preview(self.current_data, current_mode)

            except (OSError, ValueError) as error:
                self._error(f"{current_mode.capitalize()} preview failed", error)
                return None
        else:
            try:
                results = self.current_data.search_files()
                self.current_mode = "search"
                self._display(results)
                self._set_status(f"Search found {len(results)} file(s).")
                return results

            except (OSError, ValueError) as error:
                self._error("Search failed", error)
                return None
            
    def _preview(self, backend: Callable[..., Any], operation: str) -> list[dict[str, Callable[..., Any]]]:
        plan = backend.create_plan()
        self.current_mode = operation
        self._display(plan)
        self._set_status(f"Preview ready: {len(plan)} item(s).")
        return plan    
    # --------------------------------------------------
    # Execute WorkFlow
    # --------------------------------------------------

    def execute(self, current_mode) -> None:
        mode = {
            "rename"  : lambda: self._execute("rename"),
            "organize": lambda: self._execute("organize"),
            "copy"    : lambda: self._execute("copy"),
            "move"    : lambda: self._execute("move") }
        for operation, form in mode.items():
            if operation == current_mode:
                self.current_callback = form()

    def _execute(self, mode)-> list[dict[str, None]] | None:

        title, method, confirmation = self.execute_data[mode]
        backend = self.current_data
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
            plan = getattr(backend, method)()
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
    # --------------------------------------------------
    # Display Result
    # --------------------------------------------------
    
    def show_result(self, plan: dict[str, Callable[..., Any]]) -> None:
        if plan is not None:
            self._display(plan)
            
    # --------------------------------------------------
    # UI INTEGRATION
    # --------------------------------------------------

    def _display(self, plan: list[dict]) -> None:
        self.current_plan = plan or []

        # Your View should accept a list of dictionaries.
        view = getattr(self.main_window, "view", None)
        if view is not None and hasattr(view, "display_card"):
            view.display_card(self.current_plan)

        self._update_summary(self._summarize(self.current_plan))

    @staticmethod
    def _summarize(plan: list[dict[str, None]]) -> dict[str, int]:
        return {
            "total": len(plan),
            "completed": sum(x.get("status") in {"Finished", "Organized", "Copied", "Moved"} for x in plan),
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