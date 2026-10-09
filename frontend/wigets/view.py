import customtkinter as ctk
import config.theme as theme


class View(ctk.CTkFrame):
    """Scrollable preview table for the generated rename plan."""
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        top = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        top.grid(row=0, column=0, padx=16, pady=(14, 10), sticky="ew")
        top.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            master     = top, 
            text       = "PREVIEW", 
            anchor     = "w", 
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
            ).grid(row=0, column=0, sticky="w")
        self.count_label = ctk.CTkLabel(
            master        = top, 
            text          = "0 files", 
            corner_radius = 12,
            fg_color      = theme.panel_light, 
            text_color    = theme.text_secondary)
        self.count_label.grid(row=0, column=1, sticky="e")
        
        self.table = ctk.CTkScrollableFrame(
            master        = self, 
            fg_color      = theme.background,
            corner_radius = 8, 
            border_width  = 1, 
            border_color  = theme.border)
        self.table.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.table.grid_columnconfigure((0, 1), weight=3)
        self.table.grid_columnconfigure(2, weight=1)
        
        self._draw_header()

    def _draw_header(self):
        for col, text in enumerate(("Original Name", "New Name", "Status")):
            ctk.CTkLabel(
                master          = self.table, 
                text            = text, 
                anchor          = "w", 
                font            = ("Roboto", 12, "bold"),
                text_color      = theme.text_secondary, 
                fg_color        = theme.panel_light,
                corner_radius   = 4
                ).grid(row=0, column=col, padx=2, pady=2, sticky="ew")

    def clear_preview(self):
        for child in self.table.winfo_children():
            child.destroy()
        self._draw_header()

    def display_card(self, rename_plan):
        self.clear_preview()
        self.count_label.configure(text=f"{len(rename_plan)} files")
        styles = {
            "Ready"   : ("Ready",   theme.success), 
            "Finished": ("Renamed", theme.success),
            "Exist"   : ("Exists",  theme.warning), 
            "Error"   : ("Error",   theme.error),
            "Skipped" : ("Skipped", theme.warning)}
        
        for row, item in enumerate(rename_plan, start=1):
            old_path, new_path, status = item["old_name"], item["new_name"], item["status"]
            old_name = getattr(old_path, "name", str(old_path))
            new_name = getattr(new_path, "name", str(new_path))
            status_text, status_color = styles.get(status, (str(status), theme.text_secondary))
            bg = theme.panel if row % 2 == 0 else theme.background
            
            for col, value, color in ((0, old_name, theme.text_primary),
                                      (1, str(new_name), theme.text_primary),
                                      (2, status_text, status_color)):
                ctk.CTkLabel(
                    master     = self.table, 
                    text       = value, 
                    anchor     = "w" if col < 2 else "center",
                    text_color = color, 
                    fg_color   = bg, 
                    padx       = 8, 
                    pady       = 12
                    ).grid(row=row, column=col, padx=2, pady=1, sticky="ew")
