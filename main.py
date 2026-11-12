# main.py
from controller import App
from execution  import ThreadExecutor, ProcessExecutor
from frontend   import MainWindow, Title, Form, View, Status
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

executor = {
    "thread"  : ThreadExecutor,
    "process" : ProcessExecutor}

# Initialization App
def main() -> None:
    app = App(
        main_window  = MainWindow, 
        ui_compounds = ui_compounds, 
        factories    = factories,
        executor     = executor)
    app.run()

# Initialization The Program
if __name__ == "__main__":
    main()
