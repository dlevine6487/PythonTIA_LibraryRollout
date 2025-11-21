import os
import sys
from dotenv import load_dotenv

load_dotenv()

# --- GUI Library Import ---
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("Error: 'tkinter' library not found. This script requires it to display")
    print("the selection window. Please ensure tkinter is installed with your Python.")
    sys.exit(1)

# --- Set up TIA Scripting path ---
# !!! UPDATE THIS PATH !!!
# Set the path to the folder containing the TIA Scripting Python binaries
# (e.g., C:\Path\To\Your\TIA_Scripting_Python_Binaries).
tia_scripting_directory = r"E:\109742322_TIA_Scripting_Python_CODE_V110"

# NOTE: The global_lib_name placeholder is no longer needed as the user selects it via GUI.
# global_lib_name = "My_Global_Library_Name"


if os.getenv('TIA_SCRIPTING') is None:
    sys.path.append(tia_scripting_directory)
else:
    sys.path.append(os.getenv('TIA_SCRIPTING'))

try:
    import siemens_tia_scripting as ts
except ImportError:
    print("siemens_tia_scripting could not be found")
    sys.exit(1)


#----------------------------------------------------------------
# GUI Function 1: Select Global Library
#----------------------------------------------------------------
def show_library_selection(available_libraries):
    """
    Displays a Tkinter window with radio buttons for the user to select
    one of the currently open global libraries.

    Returns the name of the selected library (str) or None if cancelled.
    """
    selected_name = None

    # --- Window Setup ---
    root = tk.Tk()
    root.title("Select Source Global Library")
    root.geometry("450x300")

    # Center the dialog on the screen for better user experience
    window_width = 450
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


    # --- Header ---
    header_label = ttk.Label(root, text="Select the Global Library for comparison and update:",
                             font=("Arial", 12, "bold"))
    header_label.pack(pady=(20, 10), padx=20)

    # --- Selection Frame ---
    selection_frame = ttk.Frame(root)
    selection_frame.pack(fill="x", padx=20)

    # Variable to hold the selected library name (string)
    radio_var = tk.StringVar()

    # Populate Radio Buttons
    for i, name in enumerate(available_libraries):
        radio = ttk.Radiobutton(selection_frame, text=name, variable=radio_var, value=name)
        radio.pack(anchor="w", pady=2)
        if i == 0:
            radio_var.set(name) # Set the first one as default selected

    # --- Button Logic ---
    def on_select():
        nonlocal selected_name
        selected_name = radio_var.get()
        if not selected_name:
            messagebox.showerror("Selection Error", "Please select a library to proceed.")
            return
        root.destroy() # Close the window

    def on_cancel():
        nonlocal selected_name
        selected_name = None # Ensure a None result on cancel
        root.destroy()

    # --- Buttons Frame ---
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", pady=20, padx=20)

    select_button = ttk.Button(button_frame, text="Proceed with Selection", command=on_select)
    select_button.pack(side="right", padx=(10, 0))

    cancel_button = ttk.Button(button_frame, text="Cancel Script", command=on_cancel)
    cancel_button.pack(side="right")

    # --- Run the GUI ---
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()

    return selected_name


#----------------------------------------------------------------
# GUI Function 2: Select Types to Update (Reused from V3)
#----------------------------------------------------------------
def show_update_dialog(mismatch_list):
    """
    Displays a Tkinter window with a scrollable list of checkboxes
    for the user to select which types to update.

    Returns a list of GUIDs for the selected items.
    """
    selected_guids = []

    # --- Window Setup ---
    root = tk.Tk()
    root.title("Library Version Mismatch - Select Types")
    root.geometry("600x400")

    # --- Header ---
    header_label = ttk.Label(root, text="Select library types to update:", font=("Arial", 12, "bold"))
    header_label.pack(pady=(10, 5), padx=10)

    # --- Scrollable Frame Setup ---
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # --- Populate Checkboxes ---
    checkbox_vars = []

    # Header for the list
    header_text = f"{'Type Name':<30} | {'Project Ver.':<15} | {'Global Ver.':<15}"
    list_header = ttk.Label(scrollable_frame, text=header_text, font=("Courier", 10, "bold"))
    list_header.pack(anchor="w", padx=10, pady=2)
    ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=5, pady=(0,5))

    for item in mismatch_list:
        var = tk.BooleanVar(value=True) # Default to checked

        # Format label text for alignment
        name_display = (item['name'][:28] + '..') if len(item['name']) > 30 else item['name']
        label = f"{name_display:<30} | {item['project_ver']:<15} | {item['global_ver']:<15}"

        cb = ttk.Checkbutton(scrollable_frame, text=label, variable=var, style="TCheckbutton")
        cb.pack(anchor="w", padx=10, fill="x")

        checkbox_vars.append((var, item['guid']))

    # Configure styles for clean look
    s = ttk.Style()
    s.configure("TCheckbutton", font=("Courier", 10))

    # --- Button Logic ---
    def on_update():
        nonlocal selected_guids
        for var, guid in checkbox_vars:
            if var.get(): # If the checkbox is checked
                selected_guids.append(guid)
        root.destroy()

    def on_cancel():
        nonlocal selected_guids
        selected_guids = []
        root.destroy()

    # --- Buttons Frame ---
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", pady=10, padx=10)

    update_button = ttk.Button(button_frame, text="Update Selected", command=on_update)
    update_button.pack(side="right", padx=(10, 0))

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side="right")

    # --- Pack Scrollbar and Canvas ---
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Run the GUI ---
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    root.mainloop()

    return selected_guids

