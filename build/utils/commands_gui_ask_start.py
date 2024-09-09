"""
This file is intended to be a snippet of the GUI asking start code in gui_ask_start.py.
The code in this file is intended to be used as a reference for the commands used of the two main elements (yes/no buttons).
"""

from tkinter import Tk, messagebox, filedialog
from utils.commands_gui_initialize import load_csv, load_fc

def yes_button_clicked(window: Tk):
    """
    Command to be executed when the "Yes" button is clicked.
    
    Parameters:
    - None
    
    Returns:
    - None
    """
    print("Yes button clicked.")
    window.destroy()
    return

def no_button_clicked(new_project: bool, window: Tk):
    """
    Command to be executed when the "No" button is clicked.
    
    Parameters:
    - None
    
    Returns:
    - None
    """
    print("No button clicked.")
    # Update the global variable to False
    new_project = False
    # Ask to select the input_info.txt created in the initialization GUI
    global input_info_file
    input_info_file = filedialog.askopenfilename(filetypes=[("input_info TXT file", "*.txt")])
    read_input_info_file(input_info_file)
    window.destroy()
    return new_project

def read_input_info_file(input_info_file: str):
    """
    Read the input_info.txt file created in the initialization GUI.
    
    Parameters:
    - input_info_file (str): Path to the input_info.txt file.
    
    Returns:
    - None
    """
    # Create dictionaries to store the input files and entries as it's done in the initialization GUI
    in_files_dict = {}
    entries_fc_dict = {}
    
    with open(input_info_file, "r") as file:
        for line in file:
            if "RGB Folder Path" in line:
                in_files_dict["RGB Folder Path"] = line.split(": ")[1].strip()
            elif "File GDB Path" in line:
                in_files_dict["File GDB Path"] = line.split(": ")[1].strip()
            elif "Metocean CSV File" in line:
                in_files_dict["Metocean CSV File"] = line.split(": ")[1].strip()
            elif "SDW Feature Class Name" in line:
                entries_fc_dict["SDW Feature Class Name"] = line.split(": ")[1].strip()
            elif "Transects Feature Class Name" in line:
                entries_fc_dict["Transects Feature Class Name"] = line.split(": ")[1].strip()
    
    # Load the CSV file and the feature class
    global metocean_df, sdw_fc, transects_fc
    metocean_df = load_csv(in_files_dict["Metocean CSV File"])
    sdw_fc = load_fc(in_files_dict["File GDB Path"], entries_fc_dict["SDW Feature Class Name"])
    transects_fc = load_fc(in_files_dict["File GDB Path"], entries_fc_dict["Transects Feature Class Name"])
    print("Input info file read.")
    return