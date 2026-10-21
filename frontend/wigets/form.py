import customtkinter as     ctk
import config.theme  as     theme
import config.icon   as     icon
from   utils         import icon_image_convert
from   tkinter       import filedialog, messagebox


class _SourceFolder:
    def __init__(self, entry : ctk.CTkEntry): 
        self.entry = entry

    def get_folder_path(self) -> str | None:
        return self.entry.get().strip() or None


class Form(ctk.CTkFrame):
    def __init__(self, master, operation: dict, **kwargs): 
        super().__init__(master, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, **kwargs)

        self.operation = operation

        # Rename
        self.pattern_var        = ctk.StringVar(value="Episode")
        self.start_var          = ctk.StringVar(value="1")
        self.number_format_var  = ctk.StringVar(value="01 (Two Digits)")
        self.extension_var      = ctk.StringVar(value=".mp4")
        self.quality_var        = ctk.StringVar(value="1080p")
        self.skip_same_var      = ctk.BooleanVar(value=True) # Rename
        self.video_only_var     = ctk.BooleanVar(value=True) # Rename

        # Organize
        self.organize_by        = ctk.StringVar(value="File Type")
        self.create_folder      = ctk.BooleanVar(value=True)
        self.org_recursive      = ctk.StringVar(value=False)

        # Copy
        self.copy_overwrite      = ctk.BooleanVar(value=False)
        self.copy_recursive      = ctk.BooleanVar(value=True)
        self.copy_keep_structure = ctk.BooleanVar(value=True)

        # Move
        self.move_recursive      = ctk.BooleanVar(value=True)
        self.move_keep_structure = ctk.BooleanVar(value=True)

        # Search
        self.search_query        = ctk.StringVar(value="")
        self.search_by           = ctk.StringVar(value="All Files")
        self.search_recursive    = ctk.BooleanVar(value=True)
        self.case_sensitive      = ctk.BooleanVar(value=False)
        self.search_contents     = ctk.BooleanVar(value=False)
        self.modified_within     = None # ctk.BooleanVar(value=False)

        self.OPTIONS = {
        "rename"  : (("Skip files with the same name", self.skip_same_var), ("Show only video files", self.video_only_var)),
        "organize": (("Create folders automatically", self.create_folder), ("Include files in subfolders" , self.org_recursive)),
        "copy"    : (("Copy files (not move)", self.copy_overwrite), ("Include subfolders" , self.copy_recursive), ("Keep original file structure", self.copy_keep_structure)),
        "move"    : (("Move empty folders" , self.move_recursive), ("Keep original folder structure", self.move_keep_structure)),
        "search"  : (("Include subfolders", self.search_recursive), ("Case sensitive" , self.case_sensitive), ("Search file contents (slower)", self.search_contents)) }

        self.MENU = {
        "rename" : [(self.number_format_var, ["1 (Normal)", "01 (Two Digits)", "001 (Three Digits)"], 6, 0, (18, 6)),
                    (self.extension_var, [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".jpg", ".png", ".pdf", "All files"], 6, 1, (6, 18)),
                    (self.quality_var, ["360p", "480p", "720p", "1080p"], 8, 0, (18, 6)) ],
        "organize": [(self.organize_by, ["File Type","File Extension","Date Modified"], 5)],
        "search"  : [(self.search_by, ["All Files","Video","Image","Audio","Document","Archive","Other"], 3)] }

        self.change_form("rename")
    
    def change_form(self, mode: str) -> None:
        self._destroy_widgets()
        self._build(mode)

    def _build(self, current_mode: str) -> None:

        self.grid_columnconfigure((0, 1), weight=1)
        self.source_file = self._browse_form("Source Folder", 0) 

        modes = {
            "rename"  : self._build_rename,
            "organize": self._build_organize,
            "move"    : self._build_move,
            "copy"    : self._build_copy,
            "search"  : self._build_search,
        }

        for mode, form in modes.items():
            if mode == current_mode:
                form()

    def _build_rename(self) -> None:
        rename_label = [ 
            ("Number Format", 5, 0, (18, 6), (14, 5)),
            ("Extension", 5, 1, (6, 18), (14, 5)),
            ("Quailty", 7, 0, (18, 6), (14, 5)) ]
        
        self._section("Rename Settings", 2)

        self._label("Name", row=3, column=0, padx=(18, 6), pady=(0, 5))
        self._label("Start Number", row=3, column=1, padx=(6, 18), pady=(0, 5))
        self._entry(self.pattern_var, row=4, column=0, padx=(18, 6))
        self._entry(self.start_var, row=4, column=1, padx=(6, 18))
        
        self._menu(rename_label, self.MENU["rename"])
        self._option("rename",9)
        self._button("Rename", 12)

    def _build_organize(self) -> None:
        self.org_destination = self._browse_form("DESTINATION", 2)
        self._section("ORGANIZE BY", 4)
        self._menu(menus=self.MENU["organize"], with_colspan=True)

        info_icon = icon_image_convert(icon.info, theme.text_primary, 15)
        ctk.CTkLabel(
            master     = self, 
            text       = " Files will be sorted into folders based on their type.", 
            image      = info_icon,
            compound   = "left",
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=6, column=0, padx=(18, 6), pady=(0, 5), columnspan=2, sticky="ew")

        self._option("organize", 7)
        self._button("Organize", 10)
    
    def _build_copy(self) -> None:

        self.copy_destination = self._browse_form("DESTINATION FOLDER", 2)
        self._option("copy",4)
        self._button("Copy", 8)
            
    def _build_move(self) -> None:
        
        self.move_destination = self._browse_form("DESTINATION FOLDER", 2)
        self._option("move", 4)
        self._button("Move", 8)

    def _build_search(self) -> None:
        self._section("SEARCH BY", 2)
        self._menu(menus=self.MENU["search"], with_colspan=True)
        self._option("search", 4)

        search_icon = icon_image_convert(icon.search, theme.text_secondary, 25)
        ctk.CTkButton(
            master       = self, 
            text         = "Search", 
            height       = 46,
            image        = search_icon,
            fg_color     = theme.action, 
            hover_color  = theme.action_hover,
            command      = self.operation["run_search"]
            ).grid(row=8, column=0, columnspan=2, padx=(6, 0), sticky="ew")

    def _section(self, text: str, row: int) -> None:
        ctk.CTkLabel(
            master     = self, 
            text       = text.upper(), 
            anchor     = "w",
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
            ).grid( row=row, column=0, columnspan=2, padx=18,
                    pady=(18, 8), sticky="ew")

    def _label(self, text: str, row: int, column: int, padx: int | tuple, pady: int | tuple) -> None:
        ctk.CTkLabel(
        master     = self, 
        text       = text, 
        anchor     = "w", 
        text_color = theme.text_primary 
        ).grid(row=row, column=column, padx=padx, pady=pady, sticky="ew")

    def _entry(self, variable: str, row: int, column: int, padx: int | tuple) -> None:
        ctk.CTkEntry(
            master       = self, 
            textvariable = variable, 
            height       = 42,
            fg_color     = theme.background, 
            border_color = theme.border).grid(
            row=row, column=column, padx=padx, sticky="ew")

    def _browse_form(self, text: str, row: int) -> str:

        self._section(text, row)

        folder_row = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        folder_row.grid(row=row+1, column=0, columnspan=2, padx=18, sticky="ew")
        folder_row.grid_columnconfigure(0, weight=1)
        
        entry = ctk.CTkEntry(
            master           = folder_row, 
            height           = 42, 
            placeholder_text = "Select a folder...",
            fg_color         = theme.background, 
            border_color     = theme.border)
        entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        file = _SourceFolder(entry)

        browse_icon = icon_image_convert(icon.browse, theme.text_primary, 25)
        ctk.CTkButton(
            master      = folder_row, 
            text        = "Browse", 
            width       = 95, 
            height      = 42,
            image       = browse_icon,
            text_color  = theme.text_primary,
            fg_color    = theme.action, 
            hover_color = theme.action_hover,          
            command     = lambda: self._browse(entry)).grid(row=0, column=1)
        return file

    def _menu(self, label: list=False, menus: list=False, with_colspan: bool=False) -> None:
        if label:
            for text, row, column, padx, pady in label:
                self._label(text, row, column, padx, pady)

        if not with_colspan:
            for variable, values, row, column, padx in menus:
                ctk.CTkOptionMenu(
                    self, 
                    variable           = variable,
                    values             = values,
                    height             = 42, 
                    fg_color           = theme.panel_light, 
                    button_color       = theme.action,
                    button_hover_color = theme.action_hover
                    ).grid(row=row, column=column, padx=padx, sticky="ew")
        else:
            for variable, values, row in menus:
                ctk.CTkOptionMenu(
                    self, 
                    variable           = variable,
                    values             = values,
                    height             = 42, 
                    fg_color           = theme.panel_light, 
                    button_color       = theme.action,
                    button_hover_color = theme.action_hover
                    ).grid(row=row, column=0, columnspan=2, padx=18, sticky="ew")

    def _option(self, mode: str, row: int) -> None:

        self._section("Options", row)
        for text, variable in self.OPTIONS[mode]:
            row += 1
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

    def _button(self, text: str, row: int) -> None:
        command_preview = self.operation[f"{text.lower()}_preview"]
        command_execute = self.operation[f"{text.lower()}_execute"]
        buttons = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        buttons.grid(row=row, column=0, columnspan=2, padx=18, pady=(28, 18), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)

        preview_icon = icon_image_convert(icon.preview_fill, theme.text_secondary, 25)
        ctk.CTkButton(
            master       = buttons, 
            text         = " Preview", 
            height       = 46,
            fg_color     = "transparent", 
            border_width = 1, 
            image        = preview_icon,
            border_color = theme.action,
            hover_color  = theme.action_disable_hover, 
            text_color   = theme.text_secondary,
            command      = command_preview
            ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        execute_icon = icon_image_convert(icon.execute_fill, theme.text_secondary, 25)
        ctk.CTkButton(
            master       = buttons, 
            text         = text, 
            height       = 46,
            image        = execute_icon,
            fg_color     = theme.action, 
            hover_color  = theme.action_hover,
            command      = command_execute
            ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _browse(self, entry: ctk.CTkEntry) -> None:
        folder = filedialog.askdirectory(title="Select source folder")
        if folder and entry is not None:
            entry.delete(0, "end")
            entry.insert(0, folder)

    def call_back_rename(self) -> dict | None:
        folder = self.source_file.get_folder_path()
        if folder is None:
            return None
        pattern = self.pattern_var.get().strip()
        try:
            start_number = int(self.start_var.get().strip())
            if start_number < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid settings", "Start Number must be a non-negative integer.", parent=self)
            return None
        rename_data = {
                    "folder"        : folder,
                    "extension"     : self.extension_var.get(),
                    "pattern"       : pattern,
                    "quality"       : self.quality_var.get(),
                    "start_number"  : start_number,
                    "number_format" : self.number_format_var.get()
                }
        return rename_data

    def call_back_organize(self) -> dict | None:
        folder = self.source_file.get_folder_path()
        if folder is None:
            return
        
        destination = self.org_destination.get_folder_path()
        if destination is None:
            return
        
        organize_data = {
                    "folder"      : folder,
                    "destination" : destination,
                    "organize_by" : self.organize_by.get(),
                    "recursive"   : self.org_recursive.get()
                }
        return organize_data

    def call_back_copy(self) -> dict | None:
        folder = self.source_file.get_folder_path()
        if folder is None:
            return
        
        destination = self.copy_destination.get_folder_path()
        if destination is None:
            return
        
        copy_data = {
                    "folder"         : folder,
                    "destination"    : destination,
                    "recursive"      : self.copy_recursive.get(),
                    "keep_structure" : self.copy_keep_structure.get(),
                    "overwrite"      : self.copy_overwrite.get()
                }
        return copy_data

    def call_back_move(self) -> dict | None:
        folder = self.source_file.get_folder_path()
        if folder is None:
            return
        
        destination = self.move_destination.get_folder_path()
        if destination is None:
            return
        
        move_data = {
                    "folder"         : folder,
                    "destination"    : destination,
                    "recursive"      : self.move_recursive.get(),
                    "keep_structure" : self.move_keep_structure.get()
                }
        return move_data

    def call_back_search(self) -> dict | None:
        folder = self.source_file.get_folder_path()
        if folder is None:
            return
                
        search_data = {
                    "folder"          : folder,
                    "query"           : self.search_query.get(),
                    "file_type"       : self.search_by.get(),
                    "recursive"       : self.search_recursive.get(),
                    "case_sensitive"  : self.case_sensitive.get(),
                    "search_contents" : self.search_contents.get(),
                    "modified_within" : self.modified_within
                }
        return search_data


    def _destroy_widgets(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()






