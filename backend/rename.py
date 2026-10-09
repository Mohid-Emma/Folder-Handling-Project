# rename.py 

from pathlib import Path


class Rename:
    def __init__(
        self,
        folder,
        extension=".mp4",
        pattern=None,
        quality="1080p",
        start_number=1,
        number_format=2,
    ):
        self.folder        = Path(folder).expanduser()
        self.extension     = extension
        self.pattern       = pattern
        self.quality       = quality
        self.start_number  = int(start_number)
        self.number_format = number_format

        self.rename_plan  = []
        self.file_count   = 0
        self.rename_count = 0

    def create_rename_folder(self):
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        extension = self.extension.lower()
        files = sorted(
            (p for p in self.folder.iterdir()
                if p.is_file() and (
                    extension in ("*", "all files")
                    or p.suffix.lower() == extension)
            ),key=lambda p: p.name.lower(),)

        self.file_count = len(files)
        self.rename_count = 0
        self.rename_plan = []

        for number, source in enumerate(
            files, start=self.start_number
        ):
            if self.pattern:
                name_pattern = f"{self.pattern}{number}{self.extension}"
                name = name_pattern.format(
                    i=number,
                    number=number,
                    quality=self.quality,
                )
            else:
                width = int(self.numberformat())
                name = f"EP.{number:0{width}d}.v0.{self.quality}"

            destination = source.with_name(
                name + source.suffix
            )

            if source == destination:
                status = "Skipped"
            elif destination.exists():
                status = "Exist"
            else:
                status = "Ready"

            self.rename_plan.append({
                "source"     : source,
                "destination": destination,
                "old_name"   : source.name,
                "new_name"   : destination.name,
                "status"     : status,
                "message"    : "",
            })

        return self.rename_plan

    def rename_files(self):
        ready = [
            item for item in self.rename_plan
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

            return self.rename_plan

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
    def numberformat(self):
            if self.number_format == "1 (Normal)":
                return "01"
            elif self.number_format == "01 (Two Digits)":
                return "02"
            elif self.number_format == "001 (Three Digits)":
                return "03"
            else:
                return "02"
            

    def check_result(self):
        skipped = sum(
            item["status"] in ("Skipped", "Exist")
            for item in self.rename_plan
        )
        failed = sum(
            item["status"] == "Error"
            for item in self.rename_plan
        )

        return {
            "total": self.file_count,
            "renamed": self.rename_count,
            "skipped": skipped,
            "failed": failed,
            "extension": self.extension,
        }
        