"""
This file is intended to be a snippet of the GUI initialization code in gui_initialize.py.
The code in this file is intended to be used as a reference for the commands used to initialize the GUI elements.
"""
import os
from pathlib import Path
from tkinter import Tk, messagebox, filedialog
import time

def select_folder(in_files, button_id):
    """
    Open a dialog to select a folder and return the selected folder path.
    
    Parameters:
    - in_files (dict): Dictionary to store the selected folder paths.
    - button_id (str): ID of the button used to select the folder.
    
    Returns:
    - None
    """
    in_files[button_id] = filedialog.askdirectory() # Open the dialog to select a folder
    if in_files[button_id]:
        print("Selected folder:", in_files[button_id]) # Print the selected folder path if any
        return
    else:
        print("No folder selected.") # Print a message if no folder is selected
        return

def select_csv_file(file_path, button_id):
    """
    Open a dialog to select a CSV file and return the selected file path.
    
    Parameters:
    - file_path (dict): Dictionary to store the selected file paths.
    - button_id (str): ID of the button used to select the file.
    
    Returns:
    - None
    """
    file_path[button_id] = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Open the dialog to select a CSV file
    if file_path[button_id]:
        print("Selected file:", file_path[button_id]) # Print the selected file path if any
        return
    else:
        print("No file selected.") # Print a message if no file is selected
        return

def get_entry_text(entry, entry_id):
    """
    Get the text from an Entry widget and store it in a dictionary.
    
    Parameters:
    - entry (Entry): Entry widget to get the text from.
    - entry_id (str): ID of the Entry widget.
    
    Returns:
    - None
    """
    entry_text = entry.get()  # Get the text from the Entry widget
    if entry_text:
        print(f"Entry {entry_id} text:", entry_text)  # Print the text if any
        return entry_text
    else:
        print(f"No text in Entry {entry_id}.")  # Print a message if no text is entered
        return

def create_output_folder():
    """
    Function to create an output folder with the current timestamp.
    """
    # Get the directory where the main script is located
    basedir = Path(__file__).parent.parent
    # Create the output folder with the current timestamp
    output_folder = "output_folder_" + time.strftime("%Y%m%d-%H%M%S")
    # Create the output folder path
    output_folder_path = os.path.join(basedir, output_folder)
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Output folder created: {output_folder_path}")
    return output_folder_path

def start_button(entries_widgets: list, in_files: dict, window: Tk):
    """
    Function to be executed when the Start button is clicked.
    
    Parameters:
    - entries_widgets (list): List of Entry widgets.
    - in_files (dict): Dictionary containing the selected folder paths.
    
    Returns:
    - None
    """
    # Retrieve the entries from the Entry widgets
    entries_fc = {id + 1: get_entry_text(entry, id + 1) for id, entry in enumerate(entries_widgets)}
    # Check that the entries are not empty
    if any([e is None for e in entries_fc.values()]) or len(in_files) != 3:
        messagebox.showerror("Error", "Please fill in all the fields.")  # Show an error message if any of the entries is empty
        return
    else:
        # Create the output folder
        create_output_folder()
        # If all entries are filled, close the window
        window.destroy()
    return
