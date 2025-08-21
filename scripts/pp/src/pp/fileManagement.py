import re
import os
import numpy as np
from pp.colors import colors
from typing import Tuple, List, Dict


def extract_width_depth(filenameFolder: str) -> Tuple[float, float]:
    """
    Extract width (YYY) and depth (XXX) from the filename of the form *dXXX_wYYY*
    Args:
        filenameFolder: Path to the folder containing the file.
    Returns:
        Width and depth values extracted from the filename. Defaults to 0 if not found.
    """

    match = re.search(r"d(\d+(?:\.\d+)?)_w(\d+(?:\.\d+)?)", filenameFolder)
    depth = 0
    width = 0
    if match:
        depth = float(match.group(1))
        width = float(match.group(2))
    if not match:
        print( colors.WARNING + 
            f"Could not extract width from filename: {filenameFolder}. Returning default values : depth = {depth}, width = {width}" + colors.ENDC
        )
    return float(width), float(depth)

def readDataHistoryPointsMultiple(folders: np.ndarray) -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Reads data from the HistoryPoints files in the specified folders.

    Args:
        folders: List of paths to the folders containing the HistoryPoints files.
    Returns:
        A dictionary where each key is a folder path and the value is a tuple containing:
            - points: An array of points.
            - time: An array of time values.
            - fields: An array of fields (e.g. u, v, p) at every point (axis 0) and timestep (axis 1).
    """
    data = {}
    for folder in folders:
        points, time, fields = readDataHistoryPoints(folder)
        data[folder] = (points, time, fields)
    return data

def readDataHistoryPoints(folder: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Reads data from the HistoryPoints file in the specified folder.

    Args:
        folder: Path to the folder containing the HistoryPoints file.
    Returns:
        A tuple containing:
            - points: An array of points.
            - time: An array of time values.
            - fiedls: An array of fields (e.g. u, v, p) at every point (axis 0) and timestep (axis 1).
    """
    file_nameHistoryPoints = "HistoryPoints.his"
    old_file_nameHistoryPoints = f"{file_nameHistoryPoints}.old"

    oldPath = os.path.join(folder, old_file_nameHistoryPoints)
    newPath = os.path.join(folder, file_nameHistoryPoints)

    points_old, data_old = np.array([]), np.array([])

    points_new, time_new, fields_new = _readDataHistoryPoints(newPath)
    
    if os.path.exists(oldPath):
        points_old, time_old, fields_old = _readDataHistoryPoints(oldPath)
    
        if points_old.size != points_new.size:
            print(colors.WARNING + 
                f"Warning: File {old_file_nameHistoryPoints} is detected but has a different number of points than {file_nameHistoryPoints}. Ignoring {old_file_nameHistoryPoints}." + colors.ENDC
            )
        elif points_old.size == points_new.size:
            print(colors.OKGREEN + 
                f"Info: File {old_file_nameHistoryPoints} is detected and has the same number of points as {file_nameHistoryPoints}. Merging data." + colors.ENDC
            )

            # merge data
            time_new = np.concatenate((time_old, time_new))
            fields_new = np.concatenate((fields_old, fields_new), axis=1)

    return points_new, time_new, fields_new

def _readDataHistoryPoints(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Reads data from the HistoryPoints file in the specified folder.

    Args:
        folder: Path to the folder containing the HistoryPoints file.
    Returns:
        A tuple containing:
            - points: An array of points.
            - time: An array of time values.
            - fields: An array of fields (e.g. u, v, p) at every point (axis 0) and timestep (axis 1).
    """
    # Extract data after the header
    data: List[List[float]] = []
    points_locations: List[List[float]] = []
    num_points = -1
    with open(path, "r") as f:
        for line in f:
            if not line.startswith("#"):
                try:
                    data.append([float(value) for value in line.split()])
                except ValueError:
                    continue
            else:
                num_points += 1
                if num_points > 0:
                    points_locations.append(
                        [float(value) for value in line[1:].split()][1:]
                    )

    new_data = np.array([data[i::num_points] for i in range(num_points)])

    print(colors.OKBLUE +
          f"Read {len(data)} data points from {path}" + colors.ENDC)

    time = new_data[0, :, 0]  # we take the first column (time) from the first point
    variables = new_data[:, :, 1:]  # we take all columns except the first one (time)

    return np.array(points_locations), time, variables
