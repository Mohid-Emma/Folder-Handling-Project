# Perfect GUI — File & Folder Manager

A Python desktop application for managing files and folders through a modern, dark-themed graphical interface. **Perfect GUI** is being developed with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), with a focus on a clean user experience and a maintainable, object-oriented codebase.

> **Project status:** In development. Some tools and workflows may still be incomplete.

## Overview

Perfect GUI aims to bring common file-management tasks into one place. Instead of working through separate scripts, users can select a source folder, review an operation, and then run it from the interface.

The interface uses a dark navy-blue palette, blue action accents, reusable widgets, and a central controller to coordinate the frontend and file-operation logic.

## Planned tools

- **Rename** — rename multiple files using a naming pattern.
- **Organize** — sort files into folders based on file type.
- **Move** — move selected files to a destination folder.
- **Copy** — copy selected files to a destination folder.
- **Search** — find files using a category or file type filter.

These describe the intended feature set; availability may vary while the project is being developed.

## Design goals

- A consistent, modern desktop interface.
- Separation between UI widgets, application flow, and file-system operations.
- Reusable frontend components and shared theme/icon configuration.
- Preview and status feedback so users can understand an operation before running it.
- Small, incremental improvements that keep the code understandable and testable.

## Tech stack

- **Python** — application logic.
- **CustomTkinter** — desktop GUI widgets.
- **Tkinter** — native dialogs and supporting GUI functionality.
- **Pathlib / Python file-system utilities** — path and file handling where appropriate.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Mohid-Emma/Folder-Handling-Project.git
cd Folder-Handling-Project
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

If the repository includes a `requirements.txt`, install its listed dependencies:

```bash
python -m pip install -r requirements.txt
```

If no dependency file is present, install the GUI library:

```bash
python -m pip install customtkinter
```

The project may use additional packages for icons or other UI utilities; install those according to the imports used by the current version of the code.

### 4. Run the application

From the project root:

```bash
python main.py
```

If the application reports a missing module, check the dependency list and make sure you are running the command from the repository root.

## Project structure

The project separates file operations, interface components, configuration, and application coordination.

```text
Folder-Handling-Project/
├── backend/       # File-operation logic
├── config/        # Theme, icons, and configuration
├── frontend/      # Main window, views, widgets, and dialogs
├── utils/         # Shared helper functions
├── controller.py  # Coordinates UI events and backend operations
├── main.py        # Application entry point
└── README.md
```

The exact contents of each folder may change as the project evolves.

## Safety and workflow

File operations can affect real files. Before using the application on important data:

1. Test with a temporary folder and sample files.
2. Review the preview or planned changes when available.
3. Confirm the source and destination folders before moving, copying, or renaming files.
4. Keep a separate backup of important data.

## Development approach

The project is built incrementally: implement one operation, connect it to the controller, test the UI and backend, then refine the design before moving on to the next operation.

## Contributing

Ideas, bug reports, and improvements are welcome. Before proposing a change, describe the issue or feature and keep changes focused so they are easier to review.

1. Fork the repository.
2. Create a branch for your change.
3. Make and test the change.
4. Open a pull request with a short explanation of what changed.

## Author

Created and maintained by **Mohid Younas**.

- GitHub: [@Mohid-Emma](https://github.com/Mohid-Emma)
- Repository: [Folder-Handling-Project](https://github.com/Mohid-Emma/Folder-Handling-Project)

---

*Perfect GUI — making everyday file management clearer, more organized, and easier to use.*
