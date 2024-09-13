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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
            
            proj = Transformer.from_crs(int(src_crs.split(":")[1]),
                                        int(dst_crs.split(":")[1]), always_xy=True)
            lon_n, lat_n = proj.transform(lon, lat)

            bounds_fin.append([lat_n, lon_n])

        # Overlay raster (RGB) called img using add_child() function (opacity and bounding box set)
        self.map.add_child(folium.raster_layers.ImageOverlay(rgb,
                                                             name='RGB',
                                                             opacity=.7,
                                                             bounds=bounds_fin))
        # Center the map on the raster
        #self.map.fit_bounds(bounds_fin)
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