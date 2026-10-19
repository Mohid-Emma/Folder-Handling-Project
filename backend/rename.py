# rename.py 

from pathlib import Path


class Rename:
    numberformat = {
                "1 (Normal)"         : "01",
                "01 (Two Digits)"    : "02",
                "001 (Three Digits)" : "03" }
    
    def __init__(self, rename_data):
        self.folder        = Path(rename_data["folder"]).expanduser()
        self.extension     = rename_data["extension"]
        self.pattern       = rename_data["pattern"]
        self.quality       = rename_data["quality"]
        self.start_number  = int(rename_data["start_number"])
        self.number_format = rename_data["number_format"]

        self.plan  = []
        self.file_count   = 0
        self.rename_count = 0

    def create_plan(self):
        self.rename_count = 0
        self.plan = []
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        extension = self.extension.lower()
        files = sorted(
            (file for file in self.folder.iterdir() 
            if file.is_file() and 
            (extension in ("*", "all files") or file.suffix.lower() == extension)
            ),key=lambda file: file.name.lower())

        self.file_count = len(files)


        for number, source in enumerate(files, start=self.start_number):
            if self.pattern:
                name_pattern = f"{self.pattern}{number}"
                name = name_pattern.format(
                    i=number,
                    number=number,
                    quality=self.quality,
                )
            else:
                width = int(self.numberformat[self.number_format])
                name = f"EP.{number:0{width}d}.v0.{self.quality}"

            destination = source.with_name(
                name + source.suffix )
            
            if source == destination:
                status = "Skipped"
            elif destination.exists():
                status = "Exist"
            else:
                status = "Ready"
                self.rename_count += 1

            self.plan.append({
                "source"     : source,
                "destination": destination,
                "old_name"   : source.name,
                "new_name"   : destination.name,
                "status"     : status,
                "message"    : "", })

        return self.plan


    def rename_files(self):
        ready = [
            item for item in self.plan
            if item["status"] == "Ready"
        ]

        # Detect duplicate destinations.
        destinations = [item["destination"] for item in ready]
        if len(destinations) != len(set(destinations)):
            raise ValueError(
                "Multiple files have the same destination name."
            )

        staged = []
        self.rename_count = 0

        try:
            # Stage all sources first, allowing safe filename swaps.
            for index, item in enumerate(ready):
                temp = item["source"].with_name(
                    f".__rename_temp_{index}_{item['source'].name}"
                )

                if temp.exists():
                    raise FileExistsError(temp)

                item["source"].rename(temp)
                staged.append((item, temp))

            # Move staged files to their final destinations.
            for item, temp in staged:
                destination = item["destination"]

                if destination.exists():
                    raise FileExistsError(destination)

                temp.rename(destination)
                item["status"] = "Finished"
                item["message"] = ""
                self.rename_count += 1

            return self.plan

        except OSError as error:
            # Best-effort rollback for files still in temporary names.
            for item, temp in reversed(staged):
                if temp.exists():
                    try:
                        temp.rename(item["source"])
                    except OSError as rollback_error:
                        item["status"] = "Error"
                        item["message"] = str(rollback_error)

            for item in ready:
                if item["status"] == "Ready":
                    item["status"] = "Error"
                    item["message"] = str(error)

            raise
