# rename.py 

from pathlib import Path


class Rename:
    def __init__(self, folder, extension, pattern, quality, start_number, number_foramt):
        self.folder       = Path(folder)
        self.rename_plan  = []
        self.rename_count = 0
        self.file_count   = 0
        self.status       = None
        
        self.extension     = extension
        self.pattern       = pattern
        self.quality       = quality
        self.start_number  = start_number
        self.number_foramt = number_foramt

    # Create Rename Plan
    def create_rename_folder(self): 
        self.rename_plan  = []
        self.file_count = 0

        for i, item in enumerate(self.folder.glob(f"*{self.extension}"), start=int(self.start_number)):

            self.file_count += 1
            if self.pattern:
                new_base_name = self.pattern.format(i=i)
                new_name = self.folder / f"{new_base_name}{self.extension}"
            else:
                width = int(self.number_foramt)
                new_base_name = f"{i:0{width}d}"
                new_name = self.folder / f"EP.{new_base_name}.v0.{self.quality}{self.extension}"

            if new_name.exists():
                self.rename_plan.append([item, new_name, "Exist"])
            else:
                self.rename_plan.append([item, new_name, "Ready"])
        if not self.rename_plan:
            return None
        return self.rename_plan

    # Rename Files
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

    # Check Outcome of the Rename Files
    def check_result(self):
        if self.rename_count > 0:
            status = "renamed"
        elif self.file_count == 0:
            status = "empty"
        else:
            status = "skipped"

        return self.file_count, status, self.rename_count, self.extension