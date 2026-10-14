
import customtkinter as ctk

import config.theme as theme
import config.icon as icon

from utils.file_utils import icon_image_convert
from tkinter_icons import BootstrapIcon


class View(ctk.CTkFrame):

    MODE_CONFIG = {
        "rename": {
            "title": "Rename Preview",
            "description": "Review the original and proposed file names.",
            "columns": ("Original Name", "New Name", "Status"),
            "empty": "Select a folder and preview your rename plan.",
            "icon": icon.rename,
        },
        "organize": {
            "title": "Organize Preview",
            "description": "Review how files will be organized.",
            "columns": ("Original File", "Destination", "Status"),
            "empty": "Preview your plan to see where files will go.",
            "icon": icon.organize,
        },
        "copy": {
            "title": "Copy Preview",
            "description": "Review the files that will be copied.",
            "columns": ("Source File", "Destination", "Status"),
            "empty": "Select folders and preview your copy plan.",
            "icon": icon.copy,
        },
        "move": {
            "title": "Move Preview",
            "description": "Review the files that will be moved.",
            "columns": ("Source File", "Destination", "Status"),
            "empty": "Select folders and preview your move plan.",
            "icon": icon.move,
        },
        "search": {
            "title": "Search Results",
            "description": "Files matching your search appear here.",
            "columns": ("File Name", "Location", "Status"),
            "empty": "Enter your search criteria to find files.",
            "icon": icon.search,
        },
    }

    STATUS_CONFIG = {
        "ready": (icon.info, theme.info),
        "finished": (icon.success_fill, theme.success),
        "renamed": (icon.success_fill, theme.success),
        "organized": (icon.success_fill, theme.success),
        "copied": (icon.success_fill, theme.success),
        "moved": (icon.success_fill, theme.success),
        "skipped": (icon.warning, theme.warning),
        "exist": (icon.warning, theme.warning),
        "already exists": (icon.warning, theme.warning),
        "error": (icon.error, theme.error),
        "failed": (icon.error, theme.error),
    }

    FILE_TYPES = {
        "video": (
            {"mp4", "mkv", "avi", "mov", "webm", "wmv"},
            icon.video,
        ),
        "image": (
            {"png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"},
            icon.image,
        ),
        "audio": (
            {"mp3", "wav", "aac", "flac", "ogg", "m4a"},
            icon.audio,
        ),
        "document": (
            {
                "pdf", "txt", "doc", "docx", "rtf",
                "xls", "xlsx", "ppt", "pptx", "csv",
            },
            icon.document,
        ),
        "archive": (
            {"zip", "rar", "7z", "tar", "gz"},
            icon.archive,
        ),
    }

    def __init__(self, master, mode="rename", **kwargs):
        super().__init__(
            master=master,
            fg_color=theme.panel,
            corner_radius=8,
            border_width=1,
            border_color=theme.border,
            **kwargs,
        )

        self.mode = self._normalize_mode(mode)
        self.current_plan = []
        self.cards = []
        self._icon_cache = {}

        self._configure_layout()
        self._build_heading()
        self._build_table_heading()
        self._build_results()
        self._build_footer()

        self.change_view(self.mode)

    # ==================================================
    # Layout
    # ==================================================

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _build_heading(self):
        self.heading = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.heading.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(18, 0),
        )

        self.heading.grid_columnconfigure(1, weight=1)

        self.operation_icon = ctk.CTkLabel(
            self.heading,
            text="",
            width=44,
            height=44,
            fg_color=theme.background,
            corner_radius=7,
        )
        self.operation_icon.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(0, 12),
        )

        self.title_label = ctk.CTkLabel(
            self.heading,
            text="",
            text_color=theme.text_primary,
            font=(theme.font, 18, "bold"),
            anchor="w",
        )
        self.title_label.grid(
            row=0,
            column=1,
            sticky="sw",
        )

        self.description_label = ctk.CTkLabel(
            self.heading,
            text="",
            text_color=theme.text_muted,
            font=(theme.font, 12),
            anchor="w",
        )
        self.description_label.grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(3, 0),
        )

        self.count_label = ctk.CTkLabel(
            self.heading,
            text="0 files",
            text_color=theme.text_secondary,
            fg_color=theme.panel_light,
            corner_radius=14,
            font=(theme.font, 12),
            padx=12,
            pady=6,
        )
        self.count_label.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(12, 0),
        )

    def _build_table_heading(self):
        self.table_heading = ctk.CTkFrame(
            self,
            fg_color=theme.sidebar,
            corner_radius=6,
        )
        self.table_heading.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(18, 5),
        )

        self.table_heading.grid_columnconfigure(0, weight=1)
        self.table_heading.grid_columnconfigure(1, weight=1)
        self.table_heading.grid_columnconfigure(2, weight=0)

        self.column_labels = []

        for column in range(3):
            label = ctk.CTkLabel(
                self.table_heading,
                text="",
                text_color=theme.text_muted,
                font=(theme.font, 11, "bold"),
                anchor="w",
            )
            label.grid(
                row=0,
                column=column,
                sticky="ew",
                padx=12,
                pady=12,
            )
            self.column_labels.append(label)

    def _build_results(self):
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.background,
            corner_radius=0,
            scrollbar_button_color=theme.border,
            scrollbar_button_hover_color=theme.action_hover,
        )
        self.results_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(0, 5),
        )
        self.results_frame.grid_columnconfigure(0, weight=1)

    def _build_footer(self):
        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.footer.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=18,
            pady=(5, 14),
        )
        self.footer.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(
            self.footer,
            text="No items to display",
            text_color=theme.text_muted,
            font=(theme.font, 12),
            anchor="w",
        )
        self.result_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.status_label = ctk.CTkLabel(
            self.footer,
            text="Ready",
            text_color=theme.success,
            font=(theme.font, 12, "bold"),
        )
        self.status_label.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # ==================================================
    # Icons
    # ==================================================

    def _get_icon(self, name, color=None, size=18):
        """Create and cache a themed CustomTkinter icon."""
        color = color or theme.text_secondary
        key = (name, color, size)
    
        if key not in self._icon_cache:
            self._icon_cache[key] = icon_image_convert(
                icon_name=name,
                color=color,
                size=size,
            )
    
        return self._icon_cache[key]

    def _get_file_icon(self, filename):
        """Choose an icon based on the file extension."""
        filename = str(filename).replace("\\", "/")
        extension = filename.rsplit("/", 1)[-1]

        if "." not in extension:
            return icon.document

        extension = extension.rsplit(".", 1)[-1].lower()

        for extensions, icon_name in self.FILE_TYPES.values():
            if extension in extensions:
                return icon_name

        return icon.document

    def _get_status_config(self, status):
        """Return the icon and color for a result status."""
        key = str(status).strip().lower()

        return self.STATUS_CONFIG.get(
            key,
            (icon.info, theme.text_muted),
        )

    # ==================================================
    # Mode switching
    # ==================================================

    @staticmethod
    def _normalize_mode(mode):
        mode = str(mode).strip().lower()

        return mode if mode in View.MODE_CONFIG else "rename"

    def change_view(self, mode):
        """Update the view heading and columns for the selected tool."""
        self.mode = self._normalize_mode(mode)
        config = self.MODE_CONFIG[self.mode]

        self.operation_icon.configure(
            image=self._get_icon(
                config["icon"],
                theme.action_hover,
                22,
            )
        )

        self.title_label.configure(text=config["title"])
        self.description_label.configure(
            text=config["description"]
        )

        for label, text in zip(
            self.column_labels,
            config["columns"],
        ):
            label.configure(text=text.upper())

        self.clear_cards()
        self.show_empty()
        self.set_status("Ready", theme.success)

    # ==================================================
    # Preview and results
    # ==================================================

    def display_card(self, plan):
        """Display a plan supplied by the controller."""
        if isinstance(plan, dict):
            if isinstance(plan.get("plan"), (list, tuple)):
                plan = plan["plan"]
            elif isinstance(plan.get("results"), (list, tuple)):
                plan = plan["results"]
            elif self._is_result_item(plan):
                plan = [plan]
            else:
                plan = []

        if not isinstance(plan, (list, tuple)):
            self.show_empty("The preview data has an unsupported format.")
            return

        self.clear_cards()
        self.current_plan = list(plan)

        if not self.current_plan:
            self.show_empty()
            return

        for item in self.current_plan:
            if not isinstance(item, dict):
                item = {
                    "source": str(item),
                    "destination": "",
                    "status": "Ready",
                }

            self._create_result_row(item)

        count = len(self.current_plan)

        self.count_label.configure(text=f"{count} files")
        self.result_label.configure(
            text=f"Showing {count} items"
        )

    @staticmethod
    def _is_result_item(item):
        return any(
            key in item
            for key in (
                "source",
                "destination",
                "old_name",
                "new_name",
                "name",
                "path",
                "status",
            )
        )

    @staticmethod
    def _get_source(item):
        return str(
            item.get("old_name")
            or item.get("source")
            or item.get("path")
            or item.get("name")
            or item.get("file")
            or "Unknown file"
        )

    @staticmethod
    def _get_destination(item):
        return str(
            item.get("new_name")
            or item.get("destination")
            or item.get("target")
            or ""
        )

    def _create_result_row(self, item):
        source = self._get_source(item)
        destination = self._get_destination(item)
        status = str(item.get("status", "Ready"))

        row = ctk.CTkFrame(
            self.results_frame,
            fg_color=theme.panel,
            corner_radius=6,
            border_width=1,
            border_color=theme.border,
        )
        row.pack(fill="x", pady=3)

        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(3, weight=1)

        # File icon
        file_icon = ctk.CTkLabel(
            row,
            text="",
            image=self._get_icon(
                self._get_file_icon(source),
                theme.action_hover,
                18,
            ),
        )
        file_icon.grid(
            row=0,
            column=0,
            padx=(12, 8),
            pady=13,
        )

        # Source name
        source_label = ctk.CTkLabel(
            row,
            text=source,
            text_color=theme.text_primary,
            font=(theme.font, 12),
            anchor="w",
        )
        source_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 8),
            pady=13,
        )

        # Destination
        destination_label = ctk.CTkLabel(
            row,
            text=destination or "—",
            text_color=theme.text_secondary,
            font=(theme.font, 12),
            anchor="w",
        )
        destination_label.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=8,
            pady=13,
        )

        # Status icon and text
        status_icon, status_color = self._get_status_config(status)

        status_frame = ctk.CTkFrame(
            row,
            fg_color="transparent",
        )
        status_frame.grid(
            row=0,
            column=3,
            sticky="e",
            padx=(8, 12),
            pady=8,
        )

        ctk.CTkLabel(
            status_frame,
            text="",
            image=self._get_icon(
                status_icon,
                status_color,
                15,
            ),
        ).pack(side="left", padx=(0, 5))

        ctk.CTkLabel(
            status_frame,
            text=status,
            text_color=status_color,
            font=(theme.font, 11, "bold"),
        ).pack(side="left")

        self.cards.append(row)

    # ==================================================
    # Empty state and status
    # ==================================================

    def clear_cards(self):
        """Remove existing result rows."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.cards.clear()
        self.current_plan = []
        self.count_label.configure(text="0 files")

    def show_empty(self, message=None):
        """Display a helpful message when no results are available."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.cards.clear()
        self.current_plan = []
        self.count_label.configure(text="0 files")

        empty_frame = ctk.CTkFrame(
            self.results_frame,
            fg_color="transparent",
        )
        empty_frame.pack(
            fill="both",
            expand=True,
            pady=45,
        )

        ctk.CTkLabel(
            empty_frame,
            text="",
            image=self._get_icon(
                icon.info,
                theme.text_muted,
                32,
            ),
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            empty_frame,
            text=message or self.MODE_CONFIG[self.mode]["empty"],
            text_color=theme.text_muted,
            font=(theme.font, 13),
            wraplength=360,
            justify="center",
        ).pack(padx=20)

        self.result_label.configure(text="No items to display")

    def set_status(self, text, color=None):
        """Update the view's status indicator."""
        self.status_label.configure(
            text=str(text),
            text_color=color or theme.text_muted,
        )
