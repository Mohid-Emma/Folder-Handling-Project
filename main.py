# main.py
from controller import App
from backend    import Rename, Organize, Copy, Move, Search

factory = {
    "rename"   : Rename,
    "organize" : Organize,
    "copy"     : Copy,
    "move"     : Move,
    "search"   : Search }

# Initialization App
def main():
    app = App(factory)
    app.run()

# Initialization The Program
if __name__ == "__main__":
    main()
