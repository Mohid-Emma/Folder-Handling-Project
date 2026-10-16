import customtkinter as ctk
import config.theme  as theme
import config.icon   as icon
from utils import icon_image_convert


class Title(ctk.CTkFrame):
    TITLES = {
        "rename"  : ("Rename Files", "Change file names using a simple and flexible pattern.", "rename_fill"),
        "organize": ("Organize Files", "Automatically arrange files into folders.", "organize_fill"),
        "move"    : ("Move Files", "Move files and folders to a different location.", "move"),
        "copy"    : ("Copy Files", "Create copies of files and folders to another location.", "copy"),
        "search"  : ("Search Files", "Find files and folders by name, type, or content.", "search"),
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, height=105, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)
        
        self.icon_label = ctk.CTkLabel(
            master        = self, 
            text          = "", 
            width         = 64, 
            height        = 64,
            fg_color      = theme.action, 
            corner_radius = 9)
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=(18, 16), pady=18)
        
        self.heading = ctk.CTkLabel(self, text="Rename Files", anchor="w",
            font=("Roboto", 25, "bold"), text_color=theme.text_primary)
        self.heading.grid(row=0, column=1, padx=(0, 18), pady=(22, 0), sticky="ew")
        
        self.description = ctk.CTkLabel(
            master = self,
            text   = "Change file names using a simple and flexible pattern.", 
            anchor = "w",
            font   = ("Roboto", 14), text_color=theme.text_secondary)
        self.description.grid(row=1, column=1, padx=(0, 18), pady=(0, 20), sticky="ew")
        
        self.change_title("rename")

    def change_title(self, mode):
        title, description, icon_attr = self.TITLES.get(mode, self.TITLES["rename"])
        self.heading.configure(text=title)
        self.description.configure(text=description)
        icon_name = getattr(icon, icon_attr, None)
        if icon_name:
            try:
                image = icon_image_convert(icon_name, "#FFFFFF", 34)
                self.icon_label.configure(image=image, text="")
                self.icon_label.image = image
                return
            except Exception:
                pass
        self.icon_label.configure(text=title[:1], font=("Roboto", 24, "bold"))
