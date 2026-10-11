# main_windows.py
import customtkinter as ctk
import config.theme as theme
import config.icon as icon

from utils.file_utils       import icon_image_convert
from frontend.wigets.view   import View
from frontend.wigets.dialog import Dialog
from frontend.wigets.form   import Form
from frontend.wigets.status import Status
from frontend.wigets.title  import Title


class MainWindow(ctk.CTk):
    def __init__(self, on_folder, on_preview, on_rename, on_organize, on_copy, on_move, on_search, on_result):
        super().__init__(fg_color=theme.background)

        self.on_folder    = on_folder
        self.on_preview   = on_preview
        self.on_rename    = on_rename
        self.on_organize  = on_organize
        self.on_copy      = on_copy    
        self.on_move      = on_move    
        self.on_search    = on_search  
        self.on_result    = on_result

        self.current_mode = "rename"

        self.title("File & Folder Manager")
        self.geometry("1500x900")
        self.minsize(1100, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_layout()
        self.create_frame()
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_footer()

    # =============================================================
    # LAYOUT
    # =============================================================

    def create_layout(self):
        self.grid_rowconfigure(0, weight=0)   # Header
        self.grid_rowconfigure(1, weight=1)   # Body
        self.grid_rowconfigure(2, weight=0)   # Footer

        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main
        self.grid_propagate(False)

    def create_frame(self):
        # Header
        self.header_frame = ctk.CTkFrame(
            self,
            height=75,
            corner_radius=0,
            fg_color=theme.header,
            border_width=1,
            border_color=theme.border,
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="news")
        self.header_frame.grid_propagate(False)

        # Sidebar
        self.side_bar_frame = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=theme.sidebar,
            border_width=1,
            border_color=theme.border,
        )
        self.side_bar_frame.grid(row=1, column=0, sticky="news")
        self.side_bar_frame.grid_propagate(False)

        # Main content
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=theme.background,
        )
        self.main_frame.grid(row=1, column=1, sticky="news")

        # Footer
        self.footer_frame = ctk.CTkFrame(
            self,
            height=55,
            corner_radius=0,
            fg_color=theme.header,
            border_width=1,
            border_color=theme.border,
        )
        self.footer_frame.grid(row=2, column=0, columnspan=2, sticky="news")
        self.footer_frame.grid_propagate(False)

    # =============================================================
    # HEADER
    # =============================================================

    def create_header(self):
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)

        ctk_icon = icon_image_convert(
            icon.organize_fill,
            theme.action_hover,
            30,
        )

        self.header_title_label = ctk.CTkLabel(
            self.header_frame,
            image=ctk_icon,
            text=" File & Folder Manager",
            anchor="w",
            compound="left",
            font=("Roboto", 24, "bold"),
            text_color=theme.text_primary,
        )
        self.header_title_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=17,
            sticky="ew",
        )

        self.header_status_label = ctk.CTkLabel(
            self.header_frame,
            text="● Ready",
            font=("Roboto", 14, "bold"),
            text_color=theme.text_secondary,
        )
        self.header_status_label.grid(
            row=0,
            column=1,
            padx=25,
            pady=17,
            sticky="e",
        )

    # =============================================================
    # SIDEBAR
    # =============================================================

    def create_sidebar(self):
        self.side_bar_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self.side_bar_frame,
            text="FILE TOOLS",
            font=("Roboto", 13, "bold"),
            anchor="w",
            text_color=theme.text_muted,
        )
        title_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=(28, 12),
            sticky="ew",
        )

        self.rename_btn = self.create_button(
            self.side_bar_frame, icon.rename_fill, "Rename",
            lambda: self.change_tool("rename"), 1, True
        )
        self.organize_btn = self.create_button(
            self.side_bar_frame, icon.organize_fill, "Organize",
            lambda: self.change_tool("organize"), 2
        )
        self.move_btn = self.create_button(
            self.side_bar_frame, icon.move, "Move",
            lambda: self.change_tool("move"), 3
        )
        self.copy_btn = self.create_button(
            self.side_bar_frame, icon.copy, "Copy",
            lambda: self.change_tool("copy"), 4
        )
        self.search_btn = self.create_button(
            self.side_bar_frame, icon.search, "Search",
            lambda: self.change_tool("search"), 5
        )

    def change_tool(self, current_mode):
        self.current_mode = current_mode

        modes = {
            "rename"  : self.rename_btn,
            "organize": self.organize_btn,
            "move"    : self.move_btn,
            "copy"    : self.copy_btn,
            "search"  : self.search_btn,
        }

        for mode, button in modes.items():
            if mode == current_mode:
                button.configure(
                    fg_color=theme.action,
                    hover_color=theme.action_hover,
                )
            else:
                button.configure(
                    fg_color=theme.transparent,
                    hover_color=theme.action_disable_hover,
                )

        self.m_title.change_title(current_mode)
        self.form.change_form(current_mode)
        self.view.change_view(current_mode)
        self.status.change_status(current_mode)

    def create_button(self, parent, icon_name, text, command, row, active=False):
        fg_color = theme.action if active else theme.transparent
        hover_color = theme.action_hover if active else theme.action_disable_hover

        ctk_icon = icon_image_convert(icon_name, theme.action_hover, 30)

        button = ctk.CTkButton(
            master        = parent,
            text          = text,
            image         = ctk_icon,
            font          = ("Roboto", 16),
            anchor        = "w",
            height        = 58,
            corner_radius = 8,
            command       = command,
            fg_color      = fg_color,
            text_color    = theme.text_primary,
            hover_color   = hover_color,
        )
        button.grid(row=row, column=0, padx=12, pady=4, sticky="ew")
        return button

    # =============================================================
    # MAIN CONTENT
    # =============================================================

    def create_main_content(self):
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=5, uniform="content")
        self.main_frame.grid_columnconfigure(1, weight=6, uniform="content")
        self.main_frame.grid_columnconfigure(2, weight=3, uniform="content")

        self.m_title = Title(self.main_frame)
        self.m_title.grid(row=0, column=0, columnspan=2, padx=(18, 10), pady=(20, 8), sticky="news",
        )

        # Form/settings panel
        self.form = Form(
            master      = self.main_frame,
            on_preview  = self.preview_rename,
            on_rename   = self.confirmed_rename,
            on_organize = None,
            on_copy     = None,
            on_move     = None,
            on_search   = None)

        self.source_file = self.form.source_file
        
        
        self.form.grid(row=1, column=0, padx=(18, 8), pady=(8, 20), sticky="news")
        self.form.grid_propagate(False)

        # Preview panel
        self.view = View(self.main_frame)
        self.view.grid(row=1, column=1, padx=8, pady=(8, 20), sticky="news")

        # Status / summary panel
        self.status = Status(self.main_frame)
        self.status.grid(row=0, rowspan=2, column=2, padx=(8, 18), pady=(20, 20), sticky="news")

    # =============================================================
    # FOOTER
    # =============================================================

    def create_footer(self):
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)

        self.status_label   = self.create_status_label("● Ready", "left")
        self.status_total   = self.create_status_label("Total : 0", "right")
        self.status_renamed = self.create_status_label("Renamed : 0", "right")
        self.status_skipped = self.create_status_label("Skipped : 0", "right")
        self.status_failed  = self.create_status_label("Failed : 0", "right")

    def create_status_label(self, text, side="left"):
        label = ctk.CTkLabel(
            self.footer_frame,
            text=text,
            font=("Roboto", 14, "bold"),
            text_color=theme.text_primary,
        )

        if side == "left":
            label.grid(row=0, column=0, padx=25, pady=10, sticky="w")
        else:
            label.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="e")

        return label

    # =============================================================
    # RENAME WORKFLOW 
    # =============================================================

    def preview_rename(self):
        file_path = self.source_file.get_folder_path()
        form_data = self.form.call_back()

        if form_data is None:
            return

        if file_path is None:
            return

        pattern, extension, quality, start_number, number_format = form_data

        self.on_folder(
            file_path,
            extension,
            pattern,
            quality,
            start_number,
            number_format,
        )
        self.on_preview()

    def confirmed_rename(self):
        file_path = self.source_file.get_folder_path()
        form_data = self.form.call_back()

        if form_data is None or file_path is None:
            return

        dialog = Dialog(self)
        self.wait_window(dialog)

        if dialog.get_result():
            rename_plan = self.on_rename()
            if not rename_plan:
                return

            self.on_result(rename_plan)

    # =============================================================
    # DISPLAY
    # =============================================================

    def show_preview(self, rename_plan):
        self.view.display_card(rename_plan)

    def show_status(self, file, status, data, extension):
        extension = extension.replace(".", "").capitalize()

        if status == "renamed":
            self.status_label.configure(
                text="● Success",
                text_color=theme.success,
            )

        elif status == "empty":
            self.status_label.configure(
                text=f"● No {extension} Files Found",
                text_color=theme.error,
            )

        elif status == "skipped":
            self.status_label.configure(
                text="● No Files Renamed",
                text_color=theme.error,
            )

        elif status == "error":
            self.status_label.configure(
                text=f"{data}",
                text_color=theme.error,
            )
            self.status_failed.configure(text=f"Failed : {file-data}")

        else:
            return

        self.status_total.configure(text=f"Total : {file}")
        self.status_renamed.configure(text=f"Renamed : {data}")
        self.status_skipped.configure(text=f"Skipped : {file-data}")
