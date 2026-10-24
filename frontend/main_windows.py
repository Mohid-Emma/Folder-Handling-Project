# main_windows.py
import customtkinter as ctk
import config.theme  as theme
import config.icon   as icon
from   typing import Callable
from   utils  import icon_image_convert

class MainWindow(ctk.CTk):
    def __init__(self, ui_compounds: dict, operation: dict) -> None:
        super().__init__(fg_color=theme.background)

        self.ui_compounds     = ui_compounds
        self.operation        = operation
        self.current_mode     = "rename"
        self.current_callback = None



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

    def create_layout(self) -> None:
        self.grid_rowconfigure(0, weight=0)   # Header
        self.grid_rowconfigure(1, weight=1)   # Body
        self.grid_rowconfigure(2, weight=0)   # Footer

        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main
        self.grid_propagate(False)

    def create_frame(self) -> None:
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

    def create_header(self) -> None:
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
        self.header_title_label.grid(row=0, column=0, padx=25, pady=17, sticky="ew" )

        self.header_status_label = ctk.CTkLabel(
            self.header_frame,
            text="● Ready",
            font=("Roboto", 14, "bold"),
            text_color=theme.text_secondary,
        )
        self.header_status_label.grid(row=0, column=1, padx=25, pady=17, sticky="e" )

    # =============================================================
    # SIDEBAR
    # =============================================================

    def create_sidebar(self) -> None:
        self.side_bar_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self.side_bar_frame,
            text="FILE TOOLS",
            font=("Roboto", 13, "bold"),
            anchor="w",
            text_color=theme.text_muted,
        )
        title_label.grid(row=0, column=0, padx=25, pady=(28, 12), sticky="ew" )

        self.rename_btn = self.create_button(
            self.side_bar_frame, icon.rename_fill, "Rename",
            lambda: self.change_tool("rename"), 1, True
        )
        self.organize_btn = self.create_button(
            self.side_bar_frame, icon.organize_fill, "Organize",
            lambda: self.change_tool("organize"), 2
        )
        self.copy_btn = self.create_button(
            self.side_bar_frame, icon.copy, "Copy",
            lambda: self.change_tool("copy"), 3
        )
        self.move_btn = self.create_button(
            self.side_bar_frame, icon.move, "Move",
            lambda: self.change_tool("move"), 4
        )
        self.search_btn = self.create_button(
            self.side_bar_frame, icon.search, "Search",
            lambda: self.change_tool("search"), 5
        )

    def change_tool(self, current_mode: str) -> None:
        self.current_mode = current_mode

        modes = {
            "rename"  : self.rename_btn,
            "organize": self.organize_btn,
            "copy"    : self.copy_btn,
            "move"    : self.move_btn,
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
    
        self.current_callback = None

    def create_button(self, parent: ctk.CTkFrame, icon_name: str, text: str, command: Callable[[str], None], row: int, active: bool=False) -> ctk.CTkButton:
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

    def create_main_content(self) -> None:
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=5, uniform="content")
        self.main_frame.grid_columnconfigure(1, weight=6, uniform="content")
        self.main_frame.grid_columnconfigure(2, weight=3, uniform="content")

        self.m_title = self.ui_compounds["title"](self.main_frame)
        self.m_title.grid(row=0, column=0, columnspan=2, padx=(18, 10), pady=(20, 8), sticky="news")

        # Form/settings panel
        form_operation = {
            "rename_preview"   : lambda: self.preview("rename"),
            "rename_execute"   : lambda: self.execute("rename"),
            "organize_preview" : lambda: self.preview("organize"),
            "organize_execute" : lambda: self.execute("organize"),
            "copy_preview"     : lambda: self.preview("copy"),
            "copy_execute"     : lambda: self.execute("copy"),
            "move_preview"     : lambda: self.preview("move"),
            "move_execute"     : lambda: self.execute("move"),
            "run_search"       : lambda: self.preview("search"),}
        
        self.form = self.ui_compounds["form"](self.main_frame, form_operation)

        self.source_file = self.form.source_file
        
        
        self.form.grid(row=1, column=0, padx=(18, 8), pady=(8, 20), sticky="news")
        self.form.grid_propagate(False)

        # Preview panel
        self.view = self.ui_compounds["view"](self.main_frame)
        self.view.grid(row=1, column=1, padx=8, pady=(8, 20), sticky="news")

        # Status / summary panel
        self.status = self.ui_compounds["status"](self.main_frame)
        self.status.grid(row=0, rowspan=2, column=2, padx=(8, 18), pady=(20, 20), sticky="news")

    # =============================================================
    # FOOTER
    # =============================================================

    def create_footer(self) -> None:
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)

    # =============================================================
    # Preview Workfolw 
    # =============================================================

    def preview(self, current_mode: str) -> None:
        self.current_callback = None

        mode = {
            "rename"  : self.form.call_back_rename,
            "organize": self.form.call_back_organize,
            "copy"    : self.form.call_back_copy,
            "move"    : self.form.call_back_move,
            "search"  : self.form.call_back_search,
                }
        for operation, form in mode.items():
            if operation == current_mode:
                self.current_callback = form()

        if self.current_callback is None:
            return
        
        self.operation[f"{current_mode}_preview"](self.current_callback)

    # =============================================================
    # Execute Workfolw 
    # =============================================================

    def execute(self, current_mode: str) -> None:
        
        if self.current_callback is None:
            return
        
        plan = self.operation[f"{current_mode}_execute"]()
        if not plan:
            return
        
        self.operation["result"](plan)

    # =============================================================
    # Display
    # =============================================================

    def show_preview(self, plan: str) -> None:
        self.view.display_card(plan)
