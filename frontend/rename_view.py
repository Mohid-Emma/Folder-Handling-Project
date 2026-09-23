# rename_view.py 

import customtkinter        as     ctk
import config.theme         as     theme
from   frontend.rename_card import RenameCard


class RenameView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.create_layout()

    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)

    def display_card(self, rename_plan):
        self.clear_preview()

        self.create_title()

        for row, (old_name, new_name, status) in enumerate(rename_plan, start=1):
            RenameCard(self, old_name.name, new_name.name, status).grid(row=row, column=0, padx=5, pady=5, sticky="news")

    def create_title(self):

        title_frame = ctk.CTkFrame(self, corner_radius=0)
        title_frame.grid(row=0, column=0, sticky="news")

        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=1)
        title_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            master = title_frame, 
            text   = "Original Name",
            font   = ("Segoe UI", 15, "bold")
        ).grid(row=0, column=0, padx=15, pady=15)

        ctk.CTkLabel(
            master = title_frame, 
            text   = "New Name",
            font   = ("Segoe UI", 15, "bold")
        ).grid(row=0, column=1, padx=15, pady=15)

        ctk.CTkLabel(
            master = title_frame, 
            text   = "Status",
            font   = ("Segoe UI", 15, "bold")
        ).grid(row=0, column=2, padx=15, pady=15)

    def clear_preview(self):
        for widget in self.winfo_children():
            widget.destroy()
