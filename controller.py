# controller.py

from collections.abc import Callable
from protocols import PlanProvider, PlanExecuter, ControllerCallbacks, Executor
from tkinter   import messagebox
from frontend  import MainWindow
from typing    import Any
from queue     import Queue, Empty
import config.theme as theme



class App:
    def __init__(
            self, 
            main_window: Callable[..., MainWindow], 
            ui_compounds: dict[str, Any], 
            factories: dict[str, Any], 
            executor: dict[str, Executor]) -> None:

        # Dependency injection
        self.factories = factories

        # Current operation state
        self.current_mode = "rename"
        self.current_data: Any = None
        self.current_plan: list[dict[str, Any]] = []

        # Preview state
        self.preview_ready = False
        self.preview_request_id = 0
        self.preview_queue: Queue = Queue()

        # Execution state
        self.execution_in_progress = False
        self.execute_request_id = 0
        self.execute_queue: Queue = Queue()

        # Executors
        self.thread_executor = executor["thread"](max_workers=4)
        self.process_executor = executor["process"](max_workers=4)
        
        operation: ControllerCallbacks = {
            "preview" : self.preview,
            "execute" : self.execute }
 
        self.main_window = main_window(self.current_mode, ui_compounds, operation)
        self.main_window.after(100, self._check_preview_result)
        self.main_window.after(100, self._check_execute_result)

        self.execute_data = {
            "rename":   ("Rename",   "This will change the original filenames."),
            "organize": ("Organize", "Organize the listed files into category folders?"),
            "copy" :    ("Copy",     "Copy the listed files? Originals will remain unchanged."),
            "move" :    ("Move",     "Move the listed files? They will leave their original locations.") }

        self.main_window.protocol("WM_DELETE_WINDOW", self.close)

    # =============================================================
    # Preview WorkFlow
    # =============================================================

    def preview(self, current_mode: str, data: dict[str, Any]) -> None:
        if current_mode not in self.factories:
            self._notice(f"Unsupported operation: {current_mode}")
            return

        if self.execution_in_progress:
            self._notice("Wait for the current operation to finish.")
            return
        
        self.preview_request_id += 1
        request_id = self.preview_request_id

        self.preview_ready = False
        self.current_data = None
        self.current_plan = []
        self.current_mode = current_mode

        try:
            backend = self.factories[current_mode](data)

            future = self.thread_executor.submit(backend.create_plan)
            future.add_done_callback(
                lambda completed_future: self.preview_queue.put((completed_future, backend, current_mode, request_id)))
            
            self._set_status(f"{current_mode.title()}: Preparing preview...")
        except Exception as error:
            self._error("Could not start preview", error)

    def _check_preview_result(self) -> None:
        while True:
            try:
                (future, backend, operation, request_id) = self.preview_queue.get_nowait()
            except Empty:
                break

            if request_id != self.preview_request_id:
                continue

            try:
                plan = future.result()
                self.current_data = backend
                self.current_mode = operation
                self._preview(plan, operation)
            except Exception as error:
                self._error("Preview failed", error)

        self.main_window.after(100, self._check_preview_result)
        
    def _preview(self, plan: list[dict[str, Any]], operation: str) -> None:
        self.current_mode = operation
        self._display(plan)
        
        if operation != "search":
            self._set_status(f"Preview ready: {len(plan)} item(s).")
        else:
            self._set_status(f"Search found {len(plan)} file(s).")

    # =============================================================
    # Execute WorkFlow
    # =============================================================

    def execute(self, current_mode: str) -> None:
        if current_mode not in self.execute_data:
            self._notice(f"Unsupported operation: {current_mode}")
            return
        
        self._execute(current_mode)

    def _execute(self, mode: str) -> None:
        title, confirmation = self.execute_data[mode]
        
        if self.execution_in_progress:
            self._notice("An operation is already running.")
            return
        
        backend: PlanExecuter = self.current_data
        plan = backend.plan

        if backend is None or not getattr(backend, "plan", None):
            self._notice(f"Create a {title.lower()} preview first.")
            return None

        ready = sum(item["status"] == "Ready" for item in plan)

        if not ready:
            self._notice(f"No eligible files to {title.lower()}.")
            return 

        confirmed = messagebox.askyesno(
            f"Confirm {title}", f"{confirmation}\n\nEligible items: {ready}", parent=self.main_window)

        if not confirmed:
            return 
        
        self.execute_request_id += 1
        request_id = self.execute_request_id
        self.execution_in_progress = True
        self._set_status(f"{title}: Processing...")

        try:
            future = self.process_executor.submit(backend.execute_plan)
            future.add_done_callback(
                lambda result: self.execute_queue.put((result, backend, request_id, mode)))
        except Exception as error:
            self.execution_in_progress = False
            self._error("Could not start execution", error)


    def _check_execute_result(self) -> None:
        while True:
            try:
                (future, backend, request_id, mode,) = self.execute_queue.get_nowait()
            except Empty:
                break

            if request_id != self.execute_request_id:
                continue
            self.execution_in_progress = False
            
            try:
                plan = future.result()

                self.current_plan = plan
                self.preview_ready = False
                self.current_data = None

                self._display(plan)

                failed = sum(x["status"] == "Error" for x in plan)
                completed = sum(x["status"] == "Finished" for x in plan)
                self._set_status(f"{mode.title()}: {completed} completed, {failed} failed.")
            
            except Exception as error:
                self._error("Execute failed", error)

        self.main_window.after(100, self._check_execute_result)

    # =========================================================
    # Display and Status
    # =========================================================
    
    def _display(self, plan: list[dict[str, Any]]) -> None:
        self.current_plan = plan or []

        view = getattr(self.main_window, "view", None)
        if view is not None and hasattr(view, "display_card"):
            view.display_card(plan)

        self._update_summary(plan)

    def _update_summary(self, plan: list[dict[str, Any]]) -> None:
        summary = {
        "total"    : len(plan),
        "completed": sum(item["status"] == "Finished" for item in plan),
        "skipped"  : sum(item["status"] in ["Skipped", "Exist"] for item in plan),
        "failed"   : sum(item["status"] == "Error" for item in plan)}
        
        status = self.main_window.status
    
        if hasattr(status, "update_from_result"):
            status.update_from_result(summary)
    
    def _set_status(self, message: str) -> None:

        status = getattr(self.main_window, "status", None)
        if status is not None and hasattr(status, "set_status"):
            status.set_status(message, theme.info)

    # =========================================================
    # Notifications
    # =========================================================

    def _notice(self, message: str) -> None:
        messagebox.showinfo("File & Folder Manager", message, parent=self.main_window )
        return None

    def _error(self, title: str, error: str) -> None:

        message = str(error)
        widget = getattr(self.main_window, "status_label", None)

        if widget is not None:
            widget.configure(
                text=message,
                text_color=theme.error )

        messagebox.showerror(title, message, parent=self.main_window)

    # =========================================================
    # Application Lifecycle
    # =========================================================

    def close(self) -> None:

        self.thread_executor.shutdown()
        self.process_executor.shutdown()

        self.main_window.destroy()

    def run(self) -> None:
        self.main_window.mainloop()