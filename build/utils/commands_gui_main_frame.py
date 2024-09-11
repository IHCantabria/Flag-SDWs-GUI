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
import geopandas as gpd
import pandas as pd
from utils.commands_gui_initialize import *
from utils.commands_gui_ask_start import *
from utils.widgets_gui_main_frame import DropdownApp, MapBrowserApp
import warnings
warnings.filterwarnings("ignore")

OUTPUT_PATH = Path(__file__).parent.parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Repos Github\Flag-SDWs-GUI\build\assets\frame0")
ASSETS_PATH = Path.joinpath(OUTPUT_PATH, "assets/frame2")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
    sdw_dropdown = DropdownApp("SDW", canvas, 80, 110, sdw_options)
    
    return sdw_dropdown

def command_select_all_button():
    """
    Command to be executed when the "Select All" button is clicked.

    Parameters:
    - transect_id_dropdown (DropdownApp): DropdownApp object.

    Returns:
    - None
    """
    # Select all the transect IDs
    transect_id_dropdown.select_all()

    return

def command_deselect_all_button():
    """
    Command to be executed when the "Deselect All" button is clicked.

    Parameters:
    - transect_id_dropdown (DropdownApp): DropdownApp object.

    Returns:
    - None
    """
    # Deselect all the transect IDs
    transect_id_dropdown.deselect_all()

    return

def set_transect_id_dropdown(canvas: Canvas, sdw_selection: str):
    """
    Set the dropdown menu for the transect ID selection.

    Parameters:
    - canvas (Canvas): Canvas object to place the dropdown menu.
    - sdw_selection (str): Selected SDW.

    Returns:
    - None
    """
    # Find the transects for the selected SDW in the flag_sdw_output.CSV file
    date_sdw = sdw_selection.split(" - ")[0]
    sensor_sdw = sdw_selection.split(" - ")[1]
    transects_sdw = out_csv_df.loc[(out_csv_df["date"] == date_sdw) & (out_csv_df["sensor"] == sensor_sdw),
                                   "transect_id"].values
    # Set the transect ID dropdown menu
    transect_id_options = transects_sdw.tolist()
    transect_id_dropdown = DropdownApp("Transect ID", canvas, 85, 632, transect_id_options)
    
    return transect_id_dropdown

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
        "1- Waterline", "2- Wave run-up", "3- Max. High Tide Level", "4- Previous Higher Water Level",
        "5- Intertidal Water", "6- Backshore elements (e.g. vegetation shadow)",
        "7- N/A"
        ]
    type_indicator_dropdown = DropdownApp("Type Indicator", canvas, 80, 590, type_indicator_options)
    
    return type_indicator_dropdown

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
        "hs": ["Hs (m)", (380, 310)],
        "tide": ["Tide (m)", (710, 310)]
        }
    # Get the selected date SDW
    date_sdw = sdw_selection.split(" - ")[0]
    date_sdw = pd.to_datetime(date_sdw).floor("h")
    # Create the figure
    fig = Figure(figsize=(3, 1.5), dpi=100)
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
    # Plot the tide data for the selected date
    var_plot.plot(metocean_df.loc[date_sdw].name,
                  metocean_df.loc[date_sdw, var],
                  marker="o", lw=0, color="red", zorder=20)
    # Plot a horizontal line at the selected SDW tide
    var_plot.axhline(y=metocean_df.loc[date_sdw, var],
                     color="red", ls="--", lw=0.5, zorder=15)
    # Plot a horizontal line at the median tide level
    var_plot.axhline(y=metocean_df[var].median(), color="black", lw=0.5, zorder=10)
    # Plot the entire tide data
    var_plot.plot(metocean_df[var])
    var_plot.set_ylabel(var_params[var][0])
    # Rotate x-axis ticks labels
    var_plot.set_xticklabels(var_plot.get_xticklabels(), rotation=45)
    # Tight layout
    fig.tight_layout()
    # Set the background transparent
    fig.patch.set_facecolor('#F7F0CE')
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

def command_plot_button(window: tk.Tk, canvas: Canvas, sdw_dropdown: DropdownApp):
    """
    Command to be executed when the "Plot" button is clicked.

    Parameters:
    - window (Tk): Tkinter window object.
    - sdw_dropdown (DropdownApp): DropdownApp object.

    Returns:
    - None
    """
    # Get the selected SDW
    sdw_selection = sdw_dropdown.selected_option.get()
    # Plot the tide data
    plot_time_series(window, sdw_selection, "tide")
    # Plot the Hs data
    plot_time_series(window, sdw_selection, "hs")
    # Show the flood or ebb tide image
    show_flood_ebb(canvas, sdw_selection)
    # Show the SDW data
    show_sdw_data(window, sdw_selection)
    # Create the map browser
    map_browser = MapBrowserApp(sdw_selection)
    # Create the Transect ID dropdown menu
    global transect_id_dropdown
    transect_id_dropdown = set_transect_id_dropdown(canvas, sdw_selection)
    
    return