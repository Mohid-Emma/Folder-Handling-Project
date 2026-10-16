# copy.py

from pathlib import Path
import shutil


class Copy:
    def __init__(self, copy_data):
        self.folder         = Path(copy_data["folder"]).expanduser()
        self.destination    = Path(copy_data["destination"]).expanduser()
        self.recursive      = copy_data["recursive"]
        self.keep_structure = copy_data["keep_structure"]
        self.overwrite      = copy_data["overwrite"]
        self.plan           = []

    def create_plan(self):
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        if (
            self.recursive
            and self.destination.resolve()
            in self.folder.resolve().parents
        ):
            raise ValueError(
                "Destination cannot be inside the source folder."
            )

        paths = (
            self.folder.rglob("*")
            if self.recursive
            else self.folder.iterdir()
        )

        self.plan = []

        for source in sorted(paths, key=lambda p: str(p).lower()):
            if not source.is_file():
                continue

            relative = (
                source.relative_to(self.folder)
                if self.keep_structure
                else Path(source.name)
            )
            destination = self.destination / relative

            status = (
                "Skipped"
                if source.resolve() == destination.resolve()
                else (
                    "Exist"
                    if destination.exists() and not self.overwrite
                    else "Ready"
                )
            )

            self.plan.append({
                "source": source,
                "destination": destination,
                "old_name": source.name,
                "new_name": str(relative),
                "status": status,
                "message": "",
            })

        return self.plan

    def copy_files(self):
        for item in self.plan:
            if item["status"] != "Ready":
                continue

            try:
                destination = item["destination"]
                destination.parent.mkdir(
                    parents=True, exist_ok=True
                )

                if destination.exists() and not self.overwrite:
                    item["status"] = "Exist"
                    continue

                shutil.copy2(item["source"], destination)
                item["status"] = "Copied"

            except OSError as error:
                item["status"] = "Error"
                item["message"] = str(error)

        return self.plan