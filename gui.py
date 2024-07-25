'''

**LICENSE**

Include a proper license file according to Mythic Systems' guidelines.

**Documentation Files**

Update any existing documentation files to include Mythic Systems' branding.

### 2. Add Branding to Code

Include a header with Mythic Systems branding in each Python file:

```python
# Mythic Systems Structural Analysis Tool
# (c) 2024 Mythic Systems
# All rights reserved.
'''
import matplotlib
#from main import *

# from calculate import calculate_area_from_coords
matplotlib.use('Agg')  # Use a non-interactive backend


from read_methods import *
from report import *
from widget import *
import ifcopenshell
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import simpledialog

def on_drop(event, values):
    # print(event, type(event))
    # for d in dir(event):
    #     try:
    #         print(">>> 1. ", d, eval(f'event.{d}()'))
    #     except Exception as e:
    #         print(">>> 2. ", d, eval(f'event.{d}'))
    # print(dir(values['snow_load_entry']))
    for k, v in values.items():
        try:
            print(k, v.get().strip() or "0")
        except:
            pass

    # Entry widgets
    roof_uplift_entry = values["roof_uplift_entry"]
    roof_downpressure_entry = values["roof_downpressure_entry"]
    wind_force_entry = values["wind_force_entry"]
    wall_height_entry = values["wall_height_entry"]
    snow_load_entry = values["snow_load_entry"]
    ice_load_entry = values["ice_load_entry"]
    site_class_entry = values["site_class_entry"]
    importance_factor_entry = values["importance_factor_entry"]
    spectral_response_acceleration_entry = values["spectral_response_acceleration_entry"]
    zero_check = values["remove_zero_point_var"]

    # Assume parse_ifc_file, extract methods, calculate methods are correctly implemented
    from read_methods import parse_ifc_file, extract_element_counts, extract_section_types, extract_floor_data, extract_forces_moments
    from calculate import calculate_perimeter, calculate_roof_perimeter, calculate_area_from_coords, calculate_snow_load, calculate_ice_load, calculate_wind_loads, calculate_dead_load, calculate_beam_column_weight, compute_seismic_load
    from report import create_Aux_pdf, plot_coordinates
    from widget import live_load_widget

    ifc_file_path = event.data.strip('{}')  # Remove curly braces if present
    coordinates = parse_ifc_file(ifc_file_path, zero_val=zero_check)
    areas = calculate_area_from_coords(coordinates)

    output_path = os.path.splitext(ifc_file_path)[0] + "_coordinate_plots.pdf"
    floor_count = extract_floor_data(ifc_file_path)
    forces, moments = extract_forces_moments(ifc_file_path)
    perimeter = calculate_perimeter(coordinates)
    roof_perimeter = calculate_roof_perimeter(coordinates)

    # Call the live_load_widget function to get live load inputs
    live_loads = live_load_widget(floor_count)
    print("Live Loads: ", live_loads)

    plot_coordinates(coordinates, areas, output_path, ifc_file_path)
    print(f"Output saved to: {output_path}")

    Aux_output_path = os.path.splitext(ifc_file_path)[0] + "_Aux.pdf"

    # Validate and convert inputs safely
    try:
        roof_uplift = float(roof_uplift_entry.get().strip() or "0")
        roof_downpressure = float(roof_downpressure_entry.get().strip() or "0")
        wind_force = float(wind_force_entry.get().strip() or "0")
        wall_height = float(wall_height_entry.get().strip() or "0")
        snow_load_per_unit_area = float(snow_load_entry.get().strip() or "0")
        ice_load_per_unit_area = float(ice_load_entry.get().strip() or "0")

        # Calculate total snow and ice loads
        roof_area = areas[0]  # Assuming the XY area is the roof area
        total_snow_load = calculate_snow_load(roof_area, snow_load_per_unit_area)
        ice_load_total = calculate_ice_load(roof_area, ice_load_per_unit_area)

        # Extract element counts
        element_counts = extract_element_counts(ifc_file_path)

        # Calculate wind loads
        wind_loads = calculate_wind_loads(ifc_file_path)

        # Calculate dead load
        dead_load = calculate_dead_load(ifc_file_path)

        # Calculate beam and column weights
        total_beam_weight, total_column_weight = calculate_beam_column_weight(ifc_file_path)

        # Create Auxiliary PDF
        create_Aux_pdf(
            element_counts, Aux_output_path, ifc_file_path, floor_count, forces, moments, perimeter,
            roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas,
            wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, ice_load_total, live_loads
        )

        # Message about the number of stories
        multi_story_msg = "The building is a single story."
        if floor_count > 1:
            multi_story_msg = f"The building has {floor_count} stories."

        messagebox.showinfo("Info", f"Plot saved to {output_path}\nAuxiliary data saved to {Aux_output_path}\n{multi_story_msg}")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid numbers: {e}")


