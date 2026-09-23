# main_windows.py
import customtkinter          as     ctk
import config.theme           as     theme
from   tkinter                import filedialog
from   frontend.rename_view   import RenameView
from   frontend.rename_dialog import RenameDialog


class MainWindow(ctk.CTk):

    def __init__(self, on_folder_selected, on_preview, on_rename, on_result):
        super().__init__()

        self.on_folder_selected = on_folder_selected
        self.on_preview         = on_preview
        self.on_rename          = on_rename
        self.on_result          = on_result


        self.title("File & Folder Manger")
        self.geometry("1200x800")
        self.minsize(900, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_layout()
        self.create_frame()

        self.create_header()
        self.create_sidebar()
        self.create_form_panel()
        self.create_folder_panel()
        self.create_footer()



    def create_layout(self):

        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Main Body
        self.grid_rowconfigure(2, weight=0) # Footer

        self.grid_columnconfigure(0, weight=0) # SideBar
        self.grid_columnconfigure(1, weight=1) # Main Content

    def create_frame(self):

        self.header_frame = ctk.CTkFrame(self, height=75, corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="news")
        self.header_frame.grid_propagate(False)

        self.side_bar_frame = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.side_bar_frame.grid(row=1, column=0, sticky="news")
        self.side_bar_frame.grid_propagate(False)

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=1, column=1, padx=15, pady=15, sticky="news")

        self.footer_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, columnspan=2, sticky="news")
        self.footer_frame.grid_propagate(False)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=3)

    def create_header(self):

        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            master     = self.header_frame, 
            text       = "📚 File & Folder Management System", 
            font       = ("Segoe UI", 24, "bold"))
        
        self.title_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

        self.header_status = ctk.CTkLabel(
            master     = self.header_frame, 
            text       = "File & Folder Manger", 
            font       = ("Segoe UI", 12))
        
        self.header_status.grid(row=0, column=1, padx=25, sticky="e")

    def create_sidebar(self):
        pass

    def create_form_panel(self):

        self.interact_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.interact_frame.grid(row=0, column=0, sticky="news")
        #self.interact_frame.grid_propagate(False)


        #self.interact_frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.interact_frame.grid_columnconfigure((0,1,2), weight=1)

        self.title_label = ctk.CTkLabel(
            master     = self.interact_frame, 
            text       = "📚 Rename File & Folder System", 
            font       = ("Segoe UI", 20, "bold"))

        self.title_label.grid(row=0, column=0, columnspan=3, padx=25, pady=10, sticky="w")

        folder_frame = ctk.CTkFrame(self.interact_frame)
        folder_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        folder_frame.grid_columnconfigure(0,weight=1)

        self.folder_entry = ctk.CTkEntry(
            master           = folder_frame,
            placeholder_text = "Select a Folder",
            font             = ("Segoe UI", 12, "bold"))
        
        self.folder_entry.grid(row=0, column=0, padx=(20,0), pady=(15,5), sticky="ew")

        self.browse_button = ctk.CTkButton(
            master  = folder_frame,
            text    = "Browse",
            font    = ("Segoe UI", 12, "bold"),
            command = self.browse_folder)
        
        self.browse_button.grid(row=0, column=1, padx=15, pady=(15,5), sticky="ew")

        self.preview_button = ctk.CTkButton(
            master  = self.interact_frame,
            text    = "Preview",
            font    = ("Segoe UI", 12, "bold"),
            command = self.preview_rename)
                
        self.preview_button.grid(row=3, column=0, padx=15, pady=(15,5), sticky="ew")

        self.rename_button = ctk.CTkButton(
            master  = self.interact_frame,
            text    = "Rename",
            font    = ("Segoe UI", 12, "bold"),
            command = self.confirmed_rename)
        
        self.rename_button.grid(row=3, column=2, padx=15, pady=(15,5), sticky="ew")

    def create_folder_panel(self):
        self.display_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.display_frame.grid(row=0, column=1, sticky="news")

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

    def browse_folder(self):
        folder = filedialog.askdirectory()
        
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.on_folder_selected(folder)

    def preview_rename(self):
        self.on_preview()

    def show_preview(self, rename_plan):
        self.rename_view.display_card(rename_plan)

    def confirmed_rename(self):
        dialog = RenameDialog(self)
        self.wait_window(dialog)
        if dialog.get_result():
            self.on_rename()
            self.on_result()

    def show_status(self, status, data):
        if status == "renamed":
            self.status_label.configure(
                text       = f"● {data} files renamed successfully",
                text_color = theme.success)
            
        elif status == "empty":
            self.status_label.configure(
                text       = "● No MP4 files found",
                text_color = theme.danger)
            
        elif status == "skipped":
            self.status_label.configure(
                text       = "● No files renamed",
                text_color = theme.danger)
        elif status == "error":
            self.status_label.configure(
                text       = f"{data}",
                text_color = theme.danger)
            



                




