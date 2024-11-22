import os
import pandas as pd
import matplotlib.pyplot as plt

# Specify the time range
time_start = 10.5
time_end = 61.0

# Folder names
# folders = ["mode1", "mode2", "mode3", "mode4"]
folders = ["mode1", "mode2", "mode3", "mode4"]

# Initialize a dictionary to store data for each mode
mode_data = {}

# Read and process files
for folder in folders:
    file_path = os.path.join(folder, "EnergyFile.mdl")
    if os.path.exists(file_path):
        # Read the file into a pandas DataFrame
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, skiprows=1,
                           names=["Time", "Fourier_Mode", "Energy"])
        # Filter data based on the time range
        filtered_data = data[(data["Time"] >= time_start) & (data["Time"] <= time_end)]
        # Store the filtered data
        mode_data[folder] = filtered_data
    else:
        print(f"File not found: {file_path}")

# Plot the data
plt.figure(figsize=(10, 6))

for mode, data in mode_data.items():
    plt.plot(data["Time"], data["Energy"], label=mode)

plt.xlabel("Time")
plt.ylabel("Energy")
plt.title("Energy vs Time for Different Modes")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

