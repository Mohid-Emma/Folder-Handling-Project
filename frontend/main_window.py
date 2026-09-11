# main_windows.py
import customtkinter          as     ctk
import config.theme           as     theme
from   tkinter                import filedialog
from   frontend.rename_view   import RenameView
from   frontend.rename_dialog import RenameDialog


class MainWindow(ctk.CTk):

    def __init__(self, on_folder_selected, on_preview, on_rename):
        super().__init__()

        self.on_folder_selected = on_folder_selected
        self.on_preview         = on_preview
        self.on_rename          = on_rename

        self.title("File & Folder Manger")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_window()
        self.create_folder()
        self.create_button()

        self.rename_view = RenameView(self.main_frame)
        self.rename_view.pack(fill="both", expand=True, padx=20, pady=20)

        self.status_label = ctk.CTkLabel(
            master = self.main_frame,
            text   = "● Ready",
            font   = ("Segoe UI", 14, "bold"))
        self.status_label.pack(pady=10)

    def main_window(self):
        self.main_frame = ctk.CTkFrame(
            master = self)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.title_label = ctk.CTkLabel(
            master = self.main_frame,
            text   = "Bulk Rename",
            font   = ("Segoe UI", 28, "bold"))
        
        self.title_label.pack(pady=20)

        self.description_label = ctk.CTkLabel(
            master = self.main_frame,
            text   = "Rename multiple files quickly",
            font   = ("Segoe UI", 16))
        self.description_label.pack()

    def create_folder(self):

        self.folder_frame = ctk.CTkFrame(
            master = self.main_frame)
        self.folder_frame.pack(fill="x", padx=20, pady=20)

        self.folder_label = ctk.CTkLabel(
            master = self.folder_frame,
            text   = "Folder",
            font   = ("Segoe UI", 17, "bold"))
        
        self.folder_label.pack(anchor="w", padx=15, pady=(10,5))

        self.folder_entry = ctk.CTkEntry(
            master           = self.folder_frame,
            placeholder_text = "Select a Folder",
            font             = ("Segoe UI", 12, "bold"))
        
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(15,5), pady=(0,15))

        self.browse_button = ctk.CTkButton(
            master  = self.folder_frame,
            text    = "Browse",
            font    = ("Segoe UI", 12, "bold"),
            command = self.browse_folder)
        
        self.browse_button.pack(side="right", padx=(5,15), pady=(0,15))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.on_folder_selected(folder)

    def create_button(self):

        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(padx=30, pady=30)

        self.preview_button = ctk.CTkButton(
            master  = button_frame,
            text    = "Preview",
            font    = ("Segoe UI", 12, "bold"),
            command = self.preview_rename)
                
        self.preview_button.pack(pady=15, side="left", anchor="center")

        self.rename_button = ctk.CTkButton(
            master  = button_frame,
            text    = "Rename",
            font    = ("Segoe UI", 12, "bold"),
            command = self.confirmed_rename)
        
        self.rename_button.pack(pady=15, side="left", anchor="center")

    def preview_rename(self):
        self.on_preview()

    def show_preview(self, rename_plan):
        self.rename_view.show_preview(rename_plan)

    def confirmed_rename(self):
        dialog = RenameDialog(self)
        self.wait_window(dialog)
        if dialog.get_result():
            self.on_rename()
            self.preview_rename()

    def create_label(self, master, text):

        label = ctk.CTkLabel(
            master = master, 
            text   = text,
            font   = ("Segoe UI", 12, "bold"))
        label.pack(pady=15)
        return label

    def show_status(self, success):
        if success:
            self.status_label.configure(
                text       = "● Rename Successful",
                text_color = theme.success)
        else:
            self.status_label.configure(
                text       = "● Rename Failed",
                text_color = theme.danger)



                




