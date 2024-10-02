"""
This file holds the backend code for the main GUI frame.
"""
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.matplotlib_config import *
import matplotlib.patheffects as path_effects
import geopandas as gpd
import pandas as pd
from utils.commands_gui_initialize import *
from utils.commands_gui_ask_start import *
from utils.widgets_gui_main_frame import SDWDropdownApp, TransectsDropdownApp, TypeIndicatorDropdownApp, ConfidenceLevelDropdownApp, MapBrowserApp
import stat
import os
import warnings
warnings.filterwarnings("ignore")

OUTPUT_PATH = Path(__file__).parent.parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Repos Github\Flag-SDWs-GUI\build\assets\frame0")
ASSETS_PATH = Path.joinpath(OUTPUT_PATH, "assets/frame2")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_previous_sdws() -> list:
    """
    Get the previous saved SDWs from the output CSV file.
    """
    # Read the output CSV file
    out_csv_df = pd.read_csv(out_csv_path)
    # Create a mask to filter the rows with type indicator and level of confidence
    mask = (out_csv_df["type_indicator"] != "-") | (out_csv_df["level_confidence"] != "-")
    # Apply the mask to the output CSV DataFrame
    processed_rows = out_csv_df[mask]
    # Get the unique dates and sensors that have been already saved
    unique_date_sensor = (processed_rows["date"] + " - " + processed_rows["sensor"]).unique().tolist()
    
    return unique_date_sensor

def set_sdw_dropdown(canvas: Canvas):
    """
    Set the dropdown menu for the SDW selection.

    Parameters:
    - canvas (Canvas): Canvas object to place the dropdown menu.

    Returns:
    - None
    """
    # Set the SDW dropdown menu
    sdw_options = [f"{sdw_fc.iloc[i]['date']} - {sdw_fc.iloc[i]['sensor']}" for i in sdw_fc.index]
    sdw_dropdown = SDWDropdownApp(canvas, sdw_options)
    # Get the previous saved SDWs if any
    previous_sdws = get_previous_sdws()
    if previous_sdws:
        # Set the previous saved SDWs as selected
        sdw_dropdown.previous_selected_options = previous_sdws
        # Update the background color of the previous selected SDWs
        sdw_dropdown.update_selected_colors()
    
    return sdw_dropdown

def set_transects_dropdown(canvas: Canvas, sdw_selection: str):
    """
    Set the dropdown menu for the transects selection.

    Parameters:
    - canvas (Canvas): Canvas object to place the dropdown menu.

    Returns:
    - None
    """
    # Get the selected date and sensor
    date_sdw = sdw_selection.split(" - ")[0]
    sensor_sdw = sdw_selection.split(" - ")[1]
    # Get the transects for the selected date and sensor
    transects_options = out_csv_df.loc[(out_csv_df["date"] == date_sdw) & (out_csv_df["sensor"] == sensor_sdw),
                                       "transect_id"].unique().tolist()
    transects_dropdown = TransectsDropdownApp(canvas, transects_options)
    
    return transects_dropdown

def set_type_indicator_dropdown(canvas: Canvas):
    """
    Set the dropdown menu for the type indicator selection.

    Parameters:
    - canvas (Canvas): Canvas object to place the dropdown menu.

    Returns:
    - None
    """
    # Set the type indicator dropdown menu
    type_indicator_options = [
        "1- Waterline", "2- Wave run-up", "3- Max. High Tide Level",
        "4- Intertidal Water", "5- Intertidal Morph. Features", "6- Backshore elements",
        "7- N/A"
        ]
    type_indicator_dropdown = TypeIndicatorDropdownApp(canvas, type_indicator_options)
    # Preselect the first option
    #type_indicator_dropdown.dropdown_listbox.select_set(0)
    #type_indicator_dropdown.selected_option.set(type_indicator_options[0])
    
    return type_indicator_dropdown

def set_confidence_level_dropdown(canvas: Canvas):
    """
    Set the dropdown menu for the confidence level selection.

    Parameters:
    - canvas (Canvas): Canvas object to place the dropdown menu.

    Returns:
    - None
    """
    # Set the confidence level dropdown menu
    confidence_level_options = ["High", "Medium", "Low"]
    confidence_level_dropdown = ConfidenceLevelDropdownApp(canvas, confidence_level_options)
    # Preselect the first option
    #confidence_level_dropdown.dropdown_listbox.select_set(0)
    #confidence_level_dropdown.selected_option.set(confidence_level_options[0])
    
    return confidence_level_dropdown

