"""
This file is intended to be a snippet of the GUI initialization code in gui_initialize.py.
The code in this file is intended to be used as a reference for the commands used to initialize the GUI elements.
"""
import os
import pandas as pd
import geopandas as gpd
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
    output_folder = "output_folder_" + time.strftime("%Y%m%d%H%M%S")
    # Create the output folder path
    output_folder_path = os.path.join(basedir, output_folder)
    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Output folder created: {output_folder_path}")
    # Create a folder to store the input files
    input_files_folder = os.path.join(output_folder_path, "input_files")
    os.makedirs(input_files_folder, exist_ok=True)
    return output_folder_path, input_files_folder

def load_csv(file_path):
    """
    Load a CSV file and return the DataFrame.
    
    Parameters:
    - file_path (str): Path to the CSV file.
    
    Returns:
    - df (DataFrame): DataFrame with the CSV file data.
    """
    df = pd.read_csv(file_path)  # Load the CSV file
    df["date"] = pd.to_datetime(df["date"])  # Convert the "date" column to datetime
    df.set_index("date", inplace=True)  # Set the "date" column as the index
    print("CSV file loaded.")
    return df

def load_fc(gdb_path, fc_name):
    """
    Load a feature class and return the GeoDataFrame.
    
    Parameters:
    - gdb_path (str): Path to the File GDB.
    - fc_name (str): Name of the feature class.
    
    Returns:
    - gdf (GeoDataFrame): GeoDataFrame with the feature class data.
    """
    gdf = gpd.read_file(gdb_path, layer=fc_name)  # Load the feature class
    if fc_name == "SDW Feature Class Name":
        gdf["date"] = pd.to_datetime(gdf["date"])  # Convert the "date" column to datetime
    print(f"{fc_name} loaded.")
    return gdf

def create_out_csv(output_folder_path: str, sdw_fc: gpd.GeoDataFrame, transects_fc: gpd.GeoDataFrame):
    """
    
    """
    # Create a new column in the SDW GeoDataFrame with the date and sensor information
    #sdw_fc["date-sensor"] = sdw_fc["date"] + " - " + sdw_fc["sensor"]
    # Compute the intersection between the SDW and transects feature classes
    # to know which transects are intersect each SDW
    intersected_fc = gpd.overlay(sdw_fc, transects_fc, how="intersection", keep_geom_type=False)
    # Create a CSV file with the date-sensor information
    out_csv_path = os.path.join(output_folder_path, "flag_sdw_output.csv")
    intersected_fc[["date", "transect_id", "sensor"]].to_csv(out_csv_path, index=False)
    

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
        global output_folder_path, input_files_folder
        output_folder_path, input_files_folder = create_output_folder()
        # Create a TXT file with the input files, folders and entries information
        in_files_names = {
            2: "Metocean CSV File",
            3: "File GDB Path",
            4: "RGB Folder Path"
            }
        entry_names = {
            1: "SDW Feature Class Name",
            2: "Transects Feature Class Name",
            }
        # Create a dictionary to store the input files, folders and entries information
        global in_files_dict, entries_fc_dict
        in_files_dict = {in_files_names[key]: in_files[key] for key in in_files}
        entries_fc_dict = {entry_names[key]: entries_fc[key] for key in entries_fc}
        
        # Load the CSV file and the feature class
        global metocean_df, sdw_fc, transects_fc
        metocean_df = load_csv(in_files_dict["Metocean CSV File"])
        sdw_fc = load_fc(in_files_dict["File GDB Path"], entries_fc_dict["SDW Feature Class Name"])
        transects_fc = load_fc(in_files_dict["File GDB Path"], entries_fc_dict["Transects Feature Class Name"])
        
        with open(os.path.join(input_files_folder, "input_info.txt"), "w") as f:
            f.write("Folders Information\n\n")
            for key in in_files:
                f.write(f"{in_files_names[key]}: {in_files[key]}\n")
            f.write("\nFC Names\n\n")
            for key in entries_fc:
                f.write(f"{entry_names[key]}: {entries_fc[key]}\n")
        
        # Create the output CSV file
        create_out_csv(output_folder_path, sdw_fc, transects_fc)
        # Close the window
        window.destroy()
    return
