import customtkinter    as     ctk
import config.theme     as     theme
import config.icon      as     icon
from   utils.file_utils import icon_image_convert
from   tkinter          import filedialog, messagebox


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
        
        self.pattern_var        = ctk.StringVar(value="Episode")
        self.start_var          = ctk.StringVar(value="1")
        self.number_format_var  = ctk.StringVar(value="01 (Two Digits)")
        self.extension_var      = ctk.StringVar(value=".mp4")
        self.quality_var        = ctk.StringVar(value="1080p")
         
        self.skip_same_var      = ctk.BooleanVar(value=True)
        self.video_only_var     = ctk.BooleanVar(value=True)
 
        self.create_fold_auto   = ctk.BooleanVar(value=True)
        self.include_files_subf = ctk.BooleanVar(value=True)
 
        self.create_nonexist_folder = ctk.BooleanVar(value=True)
        self.move_emp_folder    = ctk.BooleanVar(value=True)
        
        self.copy_not_move      = ctk.BooleanVar(value=True)
        self.include_subf       = ctk.BooleanVar(value=True)
        self.keep_ori_file_str  = ctk.BooleanVar(value=True)

        self.case_sensitive     = ctk.BooleanVar(value=True)
        self.sear_file_contents = ctk.BooleanVar(value=True)


        self.OPTIONS = {
        "rename"  : (("Skip files with the same name", self.skip_same_var), ("Show only video files", self.video_only_var)),
        "organize": (("Create folders automatically", self.create_fold_auto), ("Include files in subfolders" , self.include_files_subf)),
        "move"    : (("Create destination folder if it doesn’t exist", self.create_nonexist_folder), ("Move empty folders" , self.move_emp_folder), ("Keep original folder structure", self.keep_ori_file_str)),
        "copy"    : (("Copy files (not move)", self.copy_not_move), ("Include subfolders" , self.include_subf), ("Keep original file structure", self.keep_ori_file_str)),
        "search"  : (("Include subfolders", self.include_files_subf), ("Case sensitive" , self.case_sensitive), ("Search file contents (slower)", self.sear_file_contents))
 }


        self._build_1()
        self._build_2("rename")



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
            command     = self._browse).grid(row=0, column=1)


    def _build_2(self, current_mode):
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

        self.button("Rename", None, 12)

    def _build_organize(self):
        self._section("ORGANIZE BY", 2)
        ctk.CTkOptionMenu(
            master             = self, 
            values             = ["File Type","File Extension","Date Modified"], 
            height             = 46, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
            row=3, column=0, padx=18, columnspan=2, sticky="ew")

        info_icon = icon_image_convert(icon.info, theme.text_primary, 15)
        ctk.CTkLabel(
            master     = self, 
            text       = " Files will be sorted into folders based on their type.", 
            image      = info_icon,
            compound   = "left",
            anchor     = "w", 
            text_color = theme.text_primary
            ).grid(
            row=4, column=0, padx=(18, 6), pady=(0, 5), columnspan=2, sticky="ew")

        self._section("DESTINATION", 5)
        ctk.CTkOptionMenu(
            master             = self, 
            values             = ["Same Folder","New Folder"], 
            height             = 46, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
            row=6, column=0, padx=18, columnspan=2, sticky="ew")

        self.option("organize", 7)
            
        self.button("Organize", None, 10)
            
    def _build_move(self):
        self._section("DESTINATION FOLDER", 2)

        destination_row = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        destination_row.grid(row=3, column=0, columnspan=2, padx=18, sticky="ew")
        destination_row.grid_columnconfigure(0, weight=1)
        
        self.destination_entry = ctk.CTkEntry(
            master           = destination_row, 
            height           = 42, 
            placeholder_text = "Select a folder...",
            fg_color         = theme.background, 
            border_color     = theme.border)
        self.destination_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        self.destination_file = _SourceFolder(self.destination_entry)

        browse_icon = icon_image_convert(icon.browse, theme.text_primary, 25)
        ctk.CTkButton(
            master      = destination_row, 
            text        = "Browse", 
            width       = 95, 
            height      = 42,
            image       = browse_icon,
            text_color  = theme.text_primary,
            fg_color    = theme.action, 
            hover_color = theme.action_hover,          
            command     = self._browse).grid(row=0, column=1)

        self.option("move",4)
        
        self.button("Move", None, 8)

    def _build_copy(self):
        self._section("DESTINATION FOLDER", 2)

        destination_row = ctk.CTkFrame(
            master   = self, 
            fg_color = "transparent")
        destination_row.grid(row=3, column=0, columnspan=2, padx=18, sticky="ew")
        destination_row.grid_columnconfigure(0, weight=1)
        
        self.destination_entry = ctk.CTkEntry(
            master           = destination_row, 
            height           = 42, 
            placeholder_text = "Select a folder...",
            fg_color         = theme.background, 
            border_color     = theme.border)
        self.destination_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        self.destination_file = _SourceFolder(self.destination_entry)

        browse_icon = icon_image_convert(icon.browse, theme.text_primary, 25)
        ctk.CTkButton(
            master      = destination_row, 
            text        = "Browse", 
            width       = 95, 
            height      = 42,
            image       = browse_icon,
            text_color  = theme.text_primary,
            fg_color    = theme.action, 
            hover_color = theme.action_hover,          
            command     = self._browse).grid(row=0, column=1)

        self.option("copy",4)
        
        self.button("Copy", None, 8)

    def _build_search(self):
        self._section("SEARCH BY", 2)
        ctk.CTkOptionMenu(
            master             = self, 
            values             = ["All Files","Video","Image","Audio","Document","Archive","Other"], 
            height             = 46, 
            fg_color           = theme.panel_light, 
            button_color       = theme.action,
            button_hover_color = theme.action_hover
            ).grid(
            row=3, column=0, padx=18, columnspan=2, sticky="ew")

        self.option("search", 4)
            
        self.button("Search", None, 8)

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
            



    def button(self, text, command, row):
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
            command      = self._preview
            ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        execute_icon = icon_image_convert(icon.execute_fill, theme.text_secondary, 25)
        ctk.CTkButton(
            master       = buttons, 
            text         = text, 
            height       = 46,
            image        = execute_icon,
            fg_color     = theme.action, 
            hover_color  = theme.action_hover,
            command      = command
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

    def change_form(self, mode):
        self._destroy_widgets()
        self._build_1()
        self._build_2(mode)

    def _destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _preview(self):
        self.on_preview()

    def _rename(self):
        self.on_rename()

    def organize_test(self):

        self.section_label(opts,"File Type"); ctk.CTkComboBox(opts,values=["All Files","Video","Image","Audio","Document","Archive","Other"],height=46,fg_color="#06203A",border_color="#16649B").pack(fill="x",padx=18)

        self.section_label(opts,"Additional Options"); self.checkbox(opts,"Include subfolders"); self.checkbox(opts,"Case sensitive"); self.checkbox(opts,"Search file contents (slower)"); button(opts,"⌕  Search",lambda: app.footer_status.configure(text="Search complete"),200,True).pack(fill="x",padx=18,pady=20)

        pass