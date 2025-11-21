# Library Rollout Script Documentation

## Overview

The `LibraryRollout.py` script is an automation tool designed for **Siemens TIA Portal** environments. Its primary purpose is to synchronize library types between a currently open **Project Library** and a selected **Global Library**.

It automates the tedious process of checking version mismatches for multiple library types. By leveraging the TIA Portal Openness API (via `siemens_tia_scripting`) and providing a user-friendly GUI (via `tkinter`), it allows engineers to selectively update outdated types in their project, ensuring consistency across automation projects.

---

## Code Breakdown

### Environment Setup & Configuration

```python
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ... (tkinter imports)

# !!! UPDATE THIS PATH !!!
tia_scripting_directory = r"E:\109742322_TIA_Scripting_Python_CODE_V110"

if os.getenv('TIA_SCRIPTING') is None:
    sys.path.append(tia_scripting_directory)
else:
    sys.path.append(os.getenv('TIA_SCRIPTING'))

try:
    import siemens_tia_scripting as ts
except ImportError:
    print("siemens_tia_scripting could not be found")
    sys.exit(1)
```

**Explanation:**
This section sets up the Python environment to interact with the proprietary Siemens TIA Portal API.
1.  **Environment Variables**: It loads variables from a `.env` file, allowing for dynamic configuration of paths.
2.  **Path Modification**: The `siemens_tia_scripting` library is typically not installed in the standard Python site-packages. The script appends the directory containing these binaries to `sys.path` so Python can import them.
3.  **Import Safety**: It wraps the critical import in a `try-except` block to fail gracefully if the API is missing.

* **Best Practice**: Using `os.getenv` allows developers to override the hardcoded path without changing the code, making it CI/CD friendly.
* **Edge Case**: If `tkinter` is missing (common in some minimal Linux installs), the script will exit immediately with a clear error message before attempting complex logic.

---

### GUI: Library Selection

```python
def show_library_selection(available_libraries):
    """
    Displays a Tkinter window with radio buttons for the user to select
    one of the currently open global libraries.
    """
    # ... (Window setup and logic)
    return selected_name
```

**Explanation:**
This function creates a modal dialog requesting the user to choose a "Source of Truth" Global Library.
*   **Input**: A list of string names representing open global libraries in TIA Portal.
*   **Behavior**: Dynamically generates radio buttons for each library. It centers the window on the screen for better UX.
*   **Output**: Returns the selected library name as a string, or `None` if the user cancels.

* **User Experience**: The function handles the window protocol `WM_DELETE_WINDOW` to ensure that closing the window via the "X" button correctly returns `None` rather than crashing or returning an undefined state.

---

### GUI: Update Dialog

```python
def show_update_dialog(mismatch_list):
    """
    Displays a Tkinter window with a scrollable list of checkboxes
    for the user to select which types to update.
    """
    # ... (Scrollable frame setup and logic)
    return selected_guids
```

**Explanation:**
This function presents the comparison results to the user.
*   **Input**: A list of dictionaries, where each dictionary contains details about a mismatched type (Name, Project Version, Global Version, GUID).
*   **Structure**: It uses a `Canvas` and `Scrollbar` to create a scrollable area, which is essential because library mismatches can number in the hundreds.
*   **Output**: Returns a list of GUIDs (Globally Unique Identifiers) for the types the user explicitly chose to update.

* **Performance**: The use of GUIDs for tracking selections is more robust than using names, as names can sometimes be ambiguous or duplicated in different folder structures.

---

### Main Execution Logic

```python
def run_library_rollout():
    # 1. Attach to TIA Portal
    portal = ts.attach_portal(portal_mode=ts.Enums.PortalMode.AnyUserInterface, version="20.0")

    # ... (Get libraries and show selection GUI)

    # 3. Read Project Library & 4. Read Global Library
    # ... (Iterate types and extract default versions)

    # 5. Comparison
    # ... (Compare versions and build mismatch list)

    # 6. Update Action
    global_lib.update_library(
        update_mode=1,
        delete_mode=1,
        conflict_mode=3,
        type_guids=guids_to_update
    )
```

**Explanation:**
This is the orchestrator function that ties everything together:
1.  **Connection**: Attaches to an existing TIA Portal process (specifically targeting v20.0).
2.  **Data Gathering**: Iterates through both the Project Library and the selected Global Library to build a map of `Type Name -> Version`.
3.  **Comparison Engine**: Identifies types that exist in both libraries but have different version numbers.
4.  **Execution**: Calls the `update_library` method on the TIA API.

*   **Technical Insight**: The `update_library` call uses specific integer modes (`1` and `3`). In the context of TIA Openness, these usually correspond to specific behaviors like "Update instances" or "Replace existing".
    *   `update_mode=1`: Typically "Update library types".
    *   `conflict_mode=3`: Likely "Replace" or "Overwrite" in case of conflicts.

---

## Usage Examples

### Basic Execution
Run the script from a terminal where Python has access to the `tkinter` and `siemens_tia_scripting` modules.

```bash
python src/LibraryRollout.py
```

**Expected Behavior:**
1.  **Console Log**:
    ```text
    Attaching to TIA Portal...
    Selected Global Library: Standards_Lib_V2
    Reading Project Library...
    Reading Global Library: Standards_Lib_V2...
    Comparing library types...
      - Mismatch for 'Motor_Block': Project=1.0.0, Global=1.1.0
      - Mismatch for 'Valve_Control': Project=2.0, Global=2.1

    Found 2 types with version mismatches. Showing selection dialog...
    User selected 2 types. Proceeding with update...
    Project update successful.
    Script finished.
    ```
2.  **GUI**: Two windows will appear sequentially. First, to select the library "Standards_Lib_V2". Second, to confirm the update of "Motor_Block" and "Valve_Control".

### Handling Errors
If TIA Portal is not open:
```text
Attaching to TIA Portal...
A critical error occurred: No TIA Portal instance found.
```

---

## Warnings & Gotchas

1.  **Hardcoded Paths**: The variable `tia_scripting_directory` is hardcoded in the script. Ensure this points to the valid location of the Siemens scripting binaries on your machine, or set the `TIA_SCRIPTING` environment variable.
2.  **TIA Portal Version**: The script explicitly requests version `"20.0"` in `ts.attach_portal`. If you are using TIA Portal v18 or v19, you **must** change this string, or the script will fail to attach.
3.  **Tkinter Dependency**: This script relies on `tkinter`. On standard Windows Python installs, this is included. However, on some custom environments or Linux distributions, it might be missing.
4.  **Blocking Operations**: The `update_library` call is synchronous and blocking. For very large updates, the GUI might appear frozen until the operation completes in TIA Portal.
5.  **"IsDefault" Property**: The script only compares the version of the type marked as `IsDefault="True"`. If you are working with non-default versions of types, they will be ignored.
