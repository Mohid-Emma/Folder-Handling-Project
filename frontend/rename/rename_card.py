# rename_card.py

import customtkinter as ctk
import config.theme  as theme

class RenameCard(ctk.CTkFrame):
    def __init__(self, master, old_name, new_name, status):
        super().__init__(master, fg_color=theme.transparent)

        self.old_name = old_name
        self.new_name = new_name
        self.status   = status

        self.create_layout()
        self.create_label()

    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def create_label(self):

        old_label = ctk.CTkLabel(
            master     = self, 
            text       = self.old_name,
            font       = ("Segoe UI", 12, "bold"),
            text_color = theme.text_primary)
        old_label.grid(row=1, column=0, padx=15, pady=15, sticky="ew")


        color = self.create_status()        
        
        new_label = ctk.CTkLabel(
            master     = self, 
            text       = self.new_name,
            font       = ("Segoe UI", 12, "bold"),
            text_color = color)
        new_label.grid(row=1, column=1, padx=15, pady=15, sticky="ew") 

    def create_status(self):
        if self.status == "Ready":
            return theme.action_hover
        elif self.status == "Finished":
            return theme.success

        elif self.status == "Exist":
            return theme.warning
        else:
            return theme.error