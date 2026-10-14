# organize.py

from pathlib import Path
import shutil


class Organize:
    CATEGORIES = {
        "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
        "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "Music": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
        "Documents": {
            ".pdf", ".txt", ".doc", ".docx",
            ".xls", ".xlsx", ".ppt", ".pptx",
        },
        "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
        "Applications": {".exe", ".msi", ".bat"},
    }

    def __init__(self, organize_data):
        self.folder      = Path(organize_data["folder"]).expanduser()
        self.organize_by = organize_data["organize_by"]
        self.recursive   = organize_data["recursive"]
        self.destination = Path(organize_data["destination"].expanduser()
                            if organize_data["destination"] else self.folder)

        self.plan = []

    def get_category(self, file):
        if self.organize_by == "Extension":
            return file.suffix[1:].upper() or "No Extension"

        for category, extensions in self.CATEGORIES.items():
            if file.suffix.lower() in extensions:
                return category

        return "Others"

    def create_plan(self):
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        paths = (
            self.folder.rglob("*")
            if self.recursive
            else self.folder.iterdir()
        )

        self.plan = []

        for source in sorted(paths, key=lambda p: str(p).lower()):
            if not source.is_file():
                continue

            category = self.get_category(source)
            destination = (
                self.destination / category / source.name
            )
            if source.resolve() == destination.resolve():
                status = "Skipped"
            elif destination.exists():
                status = "Exist"
            else:
                status = "Ready"

            self.plan.append({
                "source": source,
                "destination": destination,
                "old_name": source.name,
                "new_name": f"{category}/{source.name}",
                "status": status,
                "message": "",
            })

        return self.plan

    def organize_files(self):
        for item in self.plan:
            if item["status"] != "Ready":
                continue

            try:
                item["destination"].parent.mkdir(
                    parents=True, exist_ok=True
                )

                if item["destination"].exists():
                    item["status"] = "Exist"
                    continue

                shutil.move(
                    str(item["source"]),
                    str(item["destination"]),
                )
                item["status"] = "Organized"

            except OSError as error:
                item["status"] = "Error"
                item["message"] = str(error)

        return self.plan