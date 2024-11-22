import re
import matplotlib.pyplot as plt

# Initialize an empty list to store the CFL values
cfl_values = []

# Open the file and process it line by line
with open("output.txt", "r") as file:
    for line in file:
        # Match lines that start with "CFL" and extract the value
        match = re.match(r"CFL \(zero plane\): ([\d.eE+-]+)", line)
        if match:
            cfl_values.append(float(match.group(1)))

# Plot the CFL values
plt.figure(figsize=(10, 6))
plt.plot(cfl_values, color="blue", label="CFL (zero plane)")
plt.xlabel("Step Index")
plt.ylabel("CFL Value")
plt.title("CFL (zero plane) over Steps")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

