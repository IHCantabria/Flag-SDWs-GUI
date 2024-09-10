import tkinter as tk
from tkinter import ttk
from utils.commands_gui_initialize import *
from utils.commands_gui_ask_start import *
import folium
from folium import GeoJson
import rasterio
import pandas as pd
import numpy as np
from pathlib import Path

class DropdownApp():
    def __init__(self, canvas, x, y, options):

        # Create a canvas
        self.canvas = canvas
        # Specify the position of the dropdown menu
        self.x = x
        self.y = y

        # List of options
        #self.options = [f"Option {i}" for i in range(1, 51)]  # Example with 50 options
        self.options = options
        
        # List of selected options
        self.selected_options = []

        # Variable to store the selected option
        self.selected_option = tk.StringVar()

        # Create a Frame to contain the dropdown menu and scrollbar
        self.frame = ttk.Frame(self.canvas)
        # self.frame.pack(pady=20)

        # Create the dropdown menu with scrollbar
        self.create_dropdown()
        
        # Locate the Frame object in the canvas at the specified position
        self.canvas.create_window(self.x, self.y, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=17, listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, width=25)
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        # Get the selected option
        selected_index = self.dropdown_listbox.curselection()
        
        if selected_index:
            index = selected_index[0]
            
            # Add the selected index to the list of selected options if it is not already there
            if index not in self.selected_options:
                self.selected_options.append(index)
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'}) # Change the background color of the selected option
            
            # Update the selected option    
            self.selected_option.set(self.options[selected_index[0]])
            print(f"Selected: {self.selected_option.get()}")
            # Update the selected colors
            self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in self.selected_options:
            self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            
class MapBrowser():
    def __init__(self, sdw_selection: str):
        self.sdw_selection = sdw_selection
        # Create the map object
        self.map = folium.Map(location=[-34.61, -58.38], zoom_start=12)
        # Add the SDW fc to the map
        GeoJson(sdw_fc).add_to(self.map)
        # Ad the transects fc to the map
        GeoJson(transects_fc).add_to(self.map)
        # Plot the raster
        self.plot_raster(file_path)
        
    def _check_map(self):
        """
        Check if there is a map already loaded on the browser and close it.
        """
        
        
    def plot_raster(self, file_path: str):
        """
        Read the raster file and return the data.
        """
        # Get the date and sensor from the selected SDW
        date_sdw = self.sdw_selection.split(" - ")[0]
        date_sdw = pd.to_datetime(date_sdw).strftime("%Y-%m-%d")
        sensor_sdw = self.sdw_selection.split(" - ")[1]
        # Get the raster file name
        raster_file_name = Path.joinpath(rgb_folder_path, f"{date_sdw}-{sensor_sdw}.tif")
        # Read the raster file
        with rasterio.open(raster_file_name) as src:
            # Read the 3 bands RGB
            r, g, b = src.read()
            # Stack the bands
            rgb = np.dstack((r, g, b))
            # Normalize the bands
            rgb = rgb / rgb.max()
            # Get the bounds
            bounds = src.bounds
            # Add the raster to the map
            folium.raster_layers.ImageOverlay(
                image=rgb,
                bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                opacity=0.5
            ).add_to(self.map)
            