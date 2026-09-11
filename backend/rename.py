# rename.py 

from pathlib import Path

class Rename:
    def __init__(self, folder):
        self.folder      = Path(folder)
        self.rename_plan = []

    def create_rename_folder(self):
        self.rename_plan = []
        for i, item in enumerate(self.folder.glob("*.mp4"), start=1):

            new_name = self.folder / f"EP.{i:02}.v0.720p.mp4"

            if new_name.exists():
                self.rename_plan.append((item, new_name, False))
            else:
                self.rename_plan.append((item, new_name, True))

        return self.rename_plan

    def rename_files(self):
        try:
            for old_name, new_name, status in self.rename_plan:
                if status:
                    old_name.rename(new_name)
            return True
        except OSError:
            return False
        


