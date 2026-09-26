# rename_card.py

import customtkinter as ctk
import config.theme  as theme

class RenameCard(ctk.CTkFrame):
    def __init__(self, master, old_name, new_name, status):
        super().__init__(master)

        self.old_name = old_name
        self.new_name = new_name
        self.status   = status

        self.create_layout()
        self.create_label()

    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def create_label(self):

        old_label = ctk.CTkLabel(
            master = self, 
            text   = self.old_name,
            font   = ("Segoe UI", 12, "bold"))
        old_label.grid(row=1, column=0, padx=15, pady=15)

        new_label = ctk.CTkLabel(
            master = self, 
            text   = self.new_name,
            font   = ("Segoe UI", 12, "bold"))
        new_label.grid(row=1, column=1, padx=15, pady=15) 

        color, status_text = self.create_status()

        status_label = ctk.CTkLabel(
            master     = self, 
            text       = status_text,
            text_color = color,
            font       = ("Segoe UI", 12, "bold"))
        status_label.grid(row=1, column=2, padx=15, pady=15)

    def create_status(self):
        if self.status == "Ready":
            return theme.text, "● Ready for Rename"
        
        elif self.status == "Finished":
            return theme.success, "● Renamed"

        elif self.status == "Exist":
            return theme.warning, "⚠ Already Exists"

        else:
            return theme.error, "Error"