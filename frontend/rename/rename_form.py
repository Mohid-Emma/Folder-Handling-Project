#  rename_form.py

import customtkinter as     ctk
from   config        import theme

class RenameForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color= theme.panel_light)

        self.create_layout()
        self.create_widget()
        
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

        self.pattern_entry.grid(row=3, column=0, columnspan=2, padx=(20,0), pady=5, sticky="ew")

        self.type_label = ctk.CTkLabel(
            master     = self, 
            text       = "Type", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.type_label.grid(row=4, column=0, padx=25, pady=10, sticky="w")

        type_option = [
            ".mp3",
            ".mp4",
            ".mkv",
            ".txt",
            ".png",
            ".jpg"]
        
        self.type_menu = ctk.CTkOptionMenu(
            master               = self, 
            values               = type_option, 
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
        
        self.type_menu.set("Type By")
        self.type_menu.grid(row=5, column=0, padx=(0,0))

        self.quality_label = ctk.CTkLabel(
            master     = self, 
            text       = "Quality", 
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)

        self.quality_label.grid(row=6, column=0, padx=25, pady=10, sticky="w")

        quailtied_option = [
            "360p",
            "480p",
            "720p",
            "1080p"]
        
        self.quailty_menu = ctk.CTkOptionMenu(
            master               = self, 
            values               = quailtied_option, 
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
        
        self.quailty_menu.set("Quailty By")
        self.quailty_menu.grid(row=7, column=0, padx=(0,0))

        self.preview_button = ctk.CTkButton(
            master      = self,
            text        = "Preview",
            font        = ("Segoe UI", 12, "bold"),
            command     = None, #self.preview_rename,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.preview_button.grid(row=8, column=0, padx=15, pady=(15,5), sticky="ew")

        self.rename_button = ctk.CTkButton(
            master      = self,
            text        = "Rename",
            font        = ("Segoe UI", 12, "bold"),
            command     = None, #self.confirmed_rename,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        self.rename_button.grid(row=8, column=1, padx=15, pady=(15,5), sticky="ew")

