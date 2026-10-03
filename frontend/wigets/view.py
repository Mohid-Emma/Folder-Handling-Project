# rename_view.py 

import customtkinter        as     ctk
import config.theme         as     theme
from   frontend.wigets.card import RenameCard


class RenameView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.panel_light)

        self.create_layout()
        self.create_title()

        self.renamelist = RenameList(self)
        self.renamelist.grid(row=1, column=0, padx=25, pady=10, sticky="news")

    def create_layout(self):
        self.grid_rowconfigure(1, weight=1)    # Rename List 
        self.grid_columnconfigure(0, weight=1) # Rename View Title

    # Create Title
    def create_title(self):
        self.title_label = ctk.CTkLabel(
           master     = self, 
           text       = "💾 Rename Preview", 
           font       = ("Segoe UI", 18, "bold"),
           text_color = theme.text_primary)
        
        self.title_label.grid(row=0, column=0, padx=25, pady=10, sticky="w")

    # Sent Rename Plan to Rename List
    def display_card(self, rename_plan):
        self.renamelist.display_card(rename_plan)


class RenameList(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.background)

        self.create_layout()
        self.display_card(None)

    # Create Layout
    def create_layout(self):
        self.grid_columnconfigure(0, weight=1) # Rename Files List

    # Display Card
    def display_card(self, rename_plan):
        self.clear_preview()
        if rename_plan is None:
            self.show_empty_message()
            return
        self.create_title()

        for row, (old_name, new_name, status) in enumerate(rename_plan, start=2):
            RenameCard(self, old_name.name, new_name.name, status).grid(row=row, column=0, padx=5, pady=5, sticky="news")

    # Create Title For Card
    def create_title(self):
        title_frame = ctk.CTkFrame(
            master        = self, 
            corner_radius = 0,
            fg_color      = theme.transparent)
        title_frame.grid(row=1, column=0, sticky="news")

        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            master    = title_frame, 
            text      = "Original Name",
            font      = ("Segoe UI", 18, "bold"),
           text_color = theme.text_primary
        ).grid(row=0, column=0, padx=15, pady=15)

        ctk.CTkLabel(
            master    = title_frame, 
            text      = "New Name",
            font      = ("Segoe UI", 18, "bold"),
           text_color = theme.text_primary
        ).grid(row=0, column=1, padx=15, pady=15)


    # Rename Old Preview 
    def clear_preview(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Create Empty Message
    def show_empty_message(self):
        empty_frame = ctk.CTkFrame(
            master   = self, 
            fg_color = theme.transparent)
        empty_frame.grid(row=1, column=0, padx=20, pady=60, sticky="news")

        ctk.CTkLabel( 
            master = empty_frame, 
            text   = "📁", 
            font   = ("Segoe UI Emoji", 40)
            ).pack(pady=(0, 10))

        ctk.CTkLabel(
            master     = empty_frame, 
            text       = "No File Available.",
            font       = ("Segoe UI", 20, "bold"),
            text_color = theme.text_primary
            ).pack(pady=5)

        ctk.CTkLabel(
            master     = empty_frame, 
            text       = "Try Changing Your Search.",
            font       = ("Segoe UI", 11),
            text_color = theme.text_secondary
            ).pack(pady=5) 