# def on_drop(event):
#     root = TkinterDnD.Tk()
#     roof_uplift_entry = Entry(root)
#     roof_downpressure_entry = Entry(root)
#     wind_force_entry = Entry(root)
#     wall_height_entry = Entry(root)
#     from read_methods import parse_ifc_file,extract_element_counts,extract_section_types,extract_floor_data,extract_forces_moments
#     from calculate import calculate_perimeter,calculate_roof_perimeter,calculate_area_from_coords,calculate_snow_load,calculate_ice_load,calculate_wind_loads,calculate_dead_load 
#     ifc_file_path = event.data.strip('{}')  # Remove curly braces if present
#     coordinates = parse_ifc_file(ifc_file_path)
#     areas = calculate_area_from_coords(coordinates)
    
#     output_path = os.path.splitext(ifc_file_path)[0] + "_coordinate_plots.pdf"
#     floor_count = extract_floor_data(ifc_file_path)
#     forces, moments = extract_forces_moments(ifc_file_path)
#     perimeter = calculate_perimeter(coordinates)
#     roof_perimeter = calculate_roof_perimeter(coordinates)
#     # Call the live_load_widget function to get live load inputs
#     live_loads = live_load_widget(floor_count)
#     # Process live loads if needed (e.g., print them or integrate into further calculations)
#     print("Live Loads: ", live_loads)
#     plot_coordinates(coordinates, areas, output_path, ifc_file_path)
#     # forces, moments = extract_forces_moments(ifc_file_path)
#     # perimeter = calculate_perimeter(coordinates)
#     # roof_perimeter = calculate_roof_perimeter(coordinates)
    
#     plot_coordinates(coordinates, areas, output_path, ifc_file_path)
#     print(f"Output saved to: {output_path}")
#     Aux_output_path = os.path.splitext(ifc_file_path)[0] + "_Aux.pdf"
    
#     roof_uplift = float(roof_uplift_entry.get())
#     roof_downpressure = float(roof_downpressure_entry.get())
#     wind_force = float(wind_force_entry.get())
#     wall_height = float(wall_height_entry.get())
    
#     try:
#         snow_load_per_unit_area = float(snow_load_entry.get())  # Get the snow load per unit area
#         ice_load_per_unit_area = float(ice_load_entry.get())  # Get the ice load per unit area
#         roof_uplift_pressure = float(roof_uplift_entry.get())
#         roof_downpressure = float(roof_downpressure_entry.get())
#         wind_force = float(wind_force_entry.get())
#         wall_height = float(wall_height_entry.get())
        
#         # Continue with your logic
#         # For example, you could calculate the snow load and display it
#         snow_load_total = snow_load_per_unit_area * wall_height  # Example calculation
#         # messagebox.showinfo("Snow Load", f"Total Snow Load: {snow_load_total} lbs")
#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter valid numbers")
#     snow_load_per_unit_area = float(snow_load_entry.get())  # Get the snow load per unit area
#     ice_load_per_unit_area = float(ice_load_entry.get())  # Get the ice load per unit area
#     # Calculate snow load
#     roof_area = areas[0]  # Assuming the XY area is the roof area
#     total_snow_load = calculate_snow_load(roof_area, snow_load_per_unit_area)
#     ice_load_total = calculate_ice_load(roof_area, ice_load_per_unit_area)
    
#     # Extract element counts
#     element_counts = extract_element_counts(ifc_file_path)
    
#     # Calculate wind loads
#     wind_loads = calculate_wind_loads(ifc_file_path)
    
#     # Calculate dead load
#     dead_load = calculate_dead_load(ifc_file_path)
    
#     # Calculate beam and column weights
#     total_beam_weight, total_column_weight = calculate_beam_column_weight(ifc_file_path)
#     create_Aux_pdf(element_counts, Aux_output_path, ifc_file_path, floor_count, forces, moments, perimeter, roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas, wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, ice_load_total, live_loads)
    
#     section_types = extract_section_types(ifc_file_path)
    
#     multi_story_msg = "The building is a single story."
#     if floor_count > 1:
#         multi_story_msg = f"The building has {floor_count} stories."

#     messagebox.showinfo("Info", f"Plot saved to {output_path}\nAuxiliary data saved to {Aux_output_path}")
