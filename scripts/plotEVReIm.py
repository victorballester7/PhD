import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
import re
import argparse


def readData(file_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Read Eigenvalues from .evl file"""
    with open(file_path, "r") as file:
        lines = file.readlines()

    iteration_pattern = re.compile(r"-- Iteration = (\d+),")

    last_iteration_start = None

    for i, line in enumerate(lines):
        match = iteration_pattern.match(line)
        if match:
            last_iteration_start = i

    if last_iteration_start is None:
        raise ValueError("No iteration found in file")

    growth_values = []
    frequency_values = []
    residuals = []

    for line in lines[
        last_iteration_start + 2 :
    ]:  # Saltamos la línea del encabezado de valores
        linesplit = line.split()
        growth_values.append(float(linesplit[4]))
        frequency_values.append(float(linesplit[5]))
        residuals.append(float(linesplit[6]))

    return np.array(growth_values), np.array(frequency_values), np.array(residuals)


def dataPostProcess(
    Re: np.ndarray, Im: np.ndarray, error: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Post-process data
    Only keep the values that have small residuals"""

    # we keep to significant digits
    error_threshold = 0.001

    Re_err = np.abs(error / Re)
    Im_err = np.abs(error / Re)

    bool_arr = np.sqrt(Re_err ** 2 + Im_err ** 2) < error_threshold

    Re_filtered = Re[bool_arr]
    Im_filtered = Im[bool_arr]

    return Re_filtered, Im_filtered


def extractNameFolder(path: str) -> Optional[str]:
    """Extracts the 'dX_wY' part from a given path string.
    
    Args:
        path (str): The input path string.

    Returns:
        Optional[str]: The extracted 'dX_wY' string or None if not found.
    """
    match = re.search(r"d\d+(\.\d+)?_w\d+(\.\d+)?", path)
    return match.group(0) if match else None




def plotEV(folders: List[str], save: str = "") -> None:
    """Plot Re vs Im of eigenvalues for different widths"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    for folder in folders:
        name = extractNameFolder(folder)
        Re, Im, error = readData(os.path.join(folder, "mesh_" + name + ".evl"))
        Re, Im = dataPostProcess(Re, Im, error)
        ax.plot(Im, Re, label=folder, marker="o", linestyle="None")

    ax.set_xlabel("Im")
    ax.set_ylabel("Re")
    ax.set_title("Eigenvalues")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    if save == "":
        plt.show()
    else:
        plt.savefig(save)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare relative errors in *.evl files across folders."
    )
    parser.add_argument("folders", nargs="+", help="List of folders to compare.")

    parser.add_argument(
        "--save",
        default="",
        type=str,
        help="Save the plot to a file, empty string to not save (default: '').",
    )
    args = parser.parse_args()

    plotEV(args.folders, save=args.save)
