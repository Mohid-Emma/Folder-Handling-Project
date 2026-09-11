# rename_view.py 

import customtkinter as ctk
import config.theme  as theme


class RenameView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.create_layout()

    def create_layout(self):
        self.grid_columnconfigure((0,1,2), weight=1)

    def create_title(self):
        ctk.CTkLabel(
            master = self, 
            text   = "Original Name",
            font   = ("Segoe UI", 26, "bold")
        ).grid(row=0, column=0, padx=15, pady=15)

        ctk.CTkLabel(
            master = self, 
            text   = "New Name",
            font   = ("Segoe UI", 26, "bold")
        ).grid(row=0, column=1, padx=15, pady=15)

        ctk.CTkLabel(
            master = self, 
            text   = "Status",
            font   = ("Segoe UI", 26, "bold")
        ).grid(row=0, column=2, padx=15, pady=15)

    def create_label(self, row, odd_text, new_text, status):

        odd_label = ctk.CTkLabel(
            master = self, 
            text   = odd_text,
            font   = ("Segoe UI", 15, "bold"))
        odd_label.grid(row=row, column=0, padx=15, pady=15)

        new_label = ctk.CTkLabel(
            master = self, 
            text   = new_text,
            font   = ("Segoe UI", 15, "bold"))
        new_label.grid(row=row, column=1, padx=15, pady=15)

        if status:
            color       = theme.success
            status_text = "● Ready for Rename"
        else:
            color       = theme.danger
            status_text = "⚠ Already Exists" 

        status_label = ctk.CTkLabel(
            master     = self, 
            text       = status_text,
            text_color = color,
            font       = ("Segoe UI", 15, "bold"))
        status_label.grid(row=row, column=2, padx=15, pady=15)


    def show_preview(self, rename_plan):
        self.clear_preview()
        self.create_title()

        for row, (old_name, new_name, status) in enumerate(rename_plan, start=1):
            if status:
                self.create_label(row, old_name.name, new_name.name, status)
            else:
                self.create_label(row, old_name.name, new_name.name, status)

    def clear_preview(self):
        for widget in self.winfo_children():
            widget.destroy()
