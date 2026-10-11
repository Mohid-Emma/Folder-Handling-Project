# view.py
import customtkinter as ctk

from config import theme


class View(ctk.CTkFrame):
    """Reusable results view for Rename, Organize, Copy, Move and Search."""

    MODES = {
        "rename": {
            "title": "Rename Preview",
            "description": "Review the new names before renaming files.",
        },
        "organize": {
            "title": "Organize Preview",
            "description": "Review where each file will be organized.",
        },
        "copy": {
            "title": "Copy Preview",
            "description": "Review which files will be copied.",
        },
        "move": {
            "title": "Move Preview",
            "description": "Review which files will be moved.",
        },
        "search": {
            "title": "Search Results",
            "description": "Files matching your search will appear here.",
        },
    }

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=theme.panel,
            corner_radius=12,
            **kwargs,
        )

        self.current_mode = "rename"
        self.cards = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Heading
        self.heading_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.heading_frame.grid(
            row=0, column=0, sticky="ew", padx=18, pady=(16, 8)
        )
        self.heading_frame.grid_columnconfigure(0, weight=1)

        self.heading_label = ctk.CTkLabel(
            self.heading_frame,
            text="Rename Preview",
            font=(theme.font, 20, "bold"),
            text_color=theme.text_primary,
            anchor="w",
        )
        self.heading_label.grid(row=0, column=0, sticky="w")

        self.description_label = ctk.CTkLabel(
            self.heading_frame,
            text="Review the new names before renaming files.",
            font=(theme.font, 12),
            text_color=theme.text_muted,
            anchor="w",
        )
        self.description_label.grid(
            row=1, column=0, sticky="w", pady=(4, 0)
        )

        # Scrollable results area
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=8,
        )
        self.results_frame.grid(
            row=1, column=0, sticky="nsew", padx=12, pady=(0, 12)
        )
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.show_empty()

    # ---------------------------------------------------------
    # Sidebar mode changes
    # ---------------------------------------------------------
    def change_view(self, mode):
        """Change the view when a sidebar tool is selected."""
        mode = mode.lower().strip()

        if mode not in self.MODES:
            raise ValueError(f"Unsupported view mode: {mode}")

        self.current_mode = mode
        settings = self.MODES[mode]

        self.heading_label.configure(text=settings["title"])
        self.description_label.configure(text=settings["description"])

        # Don't show results left over from another tool.
        self.clear_cards()
        self.show_empty()

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------
    def display_card(self, plan):
        """
        Display a backend plan.

        Supports:
        - A list of dictionaries.
        - A list of [source, destination, status] rename entries.
        - A single dictionary.
        """
        self.clear_cards()

        if plan is None:
            self.show_empty()
            return

        if isinstance(plan, dict):
            # Search results or plans may be wrapped in a dictionary.
            if "results" in plan and isinstance(plan["results"], list):
                items = plan["results"]
            elif "plan" in plan and isinstance(plan["plan"], list):
                items = plan["plan"]
            else:
                items = [plan]
        else:
            try:
                items = list(plan)
            except TypeError:
                items = [plan]

        if not items:
            self.show_empty("No items to display.")
            return

        for index, item in enumerate(items, start=1):
            data = self._normalize_item(item)
            self._create_result_card(index, data)

    def _normalize_item(self, item):
        """Convert different backend plan formats into one format."""
        if isinstance(item, dict):
            return {
                "source": item.get(
                    "source",
                    item.get("old_name", item.get("path", "")),
                ),
                "destination": item.get(
                    "destination",
                    item.get("new_name", item.get("target", "")),
                ),
                "status": item.get("status", "Ready"),
                "message": item.get("message", ""),
                "size": item.get("size", ""),
                "modified": item.get("modified", ""),
                "raw": item,
            }

        if isinstance(item, (list, tuple)):
            source = item[0] if len(item) > 0 else ""
            destination = item[1] if len(item) > 1 else ""
            status = item[2] if len(item) > 2 else "Ready"

            return {
                "source": source,
                "destination": destination,
                "status": status,
                "message": "",
                "size": "",
                "modified": "",
                "raw": item,
            }

        return {
            "source": str(item),
            "destination": "",
            "status": "Found",
            "message": "",
            "size": "",
            "modified": "",
            "raw": item,
        }

    def _create_result_card(self, index, data):
        """Create one result card in the scrollable area."""
        card = ctk.CTkFrame(
            self.results_frame,
            fg_color=theme.panel_light,
            border_width=1,
            border_color=theme.border,
            corner_radius=10,
        )
        card.grid(
            row=index - 1,
            column=0,
            sticky="ew",
            padx=4,
            pady=5,
        )
        card.grid_columnconfigure(0, weight=1)

        source = self._display_value(data["source"])
        destination = self._display_value(data["destination"])
        status = str(data["status"] or "Ready")
        message = str(data["message"] or "")

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.grid(
            row=0, column=0, sticky="ew", padx=12, pady=(10, 6)
        )
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top_row,
            text=f"Item {index}",
            font=(theme.font, 12, "bold"),
            text_color=theme.text_secondary,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            top_row,
            text=status,
            font=(theme.font, 11, "bold"),
            text_color=self._status_color(status),
            fg_color=theme.background,
            corner_radius=6,
            padx=9,
            pady=4,
        ).grid(row=0, column=1, sticky="e")

        self._add_detail(card, "Source", source, row=1)

        # Destination can be empty for search results.
        if destination and destination != source:
            self._add_detail(card, self._destination_label(), destination, row=2)

        if data["size"]:
            self._add_detail(card, "Size", str(data["size"]), row=3)

        if data["modified"]:
            self._add_detail(card, "Modified", str(data["modified"]), row=4)

        if message:
            ctk.CTkLabel(
                card,
                text=message,
                font=(theme.font, 11),
                text_color=self._status_color(status),
                anchor="w",
                justify="left",
                wraplength=650,
            ).grid(
                row=5,
                column=0,
                sticky="ew",
                padx=12,
                pady=(4, 10),
            )
        else:
            # Small bottom padding when there is no message.
            ctk.CTkFrame(
                card,
                height=4,
                fg_color="transparent",
            ).grid(row=5, column=0)

        self.cards.append(card)

    def _add_detail(self, parent, label, value, row):
        """Add a label/value row to a result card."""
        detail = ctk.CTkFrame(parent, fg_color="transparent")
        detail.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=12,
            pady=3,
        )
        detail.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            detail,
            text=f"{label}:",
            width=95,
            font=(theme.font, 11, "bold"),
            text_color=theme.text_muted,
            anchor="w",
        ).grid(row=0, column=0, sticky="nw")

        ctk.CTkLabel(
            detail,
            text=value,
            font=(theme.font, 11),
            text_color=theme.text_primary,
            anchor="w",
            justify="left",
            wraplength=650,
        ).grid(row=0, column=1, sticky="ew")

    # ---------------------------------------------------------
    # Empty state and helpers
    # ---------------------------------------------------------
    def show_empty(self, message=None):
        """Show a simple empty state when there are no results."""
        self.empty_label = ctk.CTkLabel(
            self.results_frame,
            text=message or "No preview available yet.",
            font=(theme.font, 13),
            text_color=theme.text_muted,
        )
        self.empty_label.grid(
            row=0,
            column=0,
            sticky="n",
            padx=10,
            pady=35,
        )

    def clear_cards(self):
        """Remove old cards before showing a new mode or plan."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.cards.clear()

    def clear_preview(self):
        """Compatibility method for code using clear_preview()."""
        self.clear_cards()
        self.show_empty()

    def _destination_label(self):
        return {
            "rename": "New name",
            "organize": "Destination",
            "copy": "Copy to",
            "move": "Move to",
            "search": "Location",
        }.get(self.current_mode, "Destination")

    @staticmethod
    def _display_value(value):
        if value is None:
            return ""
        return str(value)

    @staticmethod
    def _status_color(status):
        status = str(status).lower()

        if any(word in status for word in ("error", "failed", "invalid")):
            return theme.error

        if any(word in status for word in ("exist", "skip", "warning", "conflict")):
            return theme.warning

        if any(word in status for word in ("finished", "renamed", "copied", "moved", "success", "found")):
            return theme.success

        return theme.info