# app.py

from backend.rename       import Rename
from frontend.main_window import MainWindow



class App:
    def __init__(self):
        self.rename = None

        self.window = MainWindow(
            on_folder_selected = self.set_folder,
            on_preview         = self.set_preview,
            on_rename          = self.set_rename_files)
                

    def set_folder(self, folder):
        self.rename = Rename(folder)

    def set_preview(self):
        if self.rename:
            rename_plan = self.rename.create_rename_folder()
            self.window.show_preview(rename_plan)

    def set_rename_files(self):
        if self.rename:
            success = self.rename.rename_files()
            self.window.show_status(success)


    def run(self):
        self.window.mainloop()