#----------------------------------------------------------------
# Main TIA Script Logic
#----------------------------------------------------------------
def run_library_rollout():
    global_lib_name = None

    try:
        # 1. ATTACH TO TIA PORTAL
        print("Attaching to TIA Portal...")
        portal_mode_ui = ts.Enums.PortalMode.AnyUserInterface
        version = "20.0" # Adjust this version string if necessary
        portal = ts.attach_portal(portal_mode=portal_mode_ui, version=version)

        # Get list of open global libraries to present to the user
        lib_infos = portal.get_global_library_infos()
        if not lib_infos:
            messagebox.showerror("Error", "No Global Libraries are currently open in TIA Portal.")
            return

        available_names = [info.get_name() for info in lib_infos]

        # 2. SHOW LIBRARY SELECTION GUI
        global_lib_name = show_library_selection(available_names)

        if global_lib_name is None:
            print("Library selection cancelled by user.")
            return

        print(f"Selected Global Library: {global_lib_name}")

        # 3. READ PROJECT LIBRARY
        project = portal.get_project()
        print("Reading Project Library...")
        project_lib = project.get_project_library()
        project_lib_types = project_lib.get_types()

        project_lib_versions = {}
        for obj in project_lib_types:
            name = obj.get_name()
            for version in obj.get_versions():
                try:
                    if version.get_property(name="IsDefault") == "True":
                        project_lib_versions[name] = version.get_version_number()
                        break
                except Exception as e:
                    print(f"Error accessing default version for '{name}' in Project Library. Details: {e}")
                    continue

        # 4. READ SELECTED GLOBAL LIBRARY (Source of Truth)
        print(f"Reading Global Library: {global_lib_name}...")
        global_lib = portal.get_global_library(library_name=global_lib_name)

        # Check again in case the library was closed between fetching info and getting the object
        if global_lib is None:
            messagebox.showerror("Error", f"Global Library '{global_lib_name}' could not be opened or found.")
            return

        global_lib_types = global_lib.get_types()

        global_lib_versions = {}
        global_lib_name_to_guid = {}
        for obj in global_lib_types:
            name = obj.get_name()
            guid = obj.get_guid()
            global_lib_name_to_guid[name] = guid

            for version in obj.get_versions():
                try:
                    if version.get_property(name="IsDefault") == "True":
                        global_lib_versions[name] = version.get_version_number()
                        break
                except Exception as e:
                    print(f"Error accessing default version for '{name}' in Global Library. Details: {e}")
                    continue

        # 5. COMPARISON
        print("Comparing library types...")
        common_types = set(project_lib_versions.keys()) & set(global_lib_versions.keys())
        mismatches_details = []

        for name in common_types:
            project_ver = project_lib_versions.get(name)
            global_ver = global_lib_versions.get(name)

            if project_ver != global_ver:
                print(f"  - Mismatch for '{name}': Project={project_ver}, Global={global_ver}")
                type_guid = global_lib_name_to_guid.get(name)

                if type_guid:
                    mismatches_details.append({
                        "name": name,
                        "project_ver": project_ver,
                        "global_ver": global_ver,
                        "guid": type_guid
                    })

        # 6. UPDATE ACTION
        if not mismatches_details:
            print("All matching types are synchronized. No updates needed.")
            messagebox.showinfo("Library Sync", f"All matching types are synchronized between the Project Library and '{global_lib_name}'. No updates needed.")
        else:
            print(f"\nFound {len(mismatches_details)} types with version mismatches. Showing selection dialog...")

            guids_to_update = show_update_dialog(mismatches_details)

            if not guids_to_update:
                print("Update cancelled by user or no items were selected.")
            else:
                print(f"User selected {len(guids_to_update)} types. Proceeding with update...")
                try:
                    global_lib.update_library(
                        update_mode=1,
                        delete_mode=1,
                        conflict_mode=3,
                        type_guids=guids_to_update
                    )

                    print("Project update successful.")
                    messagebox.showinfo("Update Complete", f"Successfully updated {len(guids_to_update)} library types in the Project Library.")
                except Exception as e:
                    print(f"An error occurred during the update: {e}")
                    messagebox.showerror("Update Error", f"An error occurred during the update:\n{e}")

    except Exception as e:
        print(f"A critical error occurred: {e}")
        if 'messagebox' in globals():
            messagebox.showerror("Script Error", f"A critical error occurred:\n{e}")
    finally:
        print("Script finished.")

run_library_rollout()