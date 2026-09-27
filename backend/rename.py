# rename.py 

from pathlib import Path

class Rename:
    def __init__(self, folder, extension, pattern, quality):
        self.folder         = Path(folder)
        self.rename_plan    = []
        self.rename_count   = 0
        self.folder_count   = 0
        
        self.extension = extension
        self.pattern   = pattern
        self.quality   = quality

    def create_rename_folder(self):
        self.rename_plan  = []
        self.folder_count = 0
        print(self.extension)
        for i, item in enumerate(self.folder.glob(f"*{self.extension}"), start=1):

            self.folder_count += 1
            new_base_name = self.pattern.format(i=i)
            #new_name = self.folder / f"EP.{i:02}.v0.720p.mp4"
            new_name = self.folder / f"{new_base_name}{self.extension}"

            if new_name.exists():
                self.rename_plan.append([item, new_name, "Exist"])
            else:
                self.rename_plan.append([item, new_name, "Ready"])

        return self.rename_plan

    def rename_files(self):
        self.rename_count = 0
        try:
            for rename_item in self.rename_plan:
                old_name, new_name, status = rename_item

                if status == "Ready":
                    old_name.rename(new_name)
                    rename_item[2] = "Finished"
                    self.rename_count += 1
            return True, None, self.rename_plan
        except OSError as e:
            return False, e, self.rename_plan

    def check_result(self):
        if self.rename_count > 0:
            return "renamed", self.rename_count
        elif self.folder_count == 0:
            return "empty", None
        else:
            return "skipped", None
