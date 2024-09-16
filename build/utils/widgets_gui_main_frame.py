import tkinter as tk
from tkinter import ttk
from random import randint
import folium.raster_layers
from utils.commands_gui_initialize import *
from utils.commands_gui_ask_start import *
from pyproj import Transformer
import folium
import geopandas as gpd
from folium import GeoJson
import rasterio as rio
import pandas as pd
import numpy as np
from pathlib import Path
import os
import webbrowser
import localtileserver
from localtileserver import get_folium_tile_layer
from localtileserver import TileClient

class SDWDropdownApp():
    def __init__(self, canvas, options):
        # Create a canvas
        self.canvas = canvas

        # List of options
        #self.options = [f"Option {i}" for i in range(1, 51)]  # Example with 50 options
        self.options = options
        
        # List of selected options
        self.selected_options = []
        
        # List of previous selected options
        self.previous_selected_options = []

        # Variable to store the selected option
        self.selected_option = tk.StringVar()

        # Create a Frame to contain the dropdown menu and scrollbar
        self.frame = ttk.Frame(self.canvas)
        # self.frame.pack(pady=20)

        # Create the dropdown menu with scrollbar
        self.create_dropdown()
        
        # Locate the Frame object in the canvas at the specified position
        self.canvas.create_window(75, 110, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=17, width=22, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
        self.dropdown_listbox.config(font=("Verdana", 9), fg="#4B4B91")
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        # Get the selected option
        selected_index = self.dropdown_listbox.curselection()
        # Clear the previous selected option
        self.selected_options.clear()
        # Update the list of selected options
        self.selected_options.append(selected_index[0])
        # Update the selected option
        self.selected_option.set(self.options[selected_index[0]])
        print(f"SDW Selected: {self.selected_option.get()}")
        self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in range(len(self.options)):
            if index in self.selected_options:
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            else:                      
                self.dropdown_listbox.itemconfig(index, {'bg': 'white'})
            # Change the background color of the previous selected options
            if self.options[index] in self.previous_selected_options and index not in self.selected_options:
                self.dropdown_listbox.itemconfig(index, {'bg': 'gainsboro'})
    
    def update_previous_selected_options(self):
        # Update the previous selected options
        self.previous_selected_options.append(self.selected_option.get())
                
class TransectsDropdownApp():
    def __init__(self, canvas, options):
        # Create a canvas
        self.canvas = canvas

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
        self.canvas.create_window(80, 632, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=7, width=8, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
        self.dropdown_listbox.config(font=("Verdana", 9), fg="#4B4B91")
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        # Get the selected option
        selected_indices = self.dropdown_listbox.curselection()
        # For some reason, this app is not working properly as it should.
        # It is not selecting the options correctly when the user clicks on other dropdown menus of the app.
        # To solve this issue, I declare the following conditional to identify when the selection is empty in order to not overwrite the previous selection.
        if len(selected_indices) == 0:
            return
        # Clear the previous selected option
        self.selected_options.clear()
        # Update the list of selected options
        for index in selected_indices:
            self.selected_options.append(index)
        # Update the selected option
        self.selected_option.set([self.options[index] for index in self.selected_options])
        print(f"Transects Selected: {self.selected_option.get()}")
        self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in range(len(self.options)):
            if index in self.selected_options:
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            else:
                self.dropdown_listbox.itemconfig(index, {'bg': 'white'})
    
    def select_all(self):
        # Select all the options
        self.selected_options = [i for i in range(len(self.options))]
        # Update the selected option
        self.selected_option.set(self.options)
        print(f"Transects Selected: {self.selected_option.get()}")
        self.update_selected_colors()
    
    def deselect_all(self):
        # Deselect all the options
        self.selected_options.clear()
        # Update the selected option
        self.selected_option.set([])
        print(f"Transects Selected: {self.selected_option.get()}")
        self.update_selected_colors()

class TypeIndicatorDropdownApp():
    def __init__(self, canvas, options):
        # Create a canvas
        self.canvas = canvas

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
        self.canvas.create_window(350, 650, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=5, width=30, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
        self.dropdown_listbox.config(font=("Verdana", 9), fg="#4B4B91")
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        # Get the selected option
        selected_index = self.dropdown_listbox.curselection()
        # Clear the previous selected option
        self.selected_options.clear()
        # Update the list of selected options
        self.selected_options.append(selected_index[0])
        # Update the selected option
        self.selected_option.set(self.options[selected_index[0]])
        print(f"Type of indicator Selected: {self.selected_option.get()}")
        self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in range(len(self.options)):
            if index in self.selected_options:
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            else:
                self.dropdown_listbox.itemconfig(index, {'bg': 'white'})

class ConfidenceLevelDropdownApp():
    def __init__(self, canvas, options):
        # Create a canvas
        self.canvas = canvas

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
        self.canvas.create_window(700, 650, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=3, width=10, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
        self.dropdown_listbox.config(font=("Verdana", 9), fg="#4B4B91")
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        # Get the selected option
        selected_index = self.dropdown_listbox.curselection()
        # Clear the previous selected option
        self.selected_options.clear()
        # Update the list of selected options
        self.selected_options.append(selected_index[0])
        # Update the selected option
        self.selected_option.set(self.options[selected_index[0]])
        print(f"Level of Confidence Selected: {self.selected_option.get()}")
        self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in range(len(self.options)):
            if index in self.selected_options:
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            else:
                self.dropdown_listbox.itemconfig(index, {'bg': 'white'})

class MapBrowserApp():
    def __init__(self, sdw_selection: str):
        # Read the SDW and transects fc
        self.sdw_selection = sdw_selection
        # Create the map object
        self.map = folium.Map()
        # Set the extent of the map to the transects fc
        self.set_extent()
        # Add the transects fc to the map
        self.add_transects_fc()
        # Add the SDW fc to the map
        self.add_sdw_fc()
        # Plot the raster
        self.plot_raster()
        # Add the layer control to the map
        folium.LayerControl().add_to(self.map)
        # Open the map on the browser
        self.open_map()
        
    def add_sdw_fc(self):
        """
        Add the SDW fc to the map.
        """
        # Get the selected SDW
        self.date_sdw = self.sdw_selection.split(" - ")[0]
        self.sensor_sdw = self.sdw_selection.split(" - ")[1]
        # Add the SDW fc to the map
        sdw_fc_row = sdw_fc[(sdw_fc["date"] == self.date_sdw) & (sdw_fc["sensor"] == self.sensor_sdw)]
        # Add the name of the SDW as a tooltip
        sdw_fc_row["date-sensor"] = self.date_sdw.split(" ")[0] + " - " + self.sensor_sdw # YYYY-MM-DD - Sensor
        tooltip = folium.GeoJsonTooltip(fields=["date-sensor"], aliases=["SDW Date-Sensor"])
        # Add the SDW to the map
        GeoJson(sdw_fc_row,
                name=f"SDW {self.date_sdw}",
                tooltip=tooltip,
                style_function=lambda x: {"color": "#4B4B91"}
                ).add_to(self.map)

    def add_transects_fc(self):
        """
        Add the transects fc to the map.
        """
        # Add the ID of the transects as a tooltip
        tooltip = folium.GeoJsonTooltip(fields=["transect_id"], aliases=["Transect ID"])
        # Add the transects to the map
        GeoJson(transects_fc,
                name="Transects",
                tooltip=tooltip,
                style_function=lambda x: {"color": "#DEBF33",
                                          "opacity": 0.5}
                ).add_to(self.map)
        # Add the transects id as a label on the map
        for _, row in transects_fc.iterrows():
            # Get the centroid of the transect 
            x, y = self.transformer.transform(row["geometry"].centroid.x,
                                                  row["geometry"].centroid.y)
            # Create a marker with the transect id
            folium.Marker(
                location=[y, x],  # Coordenadas del centroide
                icon=folium.DivIcon(html=f'''
                    <div style="
                        font-size: 10pt;
                        color: #DEBF33;
                        font-weight: bold;
                        text-shadow: -1px -1px 0 #000000, 1px -1px 0 #000000, -1px 1px 0 #000000, 1px 1px 0 #000000;
                    ">{row["transect_id"]}</div>'''),
                popup=f'<b>Transect ID:</b> {row["transect_id"]}',
                tooltip=f'Transect ID: {row["transect_id"]}'
            ).add_to(self.map)
    
    def set_extent(self):
        """
        Set the extent of the map to the transects fc.
        """
        # Get the transect fc bounds in geographic coordinates and set the map extent
        self.transformer = Transformer.from_crs(transects_fc.crs, "EPSG:4326", always_xy=True)
        bounds = transects_fc.total_bounds
        # Convert the bounds to lat/lon
        bounds = self.transformer.transform(bounds[0], bounds[1]) + \
            self.transformer.transform(bounds[2], bounds[3])
        self.map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
               
    def plot_raster(self):
        """
        Try another way to plot the raster on the map.
        """
        # Get the raster file name
        raster_file_name = os.path.join(rgb_folder_path, f"{self.date_sdw.split(' ')[0]}-{self.sensor_sdw}.tif")
        # Open the raster file
        with rio.open(raster_file_name) as src:
            # Read the bands
            red = src.read(1)
            green = src.read(2)
            blue = src.read(3)

            # Replace the nodata values with 0
            nodata_value = src.nodatavals[0]  # Assuming all bands have the same nodata value
            if nodata_value == 65535:
                red[red == nodata_value] = 0
                green[green == nodata_value] = 0
                blue[blue == nodata_value] = 0

            # Normalize the values to the range [0, 255] with clipping to avoid outliers
            def normalize(band):
                band_min, band_max = np.percentile(band, (2, 98))  # Clip the values between the 2nd and 98th percentile
                return np.clip((band - band_min) * 255 / (band_max - band_min), 0, 255)
            
            red = normalize(red)
            green = normalize(green)
            blue = normalize(blue)

            # Convert the bands to uint8
            rgb = np.stack((red, green, blue), axis=0).astype(np.uint8)

            # Copy the metadata of the source raster file
            profile = src.profile
            profile.update(dtype=rio.uint8, count=3, nodata=0)

            # Save the normalized RGB raster as a temporary file
            out_temp_raster = os.path.join(Path(input_info_file).parent.parent, 'temp_normalized_rgb.tif')
            with rio.open(out_temp_raster, 'w', **profile) as dst:
                dst.write(rgb)
            
            # Create a tile server from local raster file
            tile_client = TileClient(out_temp_raster)
            # Clear cache
            #tile_client.clear_cache()
            # Create folium tile layer from that server
            tile_layer = get_folium_tile_layer(tile_client, name=f"Layer_{randint(0, 10000)}") # Random name to avoid conflicts
            self.map.add_child(tile_layer)
            del tile_client, tile_layer
            
    def open_map(self):
        """
        Save and open the map on the browser.
        """
        # Add a title to the map
        title_html = f"""
        <h3 align="center" style="font-size:20px; color:#4B4B91"><b>{self.date_sdw} - {self.sensor_sdw}</b></h3>
        """
        self.map.get_root().html.add_child(folium.Element(title_html))
        # Set the path to save the map
        out_path = Path(input_info_file).parent.parent
        self.map_path = os.path.join(out_path, "map.html")
        # Save the map and open it on the browser
        self.map.save(self.map_path)
        webbrowser.open(self.map_path)