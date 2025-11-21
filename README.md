# Library Rollout

This repository contains a Python script for synchronizing library types between a Project Library and a Global Library in Siemens TIA Portal.

## Prerequisites

- **Python 3.x**
- **Siemens TIA Portal** (v20.0 or compatible)
- **TIA Openness / TIA Scripting** enabled and installed.

### Dependencies

The script relies on the `siemens_tia_scripting` library, which is part of the Siemens TIA Portal Openness ecosystem. Ensure this library is available in your Python environment or that the path to its binaries is correctly configured.

`tkinter` is used for the GUI and is typically included with standard Python installations.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install Development Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

**Note:** The current version of the script (`src/LibraryRollout.py`) contains hardcoded paths.

To run the script, you may need to manually update the `tia_scripting_directory` variable in `src/LibraryRollout.py` to point to your local TIA Scripting binaries folder.

```python
# src/LibraryRollout.py

# !!! UPDATE THIS PATH !!!
tia_scripting_directory = r"C:\Path\To\Your\TIA_Scripting_Python_Binaries"
```

### Future Improvements
A `.env.example` file is provided to suggest a future configuration method using environment variables.

## Usage

Run the script using Python:

```bash
python src/LibraryRollout.py
```

The script will:
1. Attempt to attach to a running TIA Portal instance.
2. Open a GUI to select a Global Library.
3. Compare library types between the Project Library and the selected Global Library.
4. Prompt to update any mismatched types.

## Development

### Linting and Formatting

This project uses `black` for formatting and `flake8` for linting.

To check formatting:
```bash
black --check src
```

To run linter:
```bash
flake8 src
```
