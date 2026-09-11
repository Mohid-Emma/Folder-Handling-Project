# rename_dialog.py

import customtkinter as ctk

class RenameDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.confirm = None

        self.title("Confirm Rename")
        self.geometry("400x200")
        self.transient(master)
        self.grab_set()

        self.create_widget()

    def create_widget(self):
        label = ctk.CTkLabel(
            master = self,
            text   = "Are you sure you want to rename the files?",
            font   = ("Segoe UI", 15, "bold"))
        label.pack(pady=30)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack()

        self.cancel_button = ctk.CTkButton(
            master  = button_frame,
            text    = "Cancel",
            font    = ("Segoe UI", 12, "bold"),
            command = self.destroy)
        
        self.cancel_button.pack(pady=15, side="left", anchor="center")

        self.confirm_button = ctk.CTkButton(
            master  = button_frame,
            text    = "Confirm",
            font    = ("Segoe UI", 12, "bold"),
            command = lambda: self.confirmed_rename())
        
        self.confirm_button.pack(pady=15, side="left", anchor="center")

    def confirmed_rename(self):
        self.confirm = True
        self.destroy()

    def get_result(self):
        return self.confirm