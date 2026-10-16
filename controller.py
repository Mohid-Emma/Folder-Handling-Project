# controller.py

from tkinter  import messagebox
from backend  import Rename, Organize, Copy, Move, Search
from frontend import MainWindow


class App:
    def __init__(self):
        self.rename = None
        self.organize = None
        self.copy = None
        self.move = None
        self.search = None

        self.current_operation = "rename"
        self.current_plan = []

        self.main_window = MainWindow(
            on_rename_preview   = self.rename_preview,
            on_rename_execute   = self.execute_rename,
            on_organize_preview = self.preview_organize,
            on_organize_execute = self.execute_organize,
            on_copy_preview     = self.preview_copy,
            on_copy_execute     = self.execute_copy,
            on_move_preview     = self.preview_move,
            on_move_execute     = self.execute_move,
            on_run_search       = self.run_search,
            on_result           = self.show_result,
        )

    # --------------------------------------------------
    # RENAME: callbacks used by the existing MainWindow
    # --------------------------------------------------


    def rename_preview(self,rename_data):
        self.rename = Rename(rename_data)
        self.current_operation = "rename"
        if self.rename is None:
            return self._notice("Choose a folder and configure rename settings.")

        try:
            plan = self.rename.create_rename_folder()
            self.current_operation = "rename"
            self._display(plan)
            self._set_status(f"Preview ready: {len(plan)} files.")
            summary = self.rename.check_result()
            self._update_summary(summary)
            return plan

        except (OSError, ValueError) as error:
            self._error("Rename preview failed", error)
            return None

    def execute_rename(self):
        if self.rename is None:
            return self._notice("Create a rename preview first.")

        if not self.rename.rename_plan:
            self.rename_preview()

        plan = self.rename.rename_plan
        ready = sum(x["status"] == "Ready" for x in plan)

        if not ready:
            self._notice("There are no eligible files to rename.")
            return plan

        confirmed = messagebox.askyesno(
            "Confirm Rename",
            f"Rename {ready} file(s)?\n\n"
            "This will change the original filenames.",
            parent=self.main_window,
        )

        if not confirmed:
            return None

        try:
            plan = self.rename.rename_files()
            summary = self.rename.check_result()
            self._display(plan)
            self._update_summary(summary)
            self._set_status("Rename completed.")
            return plan

        except OSError as error:
            self._display(self.rename.rename_plan)
            self._error("Rename failed", error)
            return self.rename.rename_plan

    def show_result(self, plan):
        if plan is not None:
            self._display(plan)

    # --------------------------------------------------
    # ORGANIZE
    # --------------------------------------------------

    def preview_organize(self, organize_data):

        try:
            self.organize = Organize(organize_data)
            return self._preview(self.organize, "organize")

        except (OSError, ValueError) as error:
            self._error("Organize preview failed", error)
            return None

    def execute_organize(self):
        return self._execute(
            "Organize",
            self.organize,
            "organize_files",
            "Organize the listed files into category folders?",
        )

    # --------------------------------------------------
    # COPY
    # --------------------------------------------------

    def preview_copy(self, copy_data):

        try:
            self.copy = Copy(copy_data)
            return self._preview(self.copy, "copy")

        except (OSError, ValueError) as error:
            self._error("Copy preview failed", error)
            return None

    def execute_copy(self):
        return self._execute(
            "Copy",
            self.copy,
            "copy_files",
            "Copy the listed files? Originals will remain unchanged.",
        )

    # --------------------------------------------------
    # MOVE
    # --------------------------------------------------

    def preview_move(self, move_date):
    
        try:
            self.move = Move(move_date)
            return self._preview(self.move, "move")

        except (OSError, ValueError) as error:
            self._error("Move preview failed", error)
            return None

    def execute_move(self):
        return self._execute(
            "Move",
            self.move,
            "move_files",
            "Move the listed files? They will leave their original locations.",
        )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def run_search(self, search_data):

        try:
            self.search = Search(search_data)

            results = self.search.search_files()
            self.current_operation = "search"
            self._display(results)
            self._set_status(f"Search found {len(results)} file(s).")
            return results

        except (OSError, ValueError) as error:
            self._error("Search failed", error)
            return None

    # --------------------------------------------------
    # SHARED CONTROLLER WORKFLOW
    # --------------------------------------------------

    def _preview(self, backend, operation):
        plan = backend.create_plan()
        self.current_operation = operation
        self._display(plan)
        self._set_status(f"Preview ready: {len(plan)} item(s).")
        return plan

    def _execute(self, title, backend, method, confirmation):
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
            parent=self.main_window,
        )

        if not confirmed:
            return None

        try:
            plan = getattr(backend, method)()
            self._display(plan)

            failed = sum(x["status"] == "Error" for x in plan)
            completed = sum(
                x["status"] in {
                    "Organized", "Copied", "Moved", "Finished"
                }
                for x in plan
            )

            self._set_status(
                f"{title}: {completed} completed, {failed} failed."
            )
            return plan

        except OSError as error:
            self._display(backend.plan)
            self._error(f"{title} failed", error)
            return backend.plan

    # --------------------------------------------------
    # UI INTEGRATION
    # --------------------------------------------------

    def _display(self, plan):
        self.current_plan = plan or []

        # Your View should accept a list of dictionaries.
        view = getattr(self.main_window, "view", None)
        if view is not None and hasattr(view, "display_card"):
            view.display_card(self.current_plan)

        self._update_summary(self._summarize(self.current_plan))

    @staticmethod
    def _summarize(plan):
        return {
            "total": len(plan),
            "completed": sum(
                x.get("status") in {
                    "Finished", "Organized", "Copied", "Moved"
                } for x in plan
            ),
            "skipped": sum(
                x.get("status") in {"Skipped", "Exist"}
                for x in plan
            ),
            "failed": sum(
                x.get("status") == "Error" for x in plan
            ),
        }
    
    def _update_summary(self, summary):
        status = self.main_window.status
    
        if hasattr(status, "update_from_result"):
            status.update_from_result(summary)
    
        # Keep the existing footer in sync during the transition.
        labels = {
            "status_total": f"Total: {summary.get('total', 0)}",
            "status_renamed": (
                f"Completed: {summary.get('completed', summary.get('renamed', 0))}"
            ),
            "status_skipped": f"Skipped: {summary.get('skipped', 0)}",
            "status_failed": f"Failed: {summary.get('failed', 0)}",
        }
    
        for attribute, text in labels.items():
            widget = getattr(self.main_window, attribute, None)
            if widget is not None:
                widget.configure(text=text)

    def _set_status(self, message):
        import config.theme as theme

        for attribute in ("status_label", "header_status_label"):
            widget = getattr(self.main_window, attribute, None)
            if widget is not None:
                widget.configure(
                    text=message,
                    text_color=theme.text_secondary,
                )

        status = getattr(self.main_window, "status", None)
        if status is not None and hasattr(status, "set_status"):
            status.set_status(message, theme.info)

    def _notice(self, message):
        messagebox.showinfo(
            "File & Folder Manager",
            message,
            parent=self.main_window,
        )
        return None

    def _error(self, title, error):
        import config.theme as theme

        message = str(error)
        widget = getattr(self.main_window, "status_label", None)

        if widget is not None:
            widget.configure(
                text=message,
                text_color=theme.error,
            )

        messagebox.showerror(
            title, message, parent=self.main_window
        )
        return None

    def run(self):
        self.main_window.mainloop()