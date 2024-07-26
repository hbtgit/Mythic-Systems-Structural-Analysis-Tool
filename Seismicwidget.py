import tkinter as tk

class SeismicInputWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.site_class_label = tk.Label(self, text="Site Class")
        self.site_class_label.grid(row=0, column=0)
        self.site_class_entry = tk.Entry(self)
        self.site_class_entry.grid(row=0, column=1)

        self.importance_factor_label = tk.Label(self, text="Importance Factor")
        self.importance_factor_label.grid(row=1, column=0)
        self.importance_factor_entry = tk.Entry(self)
        self.importance_factor_entry.grid(row=1, column=1)

        self.spectral_response_acceleration_label = tk.Label(self, text="Spectral Response Acceleration")
        self.spectral_response_acceleration_label.grid(row=2, column=0)
        self.spectral_response_acceleration_entry = tk.Entry(self)
        self.spectral_response_acceleration_entry.grid(row=2, column=1)

        # self.calculate_button = tk.Button(self, text="Calculate Seismic Load", command=self.calculate_seismic_load)
        # self.calculate_button.grid(row=3, columnspan=2)

    def calculate_seismic_load(self):
        # Retrieve user input
        site_class = self.site_class_entry.get()
        importance_factor = float(self.importance_factor_entry.get())
        spectral_response_acceleration = float(self.spectral_response_acceleration_entry.get())

        # Calculate seismic load (example calculation)
        seismic_load = self.compute_seismic_load(site_class, importance_factor, spectral_response_acceleration)
        print(f"Seismic Load: {seismic_load} kN")

    def compute_seismic_load(self, site_class, importance_factor, spectral_response_acceleration):
        # Implement the seismic load calculation logic here
        # Placeholder calculation
        seismic_load = importance_factor * spectral_response_acceleration * 100  # Example formula
        return seismic_load

# Integrate the widget into your main application
if __name__ == '__main__':
    root = tk.Tk()
    seismic_widget = SeismicInputWidget(master=root)
    seismic_widget.pack()
    root.mainloop()
