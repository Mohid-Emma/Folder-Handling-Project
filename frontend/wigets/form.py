import customtkinter as     ctk
import config.theme  as     theme
from   tkinter       import filedialog, messagebox


class _SourceFolder:
    def __init__(self, entry):
        self.entry = entry

    def get_folder_path(self):
        return self.entry.get().strip() or None


class Form(ctk.CTkFrame):
    def __init__(self, master, on_preview, on_rename, on_organize, on_copy, on_move, on_search, **kwargs):
        super().__init__(master, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, **kwargs)
        
        self.on_preview = on_preview
        self.on_rename = on_rename
        
        self.pattern_var       = ctk.StringVar(value="Episode")
        self.start_var         = ctk.StringVar(value="1")
        self.number_format_var = ctk.StringVar(value="01 (Two Digits)")
        self.extension_var     = ctk.StringVar(value=".mp4")
        self.quality_var       = ctk.StringVar(value="1080p")
        self.skip_same_var     = ctk.BooleanVar(value=True)
        self.video_only_var    = ctk.BooleanVar(value=True)

        self._build_1()
        self._build_2()
        self._build_3()
        self._build_4()

    def _section(self, text, row):
        ctk.CTkLabel(
            master     = self, 
            text       = text.upper(), 
            anchor     = "w",
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
            ).grid( row=row, column=0, columnspan=2, padx=18,
                    pady=(18, 8), sticky="ew")

    def _build_1(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self._section("Source Folder", 0)

        folder_row = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        folder_row.grid(row=1, column=0, columnspan=2, padx=18, sticky="ew")
        folder_row.grid_columnconfigure(0, weight=1)
        self.source_entry = ctk.CTkEntry(
            master           = folder_row, 
            height           = 42, 
            placeholder_text = "Select a folder...",
            fg_color         = theme.background, 
            border_color     = theme.border)
        
        self.source_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.source_file = _SourceFolder(self.source_entry)
        
        ctk.CTkButton(
            master      = folder_row, 
            text        = "Browse", 
            width       = 95, 
            height      = 42,
            fg_color    = theme.action, 
            hover_color = theme.action_hover,          
            command     = self._browse).grid(row=0, column=1)

    def _build_2(self):
        self._section("Rename Settings", 2)
        ctk.CTkLabel(
            master     = self, 
            text       = "Name", 
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=3, column=0, padx=(18, 6), pady=(0, 5), sticky="ew")
        ctk.CTkLabel(
            master     = self, 
            text       = "Start Number", 
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=3, column=1, padx=(6, 18), pady=(0, 5), sticky="ew")
        ctk.CTkEntry(
            master       = self, 
            textvariable = self.pattern_var, 
            height       = 42,
            fg_color     = theme.background, 
            border_color = theme.border).grid(
            row=4, column=0, padx=(18, 6), sticky="ew")
        ctk.CTkEntry(
            master       = self, 
            textvariable = self.start_var, 
            height       = 42,
            fg_color     = theme.background, 
            border_color = theme.border).grid(
            row=4, column=1, padx=(6, 18), sticky="ew")
        ctk.CTkLabel(
            master     = self, 
            text       = "Number Format", 
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=5, column=0, padx=(18, 6), pady=(14, 5), sticky="ew")
        ctk.CTkLabel(
            master     = self, 
            text       = "Extension", 
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=5, column=1, padx=(6, 18), pady=(14, 5), sticky="ew")
        ctk.CTkOptionMenu(
            master             = self, 
            variable           = self.number_format_var,
            values             = ["1 (Normal)", "01 (Two Digits)", "001 (Three Digits)"],
            height             = 42, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
                row=6, column=0, padx=(18, 6), sticky="ew")
        ctk.CTkOptionMenu(
            master             = self, 
            variable           = self.extension_var,
            values             = [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".jpg", ".png", ".pdf", "All files"],
            height             = 42, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
                row=6, column=1, padx=(6, 18), sticky="ew")
        ctk.CTkLabel(
            master     = self, 
            text       = "Quailty", 
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=7, column=0, padx=(6, 18), pady=(14, 5), sticky="ew")
        ctk.CTkOptionMenu(
            self, 
            variable           = self.quality_var,
            values             = ["360p", "480p", "720p", "1080p"],
            height             = 42, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
                row=8, column=0, padx=(18, 6), sticky="ew")

    def _build_3(self):
        self._section("Options", 9)
        for row, text, variable in (
            (10, "Skip files with the same name", self.skip_same_var),
            (11, "Show only video files", self.video_only_var),
        ):
            ctk.CTkCheckBox(
                master       = self, 
                text         = text, 
                variable     = variable,
                text_color   = theme.text_primary, 
                fg_color     = theme.action,
                hover_color  = theme.action_hover, 
                border_color = theme.border
                ).grid(
                    row=row, column=0, columnspan=2, padx=20, pady=7, sticky="w")

    def _build_4(self):

        buttons = ctk.CTkFrame(
            master=self, 
            fg_color="transparent")
        buttons.grid(row=12, column=0, columnspan=2, padx=18, pady=(28, 18), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            master       = buttons, 
            text         = "◉  Preview", 
            height       = 46,
            fg_color     = "transparent", 
            border_width = 1, 
            border_color = theme.action,
            hover_color  = theme.action_disable_hover, 
            text_color   = theme.text_secondary,
            command      = self._preview
            ).grid(row=0, column=0, padx=(0, 6), sticky="ew")
        
        ctk.CTkButton(
            master       = buttons, 
            text         = "▶  Rename", 
            height       = 46,
            fg_color     = theme.action, 
            hover_color  = theme.action_hover,
            command      = self._rename
            ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _browse(self):
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, folder)

    def call_back(self):
        pattern = self.pattern_var.get().strip()
        try:
            start_number = int(self.start_var.get().strip())
            if start_number < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid settings", "Start Number must be a non-negative integer.", parent=self)
            return None
        return (pattern, self.extension_var.get(), self.quality_var.get(),
                start_number, self.number_format_var.get())

    def _preview(self):
        self.on_preview()

    def _rename(self):
        self.on_rename()
