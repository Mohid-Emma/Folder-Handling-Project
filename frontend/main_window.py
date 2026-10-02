# main_windows.py
import customtkinter          as     ctk
import config.theme           as     theme
from   frontend.source_file          import SourceFile
from   frontend.rename.rename_view   import RenameView
from   frontend.rename.rename_dialog import RenameDialog
from   frontend.rename.rename_form   import RenameForm



class MainWindow(ctk.CTk):

    def __init__(self, on_folder, on_preview, on_rename, on_result):
        super().__init__(fg_color=theme.background)

        self.on_folder  = on_folder
        self.on_preview = on_preview
        self.on_rename  = on_rename
        self.on_result  = on_result

        self.current_tool  = "rename"


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

    # Create Layout 
    def create_layout(self):

        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Main Body
        self.grid_rowconfigure(2, weight=0) # Footer

        self.grid_columnconfigure(0, weight=0) # SideBar
        self.grid_columnconfigure(1, weight=1) # Main Content

    # Create Frame
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

    # Create Header
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

    # Create SideBar
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
        
    # Create Button
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
            font        = ("Segoe UI", 12, "bold"),
            command     = command,
            fg_color    = fg_color,
            text_color  = theme.text_primary,
            hover_color = hover_color)
        
        button.grid(row=row, column=0, padx=15, pady=(15,5), sticky="ew")
        return button

    # Create Main Content
    def create_main_content(self):
        
        self.main_frame.grid_rowconfigure(0, weight=0) # Title
        self.main_frame.grid_rowconfigure(1, weight=0) # Select Folder/File
        self.main_frame.grid_rowconfigure(2, weight=2) # Setting / Preview
        
        self.main_frame.grid_columnconfigure(0, weight=0) # Rename Form
        self.main_frame.grid_columnconfigure(1, weight=2) # Rename View 

        # Create Title For Main Contain

        title_frame = ctk.CTkFrame(
            master   = self.main_frame, 
            fg_color = theme.transparent)
        
        title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10,5), sticky="news")
        title_frame.grid_columnconfigure(0, weight=1)

        self.main_content_title = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Bulk Rename", 
            font       = ("Segoe UI", 18, "bold"),
            text_color = theme.text_primary)
        
        self.main_content_title.grid(row=0, column=0 ,padx=25, pady=5, sticky="w")

        self.main_content_discription = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Rename Multiply Files Quickly", 
            font       = ("Segoe UI", 13, "bold"),
            text_color = theme.text_secondary)
        
        self.main_content_discription.grid(row=1, column=0 ,padx=25, pady=5, sticky="w")

        # Create Source File

        self.source_file = SourceFile(self.main_frame)
        self.source_file.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="news")

        # Create Rename Form

        self.rename_form = RenameForm(
            master                 = self.main_frame, 
            on_preview_information = self.preview_rename,
            on_rename              = self.confirmed_rename)
        
        self.rename_form.grid(row=2, column=0, padx=20, pady=20, sticky="news")
        self.rename_form.grid_propagate(False)

        # Create Rename Preview

        self.rename_view = RenameView(self.main_frame)
        self.rename_view.grid(row=2, column=1, padx=20, pady=20, sticky="news")

    # Create Footer
    def create_footer(self):

        self.footer_frame.grid_rowconfigure(0, weight=1)

        self.status_label   = self.create_status_label("● Ready", (20,150))
        self.status_total   = self.create_status_label("Total : 0")
        self.status_renamed = self.create_status_label("Renamed : 0")
        self.status_skipped = self.create_status_label("Skipped : 0")
        self.status_failed  = self.create_status_label("Failed : 0")

    def create_status_label(self, text, padx = (20,180)):

        status_label = ctk.CTkLabel(
            master     = self.footer_frame,
            text       = text,
            font       = ("Segoe UI", 14, "bold"),
            text_color = theme.text_primary)
        
        status_label.pack(padx=padx, pady=10, side="left", expand=True)
        return status_label


    # Create Preview For Rename Files
    def preview_rename(self):
        file_path = self.source_file.get_folder_path()
        form_data = self.rename_form.call_back()
        if form_data is None:
            return
        if file_path is None:
            return
        pattern, extension, quality, start_number, number_foramt = form_data

        self.on_folder(file_path, extension, pattern, quality, start_number, number_foramt)
        self.on_preview()

    # Confirmed Rename Files
    def confirmed_rename(self):
        file_path = self.source_file.get_folder_path()
        form_data = self.rename_form.call_back()
        if form_data is None and file_path is None:
            return

        dialog = RenameDialog(self)
        self.wait_window(dialog)
        if dialog.get_result():
            rename_plan = self.on_rename()
            if not rename_plan:
                return

            self.on_result(rename_plan)

    # Show Preview For Rename Files
    def show_preview(self, rename_plan):
        self.rename_view.display_card(rename_plan)

    # Show Status of the Final Result
    def show_status(self, file,  status, data, extension):

        extension = extension.replace(".", "").capitalize()

        if status == "renamed":
            self.status_label.configure(
                text       = f"● Success",
                text_color = theme.success)
            
        elif status == "empty":
            self.status_label.configure(
                text       = f"● No {extension} Files Found",
                text_color = theme.error)
            
        elif status == "skipped":
            self.status_label.configure(
                text       = "● No Files Renamed",
                text_color = theme.error)
        elif status == "error":
            self.status_label.configure(
                text       = f"{data}",
                text_color = theme.error)
            self.status_failed.configure(f"Failed : {file-data}")
        else:
            return
        
        self.status_total.configure(text = f"Total : {file}")
        self.status_renamed.configure(text = f"Renamed : {data}")
        self.status_skipped.configure(text = f"Skipped : {file-data}")