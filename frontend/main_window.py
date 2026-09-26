# main_windows.py
import customtkinter          as     ctk
import config.theme           as     theme
from   frontend.source_file          import SourceFile
from   frontend.rename.rename_view   import RenameView
from   frontend.rename.rename_dialog import RenameDialog
from   frontend.rename.rename_form   import RenameForm



class MainWindow(ctk.CTk):

    def __init__(self, on_folder_selected, on_preview, on_rename, on_result):
        super().__init__(fg_color=theme.background)

        self.on_folder_selected = on_folder_selected
        self.on_preview         = on_preview
        self.on_rename          = on_rename
        self.on_result          = on_result

        self.current_tool       = "rename"


        self.title("File & Folder Manager")
        self.geometry("1500x800")
        self.minsize(900, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_layout()
        self.create_frame()

        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_footer()


    def create_layout(self):

        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Main Body
        self.grid_rowconfigure(2, weight=0) # Footer

        self.grid_columnconfigure(0, weight=0) # SideBar
        self.grid_columnconfigure(1, weight=1) # Main Content

    def create_frame(self):

        self.header_frame = ctk.CTkFrame(
            master        = self, 
            height        = 75, 
            corner_radius = 0,
            fg_color      = theme.panel)
        
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="news")
        self.header_frame.grid_propagate(False)

        self.side_bar_frame = ctk.CTkFrame(
            master        = self, 
            width         = 230, 
            corner_radius = 0,
            fg_color      = theme.sidebar)
        self.side_bar_frame.grid(row=1, column=0, sticky="news")
        self.side_bar_frame.grid_propagate(False)

        self.main_frame = ctk.CTkFrame(
            master        = self, 
            corner_radius = 10,
            fg_color      = theme.panel)
        self.main_frame.grid(row=1, column=1, padx=15, pady=15, sticky="news")

        self.footer_frame = ctk.CTkFrame(
            master        = self, 
            height        = 40, 
            corner_radius = 0,
            fg_color      = theme.panel)

        self.footer_frame.grid(row=2, column=0, columnspan=2, sticky="news")
        self.footer_frame.grid_propagate(False)

    def create_header(self):

        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_title_label = ctk.CTkLabel(
            master     = self.header_frame, 
            text       = "📁 File & Folder Manager", 
            font       = ("Segoe UI", 24, "bold"),
            text_color = theme.text_primary)
        
        self.header_title_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

        self.header_status_label = ctk.CTkLabel(
            master = self.header_frame,
            text   = "● Ready",
            font   = ("Segoe UI", 14, "bold"),
            text_color = theme.text_secondary)
        
        self.header_status_label.grid(row=0, column=1, padx=25, sticky="e")

    def create_sidebar(self):
        self.side_bar_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            master     = self.side_bar_frame, 
            text       = "📁 File & Folder Manager", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        title_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

        highlight_label = ctk.CTkLabel(
            master     = self.side_bar_frame, 
            text       = "FILE TOOLS",
            font       = ("Segoe UI", 13, "bold"),
            text_color = theme.text_secondary)

        highlight_label.grid(row=1, column=0, padx=25, pady=10, sticky="w")

        self.rename_btn   = self.create_button(self.side_bar_frame, "▣ Rename",   None, 2, True)
        self.organize_btn = self.create_button(self.side_bar_frame, "▣ Organize", None, 3)
        self.move_btn     = self.create_button(self.side_bar_frame, "▣ Move",     None, 4)
        self.copy_btn     = self.create_button(self.side_bar_frame, "▣ Copy",     None, 5)
        self.search_btn   = self.create_button(self.side_bar_frame, "▣ Search",   None, 6)
        
    def create_button(self, parent, text, command, row, active=False):
        if active:
            fg_color    = theme.action
            hover_color = theme.action_hover
        else:
            fg_color    = theme.action_disable
            hover_color = theme.action_disable_hover
        button = ctk.CTkButton(
            master      = parent,
            text        = text,
            font        = ("Segoe UI", 10, "bold"),
            command     = command,
            fg_color    = fg_color,
            text_color  = theme.text_primary,
            hover_color = hover_color)
        
        button.grid(row=row, column=0, padx=15, pady=(15,5), sticky="ew")
        return button

    def create_main_content(self):
        
        self.main_frame.grid_rowconfigure(0, weight=0) # Title
        self.main_frame.grid_rowconfigure(1, weight=0) # Select Folder/File
        self.main_frame.grid_rowconfigure(2, weight=2) # Setting / Preview
        
        self.main_frame.grid_columnconfigure(0, weight=1) # Setting
        self.main_frame.grid_columnconfigure(1, weight=2) # Preview

        title_frame = ctk.CTkFrame(
            master   = self.main_frame, 
            fg_color = theme.transparent)
        
        title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="news")
        title_frame.grid_columnconfigure(0, weight=1)

        self.main_content_title = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Bulk Rename", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)
        
        self.main_content_title.grid(row=0, column=0 ,padx=25, pady=5, sticky="w")

        self.main_content_discription = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Rename Multiply Files Quickly", 
            font       = ("Segoe UI", 13, "bold"),
            text_color = theme.text_secondary)
        
        self.main_content_discription.grid(row=1, column=0 ,padx=25, pady=5, sticky="w")

        self.source_file = SourceFile(self.main_frame)
        self.source_file.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="news")


        self.rename_form = RenameForm(self.main_frame)
        self.rename_form.grid(row=2, column=0, padx=20, pady=20, sticky="news")
        self.rename_form.grid_propagate(False)


        self.display_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        #self.display_frame.grid(row=0, column=1, sticky="news")

        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            master     = self.display_frame, 
            text       = "Display Status", 
            font       = ("Segoe UI", 24, "bold"))
        
        self.title_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

        self.rename_view = RenameView(self.display_frame)
        self.rename_view.grid(row=1, column=0, padx=20, pady=20, sticky="news")

    def create_footer(self):
        self.status_label = ctk.CTkLabel(
            master = self.footer_frame,
            text   = "● Ready",
            font   = ("Segoe UI", 14, "bold"))
        self.status_label.pack(pady=10)


    def preview_rename(self):
        self.on_preview()

    def show_preview(self, rename_plan):
        self.rename_view.display_card(rename_plan)

    def confirmed_rename(self):
        dialog = RenameDialog(self)
        self.wait_window(dialog)
        
        if dialog.get_result():
            rename_plan = self.on_rename()
            self.on_result(rename_plan)

    def show_status(self, status, data):
        if status == "renamed":
            self.status_label.configure(
                text       = f"● {data} files renamed successfully",
                text_color = theme.success)
            
        elif status == "empty":
            self.status_label.configure(
                text       = "● No MP4 files found",
                text_color = theme.error)
            
        elif status == "skipped":
            self.status_label.configure(
                text       = "● No files renamed",
                text_color = theme.error)
        elif status == "error":
            self.status_label.configure(
                text       = f"{data}",
                text_color = theme.error)
            



                




