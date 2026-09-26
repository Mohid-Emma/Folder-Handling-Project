# source_file.py

import customtkinter as     ctk
from   config        import theme
from   tkinter       import filedialog

class SourceFile(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.panel_light)

        self.folder_path = None

        self.create_layout()
        self.create_widget()

    def create_layout(self):
        self.columnconfigure(0, weight=1)

    def create_widget(self):

        self.title_label = ctk.CTkLabel(
            master     = self, 
            text       = "📁 Select a Folder", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.title_label.grid(row=0, column=0, columnspan=3, padx=25, pady=10, sticky="w")

        folder_frame = ctk.CTkFrame(
            master   = self, 
            fg_color = theme.transparent)
        folder_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        folder_frame.grid_columnconfigure(0,weight=1)

        self.folder_entry = ctk.CTkEntry(
            master                 = folder_frame,
            placeholder_text       = "📁 Select a Folder",
            font                   = ("Segoe UI", 12, "bold"),
            height                 = 35,
            border_color           = theme.border,
            text_color             = theme.text_primary,
            placeholder_text_color = theme.text_secondary,
            fg_color               = theme.background)
        
        self.folder_entry.grid(row=0, column=0, padx=(20,0), pady=(15,5), sticky="ew")

        self.browse_button = ctk.CTkButton(
            master      = folder_frame,
            text        = "Browse",
            font        = ("Segoe UI", 12, "bold"),
            command     = self.browse_folder,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)


        self.browse_button.grid(row=0, column=1, padx=15, pady=(15,5), sticky="ew")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.folder_path = folder