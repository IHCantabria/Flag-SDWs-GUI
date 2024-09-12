import tkinter as tk
from tkinter import ttk
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

class SDWDropdownApp():
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
        self.canvas.create_window(80, 110, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=17, width=25, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
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
        self.canvas.create_window(85, 632, window=self.frame, anchor="nw")

    def create_dropdown(self):
        # Frame that contains the dropdown menu and scrollbar
        dropdown_frame = ttk.Frame(self.frame)
        dropdown_frame.pack()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(dropdown_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with the options and associate it with the scrollbar
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=7, width=10, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        self.dropdown_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.dropdown_listbox.yview)

        # Bind the selection of the dropdown menu to the selected variable
        self.dropdown_listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):       
        # Multiple selection
        # Get the selected options
        self.selected_indices = self.dropdown_listbox.curselection()
        # Clear the previous selected options
        self.selected_options.clear()
        # Update the list of selected options
        self.selected_options = [self.options[index] for index in self.selected_indices]
        # Update the selected option
        self.selected_option.set(self.selected_options)
        print(f"Transects Selected: {self.selected_option.get()}")
        # Change the background color of the selected options
        self.update_selected_colors()
            
    def update_selected_colors(self):
        # Change the background color of the selected options
        for index in range(len(self.options)):
            if index in self.selected_indices:
                self.dropdown_listbox.itemconfig(index, {'bg': 'lightgreen'})
            else:
                self.dropdown_listbox.itemconfig(index, {'bg': 'white'})
        
    def select_all(self):
        # Select all the options
        self.dropdown_listbox.select_set(0, tk.END)
        # Update the selected options
        self.selected_options = self.options
        # Update the selected option
        self.selected_option.set(self.options)
        # Change the background color of the selected options
        self.update_selected_colors()
        print(f"Transects Selected: {self.selected_option.get()}")
    
    def deselect_all(self):
        # Deselect all the options
        self.dropdown_listbox.selection_clear(0, tk.END)
        # Clear the selected options
        self.selected_options.clear()
        # Update the selected option
        self.selected_option.set("")
        # Change the background color of the selected options   
        self.update_selected_colors()
        print(f"Transects Selected: {self.selected_option.get()}")
    
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
        self.dropdown_listbox = tk.Listbox(dropdown_frame, height=5, width=42, 
                                           listvariable=tk.StringVar(value=self.options),
                                           selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
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
        self.sdw_selection = sdw_selection
        # Create the map object
        self.map = folium.Map(location=[-34.61, -58.38], zoom_start=12)
        # Add the SDW fc to the map
        self.add_sdw_fc()
        # Add the transects fc to the map
        self.add_transects_fc()
        # Plot the raster
        self.plot_raster()
        # Open the map on the browser
        self.open_map()
        
    def _check_map(self):
        """
        Check if there is a map already loaded on the browser and close it.
        """
        
    def add_sdw_fc(self):
        """
        Add the SDW fc to the map.
        """
        # Get the selected SDW
        date_sdw = self.sdw_selection.split(" - ")[0]
        sensor_sdw = self.sdw_selection.split(" - ")[1]
        # Add the SDW fc to the map
        sdw_fc_row = sdw_fc[(sdw_fc["date"] == date_sdw) & (sdw_fc["sensor"] == sensor_sdw)]
        GeoJson(sdw_fc_row, name=f"SDW {date_sdw}").add_to(self.map)

    def add_transects_fc(self):
        """
        Add the transects fc to the map.
        """
        GeoJson(transects_fc, name="Transects").add_to(self.map)
        # Show the transects id as labels on the map
        for i in transects_fc.index:
            folium.Marker(
                location=[transects_fc.loc[i, "geometry"].centroid.y,
                          transects_fc.loc[i, "geometry"].centroid.x],
                popup=f"Transect ID {i}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(self.map)
       
    def plot_raster(self):
        """
        Read the raster file and return the data.
        """
        # Get the date and sensor from the selected SDW
        date_sdw = self.sdw_selection.split(" - ")[0]
        date_sdw = pd.to_datetime(date_sdw).strftime("%Y-%m-%d")
        sensor_sdw = self.sdw_selection.split(" - ")[1]
        # Get the raster file name
        raster_file_name = os.path.join(rgb_folder_path, f"{date_sdw}-{sensor_sdw}.tif")
        # Read the raster file
        
        dst_crs = 'EPSG:4326'
        with rio.open(raster_file_name) as src:
            r, g, b = src.read()
            # Stack the bands
            rgb = np.dstack((r, g, b))
            # Normalize the bands to 0-1
            rgb = rgb / rgb.max()
            src_crs = src.crs['init'].upper()
            min_lon, min_lat, max_lon, max_lat = src.bounds
            
        # Conversion from UTM to WGS84 CRS
        bounds_orig = [[min_lat, min_lon], [max_lat, max_lon]]
        bounds_fin = []
        
        for item in bounds_orig:   
            #converting to lat/lon
            lat = item[0]
            lon = item[1]
            
            proj = Transformer.from_crs(int(src_crs.split(":")[1]), int(dst_crs.split(":")[1]), always_xy=True)
            lon_n, lat_n = proj.transform(lon, lat)

            bounds_fin.append([lat_n, lon_n])

        # Overlay raster (RGB) called img using add_child() function (opacity and bounding box set)
        self.map.add_child(folium.raster_layers.ImageOverlay(rgb,
                                                             name='RGB',
                                                             opacity=.7,
                                                             bounds=bounds_fin))
        # Center the map on the raster
        self.map.fit_bounds(bounds_fin)
        folium.LayerControl().add_to(self.map)
        #rgba_image = self.add_alpha(rgb_img)
        
        """
        with rio.open(
            os.path.join(rgb_folder_path, "test.tif"),
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=count,
            dtype=rgba_image.dtype,
            transform=transform
        ) as dst:
            # Write the NumPy array to the rasterio dataset
            dst.crs = rio.crs.CRS.from_epsg(4326)
            dst.write(rgba_image)
            # Add the raster to the map
            folium.raster_layers.ImageOverlay(
                image=rgba_image,
                bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                opacity=0.5
            ).add_to(self.map)"""
        """
        with rio.open(raster_file_name, "w") as src:
            # Transform the projection to EPSG 4326
            src.crs = rio.crs.CRS.from_epsg(4326)
            # Read the 3 bands RGB
            r, g, b = src.read()
            # Stack the bands
            rgb = np.dstack((r, g, b))
            # Normalize the bands
            #rgb = rgb / rgb.max()
            # Get the bounds
            bounds = src.bounds
            # Add the raster to the map
            folium.raster_layers.ImageOverlay(
                image=rgb,
                bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                opacity=0.5
            ).add_to(self.map)"""
            
    def open_map(self):
        """
        Open the map on the browser.
        """
        out_path = Path(input_info_file).parent.parent
        map_path = os.path.join(out_path, "map.html")
        self.map.save(map_path)
        webbrowser.open(map_path)