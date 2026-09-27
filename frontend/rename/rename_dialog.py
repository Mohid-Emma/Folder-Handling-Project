# rename_dialog.py

import customtkinter as     ctk
from   config        import theme


class RenameDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.background)

        self.confirm = None

        self.title("Confirm Rename")
        self.geometry("400x200")
        self.transient(master)
        self.grab_set()

        self.create_widget()

    def create_widget(self):

        
        self.grid_columnconfigure(0, weight=1)

        self.card = ctk.CTkFrame(
            master        = self,
            corner_radius = 15,
            border_width  = 1,
            border_color  = theme.border,
            fg_color      = theme.panel)
        self.card.grid(row=0, column=0, padx=25, pady=25, sticky="news")

        self.card.grid_columnconfigure(0, weight=1)


        label = ctk.CTkLabel(
            master     = self.card,
            text       = "Are you sure you want to rename the files?",
            font       = ("Segoe UI", 15, "bold"),
            text_color = theme.text_primary)
        label.pack(pady=30)

        button_frame = ctk.CTkFrame(
            master   = self.card, 
            fg_color = theme.transparent)
        button_frame.pack()

        cancel_button = ctk.CTkButton(
            master      = button_frame,
            text        = "Cancel",
            font        = ("Segoe UI", 12, "bold"),
            command     = self.destroy,
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        cancel_button.pack(pady=15, side="left", anchor="center")

        confirm_button = ctk.CTkButton(
            master      = button_frame,
            text        = "Confirm",
            font        = ("Segoe UI", 12, "bold"),
            command     = lambda: self.confirmed_rename(),
            text_color  = theme.text_primary,
            fg_color    = theme.action,
            hover_color = theme.action_hover)
        
        confirm_button.pack(pady=15, side="left", anchor="center")

    def confirmed_rename(self):
        self.confirm = True
        self.destroy()

    def get_result(self):
        return self.confirm