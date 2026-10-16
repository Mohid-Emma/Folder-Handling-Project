
# search.py

from pathlib import Path
from datetime import datetime


class Search:
    TEXT_EXTENSIONS = {
        ".txt", ".md", ".csv", ".json", ".py",
        ".html", ".xml", ".log", ".css", ".js",
        ".yaml", ".yml", ".ini", ".cfg", ".toml",
        ".sql", ".rtf",
    }

    FILE_TYPES = {
        "all files": None,

        "video": {
            ".mp4", ".mkv", ".avi", ".mov", ".wmv",
            ".flv", ".webm", ".m4v", ".mpeg", ".mpg",
            ".3gp", ".ts", ".mts", ".m2ts", ".vob",
        },

        "image": {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp",
            ".webp", ".svg", ".ico", ".tiff", ".tif",
            ".heic", ".heif", ".avif", ".raw", ".psd",
        },

        "audio": {
            ".mp3", ".wav", ".aac", ".flac", ".ogg",
            ".wma", ".m4a", ".opus", ".aiff", ".mid",
            ".midi", ".amr",
        },

        "document": {
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".ppt", ".pptx", ".txt", ".rtf", ".odt",
            ".ods", ".odp", ".md", ".csv", ".epub",
            ".json", ".xml",
        },

        "archive": {
            ".zip", ".rar", ".7z", ".tar", ".gz",
            ".tar.gz", ".tgz", ".bz2", ".tar.bz2",
            ".xz", ".tar.xz", ".lz", ".lzma",
            ".zst", ".cab", ".iso", ".arj",
        },
    }

    def __init__(self, search_data):
        self.folder = Path(search_data["folder"]).expanduser()

        self.query           = search_data["query"]
        self.file_type       = search_data["file_type"]
        self.recursive       = search_data["recursive"]
        self.case_sensitive  = search_data["case_sensitive"]
        self.search_contents = search_data["search_contents"]
        self.modified_within = search_data["modified_within"]

        self.results = []

    @classmethod
    def _known_extensions(cls):
        return {
            extension
            for category, extensions in cls.FILE_TYPES.items()
            if category != "all files" and extensions
            for extension in extensions
        }

    def _matches_file_type(self, path):
        file_type = str(self.file_type).strip().casefold()
        filename = path.name.casefold()

        # All files
        if file_type in ("all files", "*", ".*", ""):
            return True

        # Specific extension, including compound extensions
        if file_type.startswith("."):
            return filename.endswith(file_type)

        # Category selected in the GUI
        extensions = self.FILE_TYPES.get(file_type)

        if extensions is not None:
            return any(
                filename.endswith(extension)
                for extension in extensions
            )

        # Other means extensions not covered by known categories
        if file_type == "other":
            return not any(
                filename.endswith(extension)
                for extension in self._known_extensions()
            )

        # Also allow a custom extension without a leading dot
        return filename.endswith("." + file_type)

    def _matches_content(self, path, query):
        if not self.search_contents or not query:
            return False

        # Avoid reading known binary formats as text.
        if path.suffix.casefold() not in self.TEXT_EXTENSIONS:
            return False

        try:
            with path.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                content = file.read(1_000_000)

            if not self.case_sensitive:
                content = content.casefold()

            return query in content

        except (OSError, UnicodeError):
            return False

    def search_files(self):
        if not self.folder.is_dir():
            raise NotADirectoryError(self.folder)

        query = str(self.query).strip()

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
            try:
                if not path.is_file():
                    continue

                if not self._matches_file_type(path):
                    continue

                # Check the filename first.
                name = (
                    path.name
                    if self.case_sensitive
                    else path.name.casefold()
                )

                matched = not query or query in name

                # If the filename doesn't match, check text content.
                if not matched:
                    matched = self._matches_content(path, query)

                if not matched:
                    continue

                stat = path.stat()

                # Filter by modification date.
                if (
                    cutoff is not None
                    and stat.st_mtime < cutoff
                ):
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
                # Skip files that cannot be accessed or disappear.
                continue

        return self.results
