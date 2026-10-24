# main.py
from controller import App
from frontend   import MainWindow
from frontend   import Title, Form, View, Status
from backend    import Rename, Organize, Copy, Move, Search

ui_compounds = {
    "title"  : Title,
    "form"   : Form,
    "view"   : View,
    "status" : Status }

factories = {
    "rename"   : Rename,
    "organize" : Organize,
    "copy"     : Copy,
    "move"     : Move,
    "search"   : Search }

# Initialization App
def main() -> None:
    app = App(
        main_window  = MainWindow, 
        ui_compounds = ui_compounds, 
        factories    = factories)
    app.run()

# Initialization The Program
if __name__ == "__main__":
    main()
