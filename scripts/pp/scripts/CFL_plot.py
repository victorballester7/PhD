import re
import matplotlib.pyplot as plt
from pp.inputargs import parseArgs
import os
from pp.colors import colors


def main():
    """
    Main function to plot the CFL (Courant-Friedrichs-Lewy) values from the output.txt file as a function of time steps.
    It reads the output.txt file from the specified folder(s) and extracts the CFL values.
    """
    args = parseArgs()
    # Initialize an empty list to store the CFL values
    if len(args.folders) == 0:
        print(
            colors.WARNING
            + "No folders provided. Please specify at least one folder containing the output.txt file."
            + colors.ENDC
        )
        return

    output_folder = os.path.join(args.folders[0], "output.txt")

    cfl_values = []

    # Open the file and process it line by line
    try:
        with open(output_folder, "r") as file:
            for line in file:
                # Match lines that start with "CFL" and extract the value
                match = re.search(r"CFL:\s*([0-9.eE+-]+)", line)
                if match:
                    cfl_values.append(float(match.group(1)))
    except FileNotFoundError:
        print(
            colors.WARNING
            + f"File not found: {output_folder}. Please ensure the file exists in the specified folder."
            + colors.ENDC
        )
        return

    # Plot the CFL values
    plt.figure(figsize=(10, 6))
    plt.plot(cfl_values, label="CFL")
    plt.xlabel("Step Index")
    plt.ylabel("CFL Value")
    plt.title("CFL over Steps")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
