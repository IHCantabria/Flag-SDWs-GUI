"""
This file holds the backend code for the main GUI frame.
"""
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.matplotlib_config import *
import geopandas as gpd
import pandas as pd
from utils.commands_gui_initialize import *
from utils.commands_gui_ask_start import *
from utils.widgets_gui_main_frame import DropdownApp


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
    sdw_dropdown = DropdownApp(canvas, 120, 130, sdw_options)
    return sdw_dropdown

def plot_tide(window, sdw_selection: str):
    """
    Plot the tide data.

    Parameters:
    - None

    Returns:
    - None
    """
    print("Plotting tide data...")
    # Get the selected date SDW
    date_sdw = sdw_selection.split(" - ")[0]
    date_sdw = pd.to_datetime(date_sdw).floor("h")
    # Create the figure
    fig = Figure(figsize=(3, 1.5), dpi=100)
    tide_plot = fig.add_subplot(111)
    # Plot the tide data for the selected date
    tide_plot.plot(metocean_df.loc[date_sdw].name,
                   metocean_df.loc[date_sdw, "tide"],
                   marker="o", lw=0, color="red", zorder=20)
    # Plot a horizontal line at the selected SDW tide
    tide_plot.axhline(y=metocean_df.loc[date_sdw, "tide"],
                      color="red", ls="--", lw=0.5, zorder=15)
    # Plot a horizontal line at the median tide level
    tide_plot.axhline(y=metocean_df["tide"].median(), color="black", lw=0.5, zorder=10)
    # Plot the entire tide data
    tide_plot.plot(metocean_df["tide"])
    tide_plot.set_xlabel("Time")
    tide_plot.set_ylabel("Tide (m)")
    # Rotate x-axis ticks labels
    tide_plot.set_xticklabels(tide_plot.get_xticklabels(), rotation=45)
    # Tight layout
    fig.tight_layout()
    # Set the background transparent
    fig.patch.set_facecolor('#F7F0CE')
    # Create the Tkinter canvas
    figure_canvas = FigureCanvasTkAgg(fig, master=window)
    figure_canvas.draw()
    # Place the canvas
    figure_canvas.get_tk_widget().place(x=900, y=370)
        
    return

def command_plot_button(window: tk.Tk, sdw_dropdown: DropdownApp):
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
    plot_tide(window, sdw_selection)
    return