#  rename_form.py

import customtkinter as     ctk
from   config        import theme
from   tkinter       import messagebox

class RenameForm(ctk.CTkFrame):
    def __init__(self, master, on_preview_information, on_rename):
        super().__init__(master, fg_color= theme.panel_light)

        self.on_rename              = on_rename
        self.on_preview_information = on_preview_information

        self.create_layout()
        self.create_widgets()

    # To Receive Rename Form's Value 
    def call_back(self):
        pattern = self.pattern_entry.get().strip()
        if not pattern:
            pattern = False

        start_number = self.start_number_entry.get().strip()
        if not start_number:
            messagebox.showerror("Mssing Input", f"Start Number is Missing\n"+" "*100)
            return None
        
        try:
            start_number = int(start_number)
        except ValueError:
            messagebox.showerror("Invalid Value", f"Integer Error\n"+" "*100)
            return None

        number_foramt = self.number_format_menu.get().strip()
        if number_foramt.strip() == "Number Format By":
            messagebox.showerror("Mssing Input", f"Number Format is Missing\n"+" "*100) 
            return None
        
        extension = self.extension_menu.get().strip()
        if extension.strip() == "Extension By":
            messagebox.showerror("Mssing Input", f"Extension is Missing\n"+" "*100)
            return None

        quality = self.quality_menu.get().strip()
        if quality.strip() == "Quality By":
            messagebox.showerror("Mssing Input", f"Quality is Missing\n"+" "*100)        
            return None
        
        return pattern, extension, quality, start_number, number_foramt

    # Create Layout
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1) # Contain Starting Number and Extension
        self.grid_columnconfigure(1, weight=1) # Contain Number Format and Quality

    # Create Widgets
    def create_widgets(self): 

        # Create Title 

        self.title = ctk.CTkLabel(
            master     = self, 
            text       = "⚙️ Rename Settings", 
            font       = ("Segoe UI", 18, "bold"),
            text_color = theme.text_primary)

        self.title.grid(row=0, column=0, columnspan=2, padx=25, pady=10, sticky="w")

        # First Level Contains Pattern and Cancel Button

        self.pattern_label = ctk.CTkLabel(
            master     = self, 
            text       = "Pattern", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.pattern_label.grid(row=2, column=0, padx=25, pady=5, sticky="w")

        pattern_frame = ctk.CTkFrame(
            master   = self, 
            fg_color = theme.transparent)
        pattern_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        pattern_frame.grid_columnconfigure(0,weight=1)

        self.pattern_entry = ctk.CTkEntry(
            master                 = pattern_frame,
            placeholder_text       = "Create a Pattern",
            font                   = ("Segoe UI", 12, "bold"),
            height                 = 33,
            border_color           = theme.border,
            text_color             = theme.text_primary,
            placeholder_text_color = theme.text_secondary,
            fg_color               = theme.background)

        self.pattern_entry.grid(row=0, column=0, padx=(20,5), pady=5, sticky="ew")

        self.cancel_button = ctk.CTkButton(
            master      = pattern_frame,
            text        = "Cancel",
            font        = ("Segoe UI", 12, "bold"),
            command     = self.clear_entries,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.cancel_button.grid(row=0, column=1, padx=(0,20), pady=5, sticky="ew")

        # Second Level Contains Starting Number and Number Format
        
        self.start_number_label = ctk.CTkLabel(
            master     = self, 
            text       = "Starting Number", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.start_number_label.grid(row=4, column=0, padx=25, pady=5, sticky="w")

        self.start_number_entry = ctk.CTkEntry(
            master                 = self,
            placeholder_text       = "Start Number",
            font                   = ("Segoe UI", 12, "bold"),
            height                 = 35,
            border_color           = theme.border,
            text_color             = theme.text_primary,
            placeholder_text_color = theme.text_secondary,
            fg_color               = theme.background)

        self.start_number_entry.grid(row=5, column=0, padx=(20,35), pady=5, sticky="ew")

        self.number_format_label = ctk.CTkLabel(
            master     = self, 
            text       = "Number Format", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.number_format_label.grid(row=4, column=1, padx=25, pady=5, sticky="w")

        number_format_option = ["01","02","03","04","05","06","07","08","09","010"]
        
        self.number_format_menu = ctk.CTkOptionMenu(
            master               = self, 
            values               = number_format_option, 
            command              = None,
            height               = 30,
            width                = 200,
            corner_radius        = 9,
            font                 = ("Segoe UI", 12),
            fg_color             = theme.panel,
            button_color         = theme.action,
            button_hover_color   = theme.action_hover,
            text_color           = theme.text_primary, 
            dropdown_fg_color    = theme.panel_light,
            dropdown_hover_color = theme.panel_light,
            dropdown_text_color  = theme.text_primary)
        
        self.number_format_menu.set("Number Format By")
        self.number_format_menu.grid(row=5, column=1, padx=20, sticky="ew")

        # Third Level Contains Pattern and Cancel Button
        
        self.extension_label = ctk.CTkLabel(
            master     = self, 
            text       = "Extension", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.extension_label.grid(row=6, column=0, padx=25, pady=5, sticky="w")

        extension_option = [".mp3", ".mp4", ".mkv", ".txt", ".png", ".jpg", ".txt", ".pdf"]
        
        self.extension_menu = ctk.CTkOptionMenu(
            master               = self, 
            values               = extension_option, 
            command              = None,
            height               = 30,
            width                = 200,
            corner_radius        = 9,
            font                 = ("Segoe UI", 12),
            fg_color             = theme.panel,
            button_color         = theme.action,
            button_hover_color   = theme.action_hover,
            text_color           = theme.text_primary, 
            dropdown_fg_color    = theme.panel_light,
            dropdown_hover_color = theme.panel_light,
            dropdown_text_color  = theme.text_primary)
        
        self.extension_menu.set("Extension By")
        self.extension_menu.grid(row=7, column=0, padx=20, sticky="ew")

        self.quality_label = ctk.CTkLabel(
            master     = self, 
            text       = "Quality", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.quality_label.grid(row=6, column=1, padx=25, pady=5, sticky="w")

        qualitied_option = ["360p", "480p", "720p", "1080p"]
        
        self.quality_menu = ctk.CTkOptionMenu(
            master               = self, 
            values               = qualitied_option, 
            command              = None,
            height               = 30,
            width                = 200,
            corner_radius        = 9,
            font                 = ("Segoe UI", 12),
            fg_color             = theme.panel,
            button_color         = theme.action,
            button_hover_color   = theme.action_hover,
            text_color           = theme.text_primary, 
            dropdown_fg_color    = theme.panel_light,
            dropdown_hover_color = theme.panel_light,
            dropdown_text_color  = theme.text_primary)
        
        self.quality_menu.set("Quality By")
        self.quality_menu.grid(row=7, column=1, padx=20, sticky="ew")

        # Fourth Level Contains Preview and Rename Button

        self.preview_button = ctk.CTkButton(
            master      = self,
            text        = "Preview",
            font        = ("Segoe UI", 12, "bold"),
            command     = self.on_preview_information,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.preview_button.grid(row=8, column=0, padx=15, pady=(15,5), sticky="ew")

        self.rename_button = ctk.CTkButton(
            master      = self,
            text        = "Rename",
            font        = ("Segoe UI", 12, "bold"),
            command     = self.on_rename,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.rename_button.grid(row=8, column=1, padx=15, pady=(15,5), sticky="ew")

    # To Clear Pattern Entry
    def clear_entries(self):
        self.pattern_entry.delete(0, "end")
        self.pattern_entry.focus()
