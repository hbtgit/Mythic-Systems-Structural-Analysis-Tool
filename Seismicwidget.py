import tkinter as tk
from tkinter import BooleanVar, Label, Entry, Checkbutton
from tkinterdnd2 import TkinterDnD, DND_FILES


import tkinter as tk

def calculate_seismic_load(site_class_entry, importance_factor_entry, spectral_response_acceleration_entry):
    # Retrieve user input
    site_class = site_class_entry.get()
    importance_factor = float(importance_factor_entry.get())
    spectral_response_acceleration = float(spectral_response_acceleration_entry.get())

    # Calculate seismic load
    seismic_load = compute_seismic_load(site_class, importance_factor, spectral_response_acceleration)
    print(f"Seismic Load: {seismic_load} kN")

def compute_seismic_load(site_class, importance_factor, spectral_response_acceleration):
    # Define amplification factors for different site classes
    amplification_factors = {
        'A': 0.8,
        'B': 1.0,
        'C': 1.2,
        'D': 1.4,
        'E': 1.6
    }

    # Get the amplification factor for the given site class
    amplification_factor = amplification_factors.get(site_class.upper(), 1.0)  # Default to 1.0 if site class is not found

    # Calculate the seismic load
    seismic_load = importance_factor * spectral_response_acceleration * amplification_factor
    return seismic_load

def create_seismic_input_widgets(master):
    # Create and place widgets
    site_class_label = tk.Label(master, text="Site Class")
    site_class_label.grid(row=0, column=0)
    site_class_entry = tk.Entry(master)
    site_class_entry.grid(row=0, column=1)

    importance_factor_label = tk.Label(master, text="Importance Factor")
    importance_factor_label.grid(row=1, column=0)
    importance_factor_entry = tk.Entry(master)
    importance_factor_entry.grid(row=1, column=1)

    spectral_response_acceleration_label = tk.Label(master, text="Spectral Response Acceleration")
    spectral_response_acceleration_label.grid(row=2, column=0)
    spectral_response_acceleration_entry = tk.Entry(master)
    spectral_response_acceleration_entry.grid(row=2, column=1)

    calculate_button = tk.Button(master, text="Calculate Seismic Load", 
                                 command=lambda: calculate_seismic_load(site_class_entry, 
                                                                        importance_factor_entry, 
                                                                        spectral_response_acceleration_entry))
    calculate_button.grid(row=3, columnspan=2)

    return master
