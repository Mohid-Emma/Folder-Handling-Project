import customtkinter as ctk
import config.theme as theme


class Status(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, width=220, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            master     = self,
            text       = "STATUS",
            anchor     = "w",
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
        ).grid(row=0, column=0, padx=18, pady=(18, 8), sticky="ew")
        
        self.status_value = ctk.CTkLabel(
            master     = self, 
            text       = "●  Ready", 
            anchor     = "w",
            font       = ("Roboto", 14), 
            text_color = theme.success)
        self.status_value.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="ew")
        
        ctk.CTkFrame(
            master   = self,
            height   = 1,
            fg_color = theme.border
            ).grid(row=2, column=0, padx=18, pady=2, sticky="ew")
        
        ctk.CTkLabel(
            master     = self,
            text       = "SUMMARY",
            anchor     = "w",
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
            ).grid(row=3, column=0, padx=18, pady=(18, 10), sticky="ew")
        self.total_value   = self._summary_row("Total Files",    "0", 4, theme.text_primary)
        self.ready_value   = self._summary_row("Ready",          "0", 5, theme.success)
        self.exists_value  = self._summary_row("Already Exists", "0", 6, theme.warning)
        self.skipped_value = self._summary_row("Skipped",        "0", 7, theme.text_secondary)
        self.failed_value  = self._summary_row("Failed",         "0", 8, theme.error)
        
        ctk.CTkFrame(
            master   = self, 
            height   = 1, 
            fg_color = theme.border
            ).grid(row=9, column=0, padx=18, pady=(14, 8), sticky="ew")
        
        ctk.CTkLabel(
            master     = self, 
            text       = "ⓘ  File Name Pattern", 
            anchor     = "w",
            font       = ("Roboto", 13, "bold"), 
            text_color = theme.text_secondary
            ).grid(row=10, column=0, padx=18, pady=(12, 6), sticky="ew")
        
        ctk.CTkLabel(
            master      = self, 
            text        = "The application creates numbered names based on your settings.",
            anchor      = "w", 
            justify     = "left", 
            wraplength  = 185, 
            font        = ("Roboto", 12),
            text_color  = theme.text_muted
            ).grid(row=11, column=0, padx=18, pady=(0, 18), sticky="ew")

    def _summary_row(self, label, value, row, color):
        line = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        line.grid(row=row, column=0, padx=18, pady=6, sticky="ew")
        line.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            master     = line, 
            text       = label, 
            anchor     = "w", 
            text_color = theme.text_secondary
            ).grid(row=0, column=0, sticky="w")
        value_label = ctk.CTkLabel(
            master     = line, 
            text       = value, 
            anchor     = "e", 
            text_color = color,
            font       = ("Roboto", 14, "bold"))
        value_label.grid(row=0, column=1, sticky="e")
        return value_label

    def set_status(self, text, color=None):
        self.status_value.configure(text=f"●  {text}", text_color= color if color else theme.success)

    def update_summary(self, total=0, ready=0, exists=0, skipped=0, failed=0):
        self.total_value.configure(text=str(total))
        self.ready_value.configure(text=str(ready))
        self.exists_value.configure(text=str(exists))
        self.skipped_value.configure(text=str(skipped))
        self.failed_value.configure(text=str(failed))
