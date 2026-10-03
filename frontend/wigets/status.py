# rename_status.py

import customtkinter as ctk
import config.theme  as theme

class RenameStatus(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=theme.panel_light)

