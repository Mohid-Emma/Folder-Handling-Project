# controller.py

from backend.rename       import Rename
from frontend.main_window import MainWindow

class App:
    def __init__(self):
        self.rename = None

        self.main_window = MainWindow(
            on_folder  = self.set_folder,
            on_preview = self.set_preview,
            on_rename  = self.set_rename_files,
            on_result  = self.show_result)
    
    # Sent Data to Rename Class
    def set_folder(self, folder, extention, pattern, quality,start_number, number_foramt):
        self.rename = Rename(folder, extention, pattern, quality, start_number, number_foramt)

    # Sent Data To Window For Preview
    def set_preview(self):
        if self.rename:
            rename_plan = self.rename.create_rename_folder()
            self.main_window.show_preview(rename_plan)

    # Sent Rename Plan And Status of the Results
    def set_rename_files(self):
        rename_plan = None
        
        if self.rename:
            success, error, rename_plan = self.rename.rename_files()
            if success:
                status, data = self.rename.check_result()
                self.main_window.show_status(status, data)
            else:
                self.main_window.show_status("error", error)
        return rename_plan

    # Sent Data To Window For Show Results
    def show_result(self, rename_plan):
        if rename_plan is not None:
            self.main_window.show_preview(rename_plan)

    # Run The CTK 
    def run(self):
        self.main_window.mainloop()
