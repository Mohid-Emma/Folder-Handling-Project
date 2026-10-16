import customtkinter as     ctk
import config.theme  as     theme
import config.icon   as     icon
from   utils         import icon_image_convert
from   tkinter       import filedialog, messagebox


class _SourceFolder:
    def __init__(self, entry):
        self.entry = entry

    def get_folder_path(self):
        return self.entry.get().strip() or None


class Form(ctk.CTkFrame):


    def __init__(self, master, 
                on_rename_preview, on_rename_execute, 
                on_organize_preview, on_organize_execute,  
                on_copy_preview, on_copy_execute, 
                on_move_preview, on_move_execute, 
                on_run_search, 
                **kwargs):
        super().__init__(master, fg_color=theme.panel, corner_radius=10, border_width=1, border_color=theme.border, **kwargs)

        # Rename
        self.on_rename_preview = on_rename_preview
        self.on_rename_execute = on_rename_execute

        # Organize
        self.on_organize_preview = on_organize_preview
        self.on_organize_execute = on_organize_execute

        # Copy
        self.on_copy_preview = on_copy_preview
        self.on_copy_execute = on_copy_execute

        # Move
        self.on_move_preview = on_move_preview
        self.on_move_execute = on_move_execute

        # Search
        self.on_run_search = on_run_search

        # Rename
        self.pattern_var        = ctk.StringVar(value="Episode")
        self.start_var          = ctk.StringVar(value="1")
        self.number_format_var  = ctk.StringVar(value="01 (Two Digits)")
        self.extension_var      = ctk.StringVar(value=".mp4")
        self.quality_var        = ctk.StringVar(value="1080p")

        # Organize
        self.organize_by        = ctk.StringVar(value="File Type")
        self.org_recursive      = ctk.StringVar(value=False)

        # Copy
        self.copy_recursive      = ctk.BooleanVar(value=True)
        self.copy_keep_structure = ctk.BooleanVar(value=True)
        self.copy_overwrite      = ctk.BooleanVar(value=False)

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


        self.skip_same_var      = ctk.BooleanVar(value=True)
        self.video_only_var     = ctk.BooleanVar(value=True)
        self.create_fold_auto   = ctk.BooleanVar(value=True)
        self.create_nonexist_folder = ctk.BooleanVar(value=True)        
        self.copy_not_move      = ctk.BooleanVar(value=True)


        self.OPTIONS = {
        "rename"  : (("Skip files with the same name", self.skip_same_var), ("Show only video files", self.video_only_var)),
        "organize": (("Create folders automatically", self.create_fold_auto), ("Include files in subfolders" , self.org_recursive)),
        "copy"    : (("Copy files (not move)", self.copy_not_move), ("Include subfolders" , self.copy_recursive), ("Keep original file structure", self.copy_keep_structure)),
        "move"    : (("Create destination folder if it doesn’t exist", self.create_nonexist_folder), ("Move empty folders" , self.move_recursive), ("Keep original folder structure", self.move_keep_structure)),
        "search"  : (("Include subfolders", self.search_recursive), ("Case sensitive" , self.case_sensitive), ("Search file contents (slower)", self.search_contents))
 }
        self.change_form("rename")



    def _section(self, text, row):
        ctk.CTkLabel(
            master     = self, 
            text       = text.upper(), 
            anchor     = "w",
            font       = ("Roboto", 13, "bold"),
            text_color = theme.text_secondary
            ).grid( row=row, column=0, columnspan=2, padx=18,
                    pady=(18, 8), sticky="ew")

    def _build(self, current_mode):

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


    def _build_rename(self):
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

        self.option("rename",9)

        self.button("Rename", self.on_rename_preview, self.on_rename_execute, 12)

    def _build_organize(self):

        self.org_destination = self._browse_form("DESTINATION", 2)

        self._section("ORGANIZE BY", 4)
        ctk.CTkOptionMenu(
            master             = self, 
            values             = ["File Type","File Extension","Date Modified"], 
            height             = 46, 
            variable           = self.organize_by,
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
            row=5, column=0, padx=18, columnspan=2, sticky="ew")

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

        self.option("organize", 7)
        self.button("Organize", self.on_organize_preview, self.on_organize_execute, 10)
    
    def _build_copy(self):

        self.copy_destination = self._browse_form("DESTINATION FOLDER", 2)
        self.option("copy",4)
        self.button("Copy", self.on_copy_preview, self.on_copy_execute, 8)
            
    def _build_move(self):
        
        self.move_destination = self._browse_form("DESTINATION FOLDER", 2)
        self.option("move", 4)
        self.button("Move", self.on_move_preview, self.on_move_execute, 8)

    def _build_search(self):
        self._section("SEARCH BY", 2)
        ctk.CTkOptionMenu(
            master             = self, 
            variable           =self.search_by,
            values             = ["All Files","Video","Image","Audio","Document","Archive","Other"], 
            height             = 46, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
            row=3, column=0, padx=18, columnspan=2, sticky="ew")

        self.option("search", 4)

        search_icon = icon_image_convert(icon.search, theme.text_secondary, 25)
        ctk.CTkButton(
            master       = self, 
            text         = "Search", 
            height       = 46,
            image        = search_icon,
            fg_color     = theme.action, 
            hover_color  = theme.action_hover,
            command      = self.on_run_search
            ).grid(row=8, column=0, columnspan=2, padx=(6, 0), sticky="ew")

    def _browse_form(self, text, row):

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
    def option(self, mode, row):

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

    def button(self, text, command_preview, command_execute, row):
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

    def _browse(self, entry):
        folder = filedialog.askdirectory(title="Select source folder")
        if folder and entry is not None:
            entry.delete(0, "end")
            entry.insert(0, folder)

    def call_back_rename(self):
        folder = self.source_file.get_folder_path()
        if folder is None:
            return
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

    def call_back_organize(self):
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

    def call_back_copy(self):
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

    def call_back_move(self):
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

    def call_back_search(self):
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
    
    def change_form(self, mode):
        self._destroy_widgets()
        self._build(mode)

    def _destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()






