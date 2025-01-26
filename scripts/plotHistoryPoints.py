import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional

def read_history_points(file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Read HistoryPoints.his file and extract time and non-temporal variables.

    Args:
        file_path: Path to the HistoryPoints.his file.

    Returns:
        A NumPy array containing the data with time and non-temporal variables.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Extract data after the header
    data: List[List[float]] = []
    points_locations: List[List[float]] = []
    num_points: int = -1
    for line in lines:
        if not line.startswith("#"):
            try:
                data.append([float(value) for value in line.split()])
            except ValueError:
                continue
        else:
            num_points += 1
            if num_points > 0:
                points_locations.append([float(value) for value in line[1:].split()][1:])

    new_data = np.array([data[i::num_points] for i in range(num_points)])
    
    return new_data, np.array(points_locations)

def plot_comparison(
    folders: List[str], file_name: str = "HistoryPoints.his", point: int = 0, reference: int = 0, time_min: Optional[float] = None
) -> None:
    """Plot relative errors of non-temporal variables compared to a reference folder.

    Args:
        folders: List of folder paths to compare.
        file_name: Name of the file to read in each folder (default: "HistoryPoints.his").
        point: Index of the point to compare (default: 0).
        reference: Index of the folder to use as reference (default: 0).
        time_min: Minimum time value to include in the comparison (default: None).
    """
    data_by_folder: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
    variable_labels: Optional[List[str]] = ["u", "v", "p"]

    points_loc: np.ndarray = np.array([0, 0, 0])

    for i, folder in enumerate(folders):
        file_path = os.path.join(folder, file_name)
        if os.path.exists(file_path):
            if i == 0:
                data, points_loc = read_history_points(file_path)
            else:
                data, _ = read_history_points(file_path)
            
            time = data[point, :, 0]
            variables = data[point, :, 1:]

            if i == 0 and variables.shape[1] > 3:
                variable_labels = ["u", "v", "w", "p"]

            data_by_folder[folder] = (time, variables)
        else:
            print(f"Warning: File {file_path} does not exist. Skipping folder '{folder}'.")

    if not data_by_folder:
        print("No data found in any folder.")
        return

    ref_folder = folders[reference]
    if ref_folder not in data_by_folder:
        print(f"Reference folder '{ref_folder}' does not contain valid data.")
        return

    ref_time, ref_variables = data_by_folder[ref_folder]

    # Truncate variables to the smallest time range
    time_max = min(len(ref_time), *[len(data[0]) for data in data_by_folder.values()])
    ref_time = ref_time[:time_max]
    ref_variables = ref_variables[:time_max]

    if time_min is not None:
        valid_indices = ref_time >= time_min
        ref_time = ref_time[valid_indices]
        ref_variables = ref_variables[valid_indices]
        for folder in data_by_folder:
            time, variables = data_by_folder[folder]
            valid_indices = time[:time_max] >= time_min
            data_by_folder[folder] = (time[:time_max][valid_indices], variables[:time_max][valid_indices])

    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
    plt.suptitle(f"Relative Errors (Point {point}: x = {points_loc[point, 0]:.2f}, y = {points_loc[point, 1]:.2f}, z = {points_loc[point, 2]:.2f})")

    num_variables = len(variable_labels)
    for i, ax in enumerate(axes.flatten()):
        if i >= num_variables:
            break

        for folder, (time, variables) in data_by_folder.items():
            if folder == ref_folder:
                continue

            time = time[:time_max]
            variables = variables[:time_max]

            rel_error = np.abs((variables[:, i] - ref_variables[:, i]) / ref_variables[:, i])
            ax.plot(time, rel_error, label=f"{folder} (vs {ref_folder})")

        ax.set_ylabel(f"Relative Error: {variable_labels[i]}")
        ax.grid()
        ax.legend()

    axes[-1, 0].set_xlabel("Time")
    axes[-1, 1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare relative errors in HistoryPoints.his files across folders."
    )
    parser.add_argument("folders", nargs="+", help="List of folders to compare.")
    parser.add_argument(
        "--file_name",
        default="HistoryPoints.his",
        help="Name of the file to read (default: HistoryPoints.his).",
    )
    parser.add_argument(
        "--point", default=0, type=int, help="Point number to compare (default: 0)."
    )
    parser.add_argument(
        "--reference", default=0, type=int, help="Index of the reference folder (default: 0)."
    )
    parser.add_argument(
        "--time_min", default=None, type=float, help="Minimum time value to include in the comparison (default: None)."
    )
    args = parser.parse_args()

    plot_comparison(args.folders, file_name=args.file_name, point=args.point, reference=args.reference, time_min=args.time_min)