def plot_time_series(window: tk.Tk, sdw_selection: str, var: str):
    """
    Plot the Hs/Tide time series data.

    Parameters:
    - window (Tk): Tkinter window object.
    - sdw_selection (str): Selected SDW.
    - var (str): Variable to plot (Hs or Tide).

    Returns:
    - None
    """
    print(f"Plotting {var} data...")
    # Set the parameters for the selected variable to plot
    var_params = {
        "hs": ["Hs (m)", (380, 290)],
        "tide": ["Tide (m)", (710, 290)]
        }
    # Get the selected date SDW
    date_sdw = sdw_selection.split(" - ")[0]
    date_sdw = pd.to_datetime(date_sdw).floor("h")
    # Create the figure
    fig = Figure(figsize=(3, 1.75), dpi=100)
    var_plot = fig.add_subplot(111)
    # Check that the selected date is in the metocean data. If not, display a empty plot
    if date_sdw not in metocean_df.index:
        var_plot.set_title(f"No data for {date_sdw}")
        # Create the Tkinter canvas
        figure_canvas = FigureCanvasTkAgg(fig, master=window)
        figure_canvas.draw()
        # Place the canvas in the window
        figure_canvas.get_tk_widget().place(x=var_params[var][1][0],
                                            y=var_params[var][1][1])

        return
    # Plot the data for the selected date
    var_plot.plot(metocean_df.loc[date_sdw].name,
                  metocean_df.loc[date_sdw, var],
                  marker="o", lw=0, color="red", zorder=20,
                  label=f"SDW date: {metocean_df.loc[date_sdw, var]:.2f}")
    # Plot a horizontal line at the selected SDW tide
    var_plot.axhline(y=metocean_df.loc[date_sdw, var],
                     color="red", ls="--", lw=0.5, zorder=15)
    # Plot a horizontal line at the median level
    var_median = metocean_df[var].median()
    var_plot.axhline(y=var_median, color="black", lw=1, zorder=10)
    # Draw the median level text
    median_text = var_plot.text(metocean_df.index[0], var_median,
                                f"P50% = {var_median:.2f}",
                                ha="left", va="center", color="black", fontsize=7.5,
                                zorder=10)
    median_text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                                  path_effects.Normal()])
    # Plot the entire tide data
    var_plot.plot(metocean_df[var])
    var_plot.set_ylabel(var_params[var][0])
    # Rotate x-axis ticks labels
    var_plot.set_xticklabels(var_plot.get_xticklabels(), rotation=45)
    # Set the legend
    var_plot.legend(fontsize=7.5, labelcolor='linecolor')
    # Tight layout
    fig.tight_layout()
    # Set the background of the figure and axis "transparent"
    fig.patch.set_facecolor('#F7F0CE')
    var_plot.set_facecolor('#F7F0CE')
    # Create the Tkinter canvas
    figure_canvas = FigureCanvasTkAgg(fig, master=window)
    figure_canvas.draw()
    # Place the canvas in the window
    figure_canvas.get_tk_widget().place(x=var_params[var][1][0],
                                        y=var_params[var][1][1])
        
    return

def show_flood_ebb(canvas: Canvas, sdw_selection: str):
    """
    Show an image of flood or ebb tide whether the selected SDW is in flood or ebb tide.
    
    Parameters:
    - window (Tk): Tkinter window object.
    - sdw_selection (str): Selected SDW.
    
    Returns:
    - None
    """
    # Get the selected date SDW
    date_sdw = sdw_selection.split(" - ")[0]
    date_sdw = pd.to_datetime(date_sdw).floor("h")
    # Check the previous tide level to determine if the tide is in flood or ebb
    if metocean_df.loc[date_sdw, "tide"] > metocean_df.loc[date_sdw - pd.Timedelta(hours=1), "tide"]:
        print("Flood tide")
        # Plot the flood tide image
        fig = Figure(figsize=(1.5, 1.5), dpi=100)
        ax = fig.add_subplot(111)
        image = ax.imshow(plt.imread(relative_to_assets("image_9.png")))
    else:
        print("Ebb tide")
        # Plot the ebb tide image
        fig = Figure(figsize=(1.5, 1.5), dpi=100)
        ax = fig.add_subplot(111)
        image = ax.imshow(plt.imread(relative_to_assets("image_10.png")))
    ax.axis("off")
    fig.tight_layout()
    # Make the background transparent
    fig.patch.set_facecolor('#F7F0CE')
    canvas = FigureCanvasTkAgg(fig, master=canvas)
    canvas.draw()
    canvas.get_tk_widget().place(x=1050, y=300)
    
    return

def show_sdw_data(window: tk.Tk, sdw_selection: str):
    """
    Display the selected SDW data in a table.
    """
    # Get the selected SDW
    date_sdw = sdw_selection.split(" - ")[0]
    sensor_sdw = sdw_selection.split(" - ")[1]
    # Check that the SDW feature class has the extra columns
    extra_cols = ["algorithm", "index", "threshold"]
    # Check that the extra_cols exist in the sdw_fc GeoDataFrame, otherwise create them with NaN values
    for col in extra_cols:
        if col not in sdw_fc.columns:
            sdw_fc[col] = "NaN"
    # Get the selected row of the sdw_fc GeoDataFrame
    sdw_fc_row = sdw_fc[(sdw_fc["date"] == date_sdw) & (sdw_fc["sensor"] == sensor_sdw)]
    # Turn uppercase all columns
    sdw_fc_row.columns = sdw_fc_row.columns.str.upper()
    # Create a matplotlib table with the selected SDW data
    table_cols = ["DATE", "SENSOR", "ALGORITHM", "INDEX", "THRESHOLD"]
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.axis("off")
    table_data = sdw_fc_row[table_cols].values
    table = ax.table(cellText=table_data, colLabels=table_cols,
                     loc="center", cellLoc="center", colLoc="center",
                     cellColours=[["#F7F0CE"]*5]*len(table_data))
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.5, 1.5)
    fig.tight_layout()
    fig.patch.set_facecolor('#F7F0CE')
    # Create the Tkinter canvas
    figure_canvas = FigureCanvasTkAgg(fig, master=window)
    figure_canvas.draw()
    # Place the canvas in the window
    figure_canvas.get_tk_widget().place(x=410, y=67)
    
    return    

