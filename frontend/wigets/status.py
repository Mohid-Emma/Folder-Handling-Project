# frontend/wigets/status.py

import customtkinter as ctk
import config.theme as theme


class Status(ctk.CTkFrame):

    MODE_INFO = {
        "rename": {
            "status": "Ready to rename",
            "info_title": "File Name Pattern",
            "info_text": (
                "The application creates numbered file names "
                "based on your selected pattern and settings."
            ),
        },
        "organize": {
            "status": "Ready to organize",
            "info_title": "File Organization",
            "info_text": (
                "Files are arranged into folders based on the "
                "selected organization method."
            ),
        },
        "copy": {
            "status": "Ready to copy",
            "info_title": "Copy Files",
            "info_text": (
                "Selected files are copied to your destination "
                "folder while following your copy settings."
            ),
        },
        "move": {
            "status": "Ready to move",
            "info_title": "Move Files",
            "info_text": (
                "Selected files are moved to your destination "
                "folder according to your move settings."
            ),
        },
        "search": {
            "status": "Ready to search",
            "info_title": "Search Files",
            "info_text": (
                "Find files by name, file type, and other "
                "search options supported by your settings."
            ),
        },
    }

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            width=220,
            fg_color=theme.panel,
            corner_radius=10,
            border_width=1,
            border_color=theme.border,
            **kwargs,
        )

        self.current_mode = "rename"

        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        # STATUS heading
        ctk.CTkLabel(
            master=self,
            text="STATUS",
            anchor="w",
            font=("Roboto", 13, "bold"),
            text_color=theme.text_secondary,
        ).grid(
            row=0, column=0,
            padx=18, pady=(18, 8),
            sticky="ew",
        )

        # Current status message
        self.status_value = ctk.CTkLabel(
            master=self,
            text="●  Ready to rename",
            anchor="w",
            font=("Roboto", 14),
            text_color=theme.success,
            wraplength=185,
            justify="left",
        )
        self.status_value.grid(
            row=1, column=0,
            padx=18, pady=(0, 16),
            sticky="ew",
        )

        self._divider(row=2, pady=2)

        # SUMMARY heading
        ctk.CTkLabel(
            master=self,
            text="SUMMARY",
            anchor="w",
            font=("Roboto", 13, "bold"),
            text_color=theme.text_secondary,
        ).grid(
            row=3, column=0,
            padx=18, pady=(18, 10),
            sticky="ew",
        )

        # Counts
        self.total_value = self._summary_row(
            "Total Files", "0", 4, theme.text_primary
        )
        self.ready_value = self._summary_row(
            "Ready", "0", 5, theme.success
        )
        self.exists_value = self._summary_row(
            "Already Exists", "0", 6, theme.warning
        )
        self.skipped_value = self._summary_row(
            "Skipped", "0", 7, theme.text_secondary
        )
        self.failed_value = self._summary_row(
            "Failed", "0", 8, theme.error
        )

        self._divider(row=9, pady=(14, 8))

        # Context-sensitive information
        self.info_title = ctk.CTkLabel(
            master=self,
            text="ⓘ  File Name Pattern",
            anchor="w",
            font=("Roboto", 13, "bold"),
            text_color=theme.text_secondary,
            wraplength=185,
        )
        self.info_title.grid(
            row=10, column=0,
            padx=18, pady=(12, 6),
            sticky="ew",
        )

        self.info_text = ctk.CTkLabel(
            master=self,
            text=self.MODE_INFO["rename"]["info_text"],
            anchor="w",
            justify="left",
            wraplength=185,
            font=("Roboto", 12),
            text_color=theme.text_muted,
        )
        self.info_text.grid(
            row=11, column=0,
            padx=18, pady=(0, 18),
            sticky="ew",
        )

        self.grid_propagate(True)

    # ---------------------------------------------------------
    # Layout helpers
    # ---------------------------------------------------------
    def _divider(self, row, pady=2):
        ctk.CTkFrame(
            master=self,
            height=1,
            fg_color=theme.border,
        ).grid(
            row=row, column=0,
            padx=18, pady=pady,
            sticky="ew",
        )

    def _summary_row(self, label, value, row, color):
        line = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
        )
        line.grid(
            row=row, column=0,
            padx=18, pady=6,
            sticky="ew",
        )
        line.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            master=line,
            text=label,
            anchor="w",
            font=("Roboto", 12),
            text_color=theme.text_secondary,
        ).grid(
            row=0, column=0,
            sticky="w",
        )

        value_label = ctk.CTkLabel(
            master=line,
            text=value,
            anchor="e",
            font=("Roboto", 14, "bold"),
            text_color=color,
        )
        value_label.grid(
            row=0, column=1,
            sticky="e",
        )

        return value_label

    # ---------------------------------------------------------
    # Sidebar mode switching
    # ---------------------------------------------------------
    def change_status(self, mode):
        mode = mode.lower().strip()

        if mode not in self.MODE_INFO:
            raise ValueError(f"Unsupported status mode: {mode}")

        self.current_mode = mode
        settings = self.MODE_INFO[mode]

        self.info_title.configure(
            text=f"ⓘ  {settings['info_title']}"
        )
        self.info_text.configure(
            text=settings["info_text"]
        )

        self.reset_summary()
        self.set_status(settings["status"], theme.success)

    # ---------------------------------------------------------
    # Status message
    # ---------------------------------------------------------
    def set_status(self, text, color=None):
        self.status_value.configure(
            text=f"●  {text}",
            text_color=color or theme.success,
        )

    # ---------------------------------------------------------
    # Summary updates
    # ---------------------------------------------------------
    def update_summary(
        self,
        total=0,
        ready=0,
        exists=0,
        skipped=0,
        failed=0,
    ):
        self.total_value.configure(text=str(total))
        self.ready_value.configure(text=str(ready))
        self.exists_value.configure(text=str(exists))
        self.skipped_value.configure(text=str(skipped))
        self.failed_value.configure(text=str(failed))

    def reset_summary(self):
        self.update_summary()

    # ---------------------------------------------------------
    # Optional: update from a backend summary dictionary
    # ---------------------------------------------------------
    def update_from_result(self, summary):
        """
        Accepts summary dictionaries with common backend keys.

        Example:
            {
                "total": 10,
                "renamed": 7,
                "skipped": 2,
                "failed": 1
            }
        """
        if not isinstance(summary, dict):
            return

        total = summary.get(
            "total",
            summary.get("total_files", 0),
        )

        ready = summary.get("ready", summary.get( "renamed", summary.get("copied", summary.get("moved", summary.get("organized", summary.get("found", 0))))))

        exists = summary.get(
            "exists",
            summary.get("already_exists", 0),
        )

        skipped = summary.get("skipped", 0)

        failed = summary.get(
            "failed",
            summary.get("errors", 0),
        )

        self.update_summary(
            total=total,
            ready=ready,
            exists=exists,
            skipped=skipped,
            failed=failed,
        )