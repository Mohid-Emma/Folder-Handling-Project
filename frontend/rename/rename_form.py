#  rename_form.py

import customtkinter as     ctk
from   config        import theme

class RenameForm(ctk.CTkFrame):
    def __init__(self, master, on_preview_information, on_rename):
        super().__init__(master, fg_color= theme.panel_light)

        self.on_rename              = on_rename
        self.on_preview_information = on_preview_information


        self.create_layout()
        self.create_widget()

    def call_back(self):
        pattern = self.pattern_entry.get().strip()
        if pattern is None:
            return

        extension = self.extension_menu.get().strip()
        if extension is None:
            return

        quality = self.quality_menu.get().strip()
        if quality is None:
            return
        return pattern, extension, quality



    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_widget(self): 

        self.title = ctk.CTkLabel(
            master     = self, 
            text       = "⚙️ Rename Settings", 
            font       = ("Segoe UI", 18, "bold"),
            text_color = theme.text_primary)

        self.title.grid(row=0, column=0, columnspan=2, padx=25, pady=10, sticky="w")

        self.pattern_label = ctk.CTkLabel(
            master     = self, 
            text       = "Pattern", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.pattern_label.grid(row=2, column=0, padx=25, pady=5, sticky="w")

        self.pattern_entry = ctk.CTkEntry(
            master                 = self,
            placeholder_text       = "Create a Pattern",
            font                   = ("Segoe UI", 12, "bold"),
            height                 = 35,
            border_color           = theme.border,
            text_color             = theme.text_primary,
            placeholder_text_color = theme.text_secondary,
            fg_color               = theme.background)

        self.pattern_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        self.extension_label = ctk.CTkLabel(
            master     = self, 
            text       = "extension", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.extension_label.grid(row=4, column=0, padx=25, pady=10, sticky="w")

        extension_option = [
            ".mp3",
            ".mp4",
            ".mkv",
            ".txt",
            ".png",
            ".jpg",
            ".txt",
            ".pdf"]
        
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
        self.extension_menu.grid(row=5, column=0, padx=(0,0))

        self.quality_label = ctk.CTkLabel(
            master     = self, 
            text       = "Quality", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.quality_label.grid(row=6, column=0, padx=25, pady=10, sticky="w")

        qualitied_option = [
            "360p",
            "480p",
            "720p",
            "1080p"]
        
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
        self.quality_menu.grid(row=7, column=0, padx=(0,0))

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
            command     = self.on_rename, #self.confirmed_rename,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.rename_button.grid(row=8, column=1, padx=15, pady=(15,5), sticky="ew")


    # def file_inform(self):

        
