# search.py

from pathlib import Path
from datetime import datetime


class Search:
    TEXT_EXTENSIONS = {
        ".txt", ".md", ".csv", ".json", ".py",
        ".html", ".xml", ".log",
    }

    def __init__(self, search_data):

        self.folder          = Path(search_data["folder"]).expanduser()
        self.query           = search_data["query"]
        self.file_type       = search_data["file_type"]
        self.recursive       = search_data["recursive"]
        self.case_sensitive  = search_data["case_sensitive"]
        self.search_contents = search_data["search_contents"]
        self.modified_within = search_data["modified_within"]
        self.results = []

    def search_files(self):
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        query = self.query
        if not self.case_sensitive:
            query = query.casefold()

        cutoff = None
        if self.modified_within is not None:
            cutoff = (
                datetime.now().timestamp()
                - int(self.modified_within) * 86400
            )

        paths = (
            self.folder.rglob("*")
            if self.recursive
            else self.folder.iterdir()
        )

        self.results = []

        for path in paths:
            if not path.is_file():
                continue
            file_type = self.file_type.strip()
            if file_type.lower() not in ("all files", "*", ".*"):
                extension = (
                    file_type if file_type.startswith(".")
                    else "." + file_type
                )
                if path.suffix.lower() != extension.lower():
                    continue

            name = (
                path.name if self.case_sensitive
                else path.name.casefold()
            )
            matched = not query or query in name

            # Limit content searching to known text formats.
            if (
                not matched
                and query
                and self.search_contents
                and path.suffix.lower() in self.TEXT_EXTENSIONS
            ):
                try:
                    content = path.read_text(
                        encoding="utf-8", errors="ignore"
                    )[:1_000_000]

                    if not self.case_sensitive:
                        content = content.casefold()

                    matched = query in content

                except OSError:
                    pass

            if not matched:
                continue

            try:
                stat = path.stat()

                if cutoff and stat.st_mtime < cutoff:
                    continue

                self.results.append({
                    "source": path,
                    "destination": path,
                    "old_name": path.name,
                    "new_name": str(path.parent),
                    "status": "Found",
                    "message": "",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(
                        stat.st_mtime
                    ),
                })

            except OSError:
                # A file may disappear while searching.
                continue

        return self.results