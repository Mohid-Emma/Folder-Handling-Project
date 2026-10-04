# file_utils.py

import customtkinter as     ctk
from   tkinter_icons import BootstrapIcon


def icon_image_convert(icon_name, color, size):
    icon = BootstrapIcon.render_pil(icon_name, size, color=color)
    ctk_icon = ctk.CTkImage(light_image=icon, dark_image=icon, size=(size,size))
    return ctk_icon
        