# main.py
from controller import App
from frontend   import Title, Form, View, Status
from backend    import Rename, Organize, Copy, Move, Search

display = {
    "title"  : Title,
    "form"   : Form,
    "view"   : View,
    "status" : Status }

factory = {
    "rename"   : Rename,
    "organize" : Organize,
    "copy"     : Copy,
    "move"     : Move,
    "search"   : Search }

# Initialization App
def main() -> None:
    app = App(display, factory)
    app.run()

# Initialization The Program
if __name__ == "__main__":
    main()
