"""
This file is intended to be a snippet of the GUI initialization code in gui_initialize.py.
The code in this file is intended to be used as a reference for the commands used to initialize the GUI elements.
"""
import os
from tkinter import Tk, messagebox, filedialog
import time

def select_folder(folder_path, button_id):
    """
    Open a dialog to select a folder and return the selected folder path.
    
    Parameters:
    - folder_path (dict): Dictionary to store the selected folder paths.
    - button_id (str): ID of the button used to select the folder.
    
    Returns:
    - None
    """
    folder_path[button_id] = filedialog.askdirectory()  # Open the dialog to select a folder
    if folder_path[button_id]:
        print("Selected folder:", folder_path[button_id])  # Print the selected folder path if any
        return
    else:
        print("No folder selected.")  # Print a message if no folder is selected
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

def create_output_folder(basedir):
    """
    Function to create an output folder with the current timestamp.
    """
    output_folder = "output_folder " + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(os.path.join(basedir, output_folder), exist_ok=True)
    

def start_button(entries_widgets: list, folder_path: dict, window: Tk):
    """
    Function to be executed when the Start button is clicked.
    
    Parameters:
    - entries_widgets (list): List of Entry widgets.
    - folder_path (dict): Dictionary containing the selected folder paths.
    
    Returns:
    - None
    """
    # Retrieve the entries from the Entry widgets
    entries_fc = {id + 1: get_entry_text(entry, id + 1) for id, entry in enumerate(entries_widgets)}
    # Check that the entries are not empty
    if any([e is None for e in entries_fc.values()]) or len(folder_path) != 3:
        messagebox.showerror("Error", "Please fill in all the fields.")  # Show an error message if any of the entries is empty
        return
    else:
        # Create the output folder
        create_output_folder(folder_path[3])
        # If all entries are filled, close the window
        window.destroy()
    return