def command_select_all_button():
    """
    Command to be executed when the "Select All" button is clicked.

    Parameters:
    - None

    Returns:
    - None
    """
    # Select all the transects
    transects_dropdown.select_all()
    
    return

def command_deselect_all_button():
    """
    Command to be executed when the "Deselect All" button is clicked.

    Parameters:
    - None

    Returns:
    - None
    """
    # Select all the transects
    transects_dropdown.deselect_all()
    
    return

def command_plot_button(window: tk.Tk, canvas: Canvas, sdw_dropdown: SDWDropdownApp):
    """
    Command to be executed when the "Plot" button is clicked.

    Parameters:
    - window (Tk): Tkinter window object.
    - sdw_dropdown (SDWDropdownApp): SDWDropdownApp object.

    Returns:
    - None
    """
    # Get the selected SDW
    sdw_selection = sdw_dropdown.selected_option.get()
    try:
        # Plot the tide data
        plot_time_series(window, sdw_selection, "tide")
        # Show the flood or ebb tide image
        show_flood_ebb(canvas, sdw_selection)
    except KeyError:
        print("No tide data for the selected date.")
    try:
        # Plot the Hs data
        plot_time_series(window, sdw_selection, "hs")
    except KeyError:
        print("No wave data for the selected date.")
    # Show the SDW data
    show_sdw_data(window, sdw_selection)
    # Create the map browser
    map_browser = MapBrowserApp(sdw_selection)
    # Create the Transects dropdown menu
    global transects_dropdown
    transects_dropdown = set_transects_dropdown(canvas, sdw_selection)
    # Create the Type Indicator dropdown menu
    global type_indicator_dropdown
    type_indicator_dropdown = set_type_indicator_dropdown(canvas)
    # Create the Confidence Level dropdown menu
    global confidence_level_dropdown
    confidence_level_dropdown = set_confidence_level_dropdown(canvas)
        
    return

def command_save_sdw_button(sdw_dropdown, entry_1):
    """
    Command to be executed when the "Save SDW" button is clicked.

    Parameters:
    - sdw_dropdown (SDWDropdownApp): SDWDropdownApp object.
    - entry_1 (Entry): Entry object.

    Returns:
    - None
    """
    # 1 == Grab the data ==
    # Create a list to store all the saved SDWs if not exists
    if "saved_sdws" not in locals():
        saved_sdws = []
    sdw_selection = sdw_dropdown.selected_option.get()
    saved_sdws.append(sdw_selection)
    # Get the selected date and sensor
    date_sdw = sdw_selection.split(" - ")[0]
    sensor_sdw = sdw_selection.split(" - ")[1]
    # Get the selected transect IDs
    transects_selection = eval(transects_dropdown.selected_option.get())
    # Get the type of indicator
    type_indicator = type_indicator_dropdown.selected_option.get()
    # Get the level of confidence
    confidence_level = confidence_level_dropdown.selected_option.get()
    # Create a boolean mask for the date, sensor, and transect IDs
    mask = (out_csv_df["date"] == date_sdw) & \
        (out_csv_df["sensor"] == sensor_sdw) & \
            (out_csv_df["transect_id"].isin(transects_selection))
            
    # 2 == Update the background color of the previous selected SDW and transects==
    # SDWs
    sdw_dropdown.update_previous_selected_options()
    sdw_dropdown.update_selected_colors()
    # Transects
    transects_dropdown.saved_transects += transects_selection
    transects_dropdown.update_selected_colors()
    
    # 3 == Update the out_csv_df with the selected type indicator and level of confidence ==
    # Update the out_csv_df with the selected type indicator
    out_csv_df.loc[mask, "type_indicator"] = type_indicator
    # Update the out_csv_df with the selected level of confidence
    out_csv_df.loc[mask, "level_confidence"] = confidence_level
    # Give all permissions to the output CSV file
    out_csv_path_o = Path(out_csv_path)
    out_csv_path_o.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    # Save the out_csv_df to the output CSV file
    out_csv_df.to_csv(out_csv_path_o, index=False)
    
    # 4 == Update the entry_1 widget with the selected SDW ==
    # Calculate the number of SDW left to save
    unique_date_sensor = (out_csv_df["date"] + " - " + out_csv_df["sensor"]).unique()
    sdw_left = len(unique_date_sensor) - len(saved_sdws)
    # Update the entry_1 widget with the number of SDW left to save
    #entry_1.delete(0, tk.END)
    #entry_1.insert(0, f"{len(saved_sdws)}/{len(unique_date_sensor)} SDW done")
    
    print("SDW saved.")
    
    return