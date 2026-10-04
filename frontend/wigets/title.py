# title.py

import customtkinter    as     ctk
import config.theme     as     theme
import config.icon            as     icon
from   utils.file_utils import icon_image_convert


class Title(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.panel)

        self.create_layout()
        self.create_widgets()


    def create_layout(self):
        self.grid_columnconfigure(0, weight=0) # Icon
        self.grid_columnconfigure(1, weight=1) # Text

    def create_widgets(self):

        icon_frame = ctk.CTkFrame(
            master   = self, 
            border_width=5,
            fg_color = theme.action,
            border_color=theme.action
            )
        
        icon_frame.grid(row=0, column=0, padx=10, pady=10)

        ctk_icon = icon_image_convert(icon.rename_fill, theme.text_primary, 35)

        self.icon_label = ctk.CTkLabel(
            master  = icon_frame,
            image   = ctk_icon,
            text    = "",
            bg_color= theme.action)
        
        self.icon_label.grid(row=0, column=0, padx=2, pady=2, ipadx=5, ipady=7, sticky="news")

        title_frame = ctk.CTkFrame(
            master   = self, 
            fg_color = theme.transparent)
        
        title_frame.grid(row=0, column=1, padx=10, pady=10, sticky="news")        
        self.title_label = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Rename Files", 
            font       = ("Roboto", 23, "bold"),
            text_color = theme.text_primary)
        
        self.title_label.grid(row=0, column=0, sticky="w")

        self.discription_label = ctk.CTkLabel(
            master     = title_frame, 
            text       = "Change file names using a simple and flexible pattern.", 
            font       = ("Roboto", 13),
            text_color = theme.text_secondary)

        self.discription_label.grid(row=1, column=0)

    def change_title(self, mode):
        if mode == "rename":
            self.rename_title()
        elif mode == "organize":
            self.organize_title()
        elif mode == "copy":
            self.copy_title()
        elif mode == "move":
            self.move_title()
        elif mode == "search":
            self.search_title()

    def rename_title(self):

        rename_icon = icon_image_convert(icon.rename_fill, theme.text_primary, 35)
        self.icon_label.configure(image = rename_icon)
        self.title_label.configure(text = "Rename Files")
        self.discription_label.configure(text = "Change file names using a simple and flexible pattern.")

    def organize_title(self):

        organize_icon = icon_image_convert(icon.organize_fill, theme.text_primary, 35)
        self.icon_label.configure(image = organize_icon)
        self.title_label.configure(text = "Organize Files")
        self.discription_label.configure(text = "Automatically arrange files into folders.")

    def copy_title(self):

        copy_icon = icon_image_convert(icon.copy, theme.text_primary, 35)
        self.icon_label.configure(image = copy_icon)
        self.title_label.configure(text = "Copy Files")
        self.discription_label.configure(text = "Create copies of files and folders to another location.")

    def move_title(self):

        move_icon = icon_image_convert(icon.move, theme.text_primary, 35)
        self.icon_label.configure(image = move_icon)
        self.title_label.configure(text = "Move Files")
        self.discription_label.configure(text = "Move files and folders to a different location.")

    def search_title(self):

        search_icon = icon_image_convert(icon.search, theme.text_primary, 35)
        self.icon_label.configure(image = search_icon)
        self.title_label.configure(text = "Search Files")
        self.discription_label.configure(text = "Find files and folders by name, type, content.")