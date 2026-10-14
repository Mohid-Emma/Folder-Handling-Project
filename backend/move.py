# move.py

from pathlib import Path
import shutil


class Move:
    def __init__(self, move_date):
        self.folder         = Path(move_date["folder"]).expanduser()
        self.destination    = Path(move_date["destination"]).expanduser()
        self.recursive      = move_date["recursive"]
        self.keep_structure = move_date["keep_structure"]
        self.plan = []

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
                else "Exist" if destination.exists() else "Ready"
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

    def move_files(self):
        for item in self.plan:
            if item["status"] != "Ready":
                continue

            try:
                destination = item["destination"]
                destination.parent.mkdir(
                    parents=True, exist_ok=True
                )

                if destination.exists():
                    item["status"] = "Exist"
                    continue

                shutil.move(str(item["source"]), str(destination))
                item["status"] = "Moved"

            except OSError as error:
                item["status"] = "Error"
                item["message"] = str(error)

        return self.plan