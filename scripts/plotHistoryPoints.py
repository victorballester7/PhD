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
                points_locations.append(
                    [float(value) for value in line[1:].split()][1:]
                )

    # for i in range(num_points):
    #     print(np.array(data[i::num_points]).shape)

    new_data = np.array([data[i::num_points] for i in range(num_points)])

    return new_data, np.array(points_locations)


def plot_comparison(
    folders: List[str],
    file_name: str = "HistoryPoints.his",
    points: List[int] = [0],
    reference: int = 0,
    time_min: Optional[float] = None,
    use_relative: bool = False,
    save: str = "",
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

    oldHistoryPoints = "HistoryPoints.his.old"

    for i, folder in enumerate(folders):
        file_path = os.path.join(folder, file_name)
        if os.path.exists(file_path):
            if i == 0:
                data, points_loc = read_history_points(file_path)
            else:
                data, _ = read_history_points(file_path)

            if os.path.exists(os.path.join(folder, oldHistoryPoints)):
                print(
                    f"Warning: File {oldHistoryPoints} exists in folder '{folder}'. Appending data from this file."
                )
                old_data, _ = read_history_points(
                    os.path.join(folder, oldHistoryPoints)
                )
                data = np.append(old_data, data, axis=1)

            time = data[points, :, 0]
            variables = data[points, :, 1:]

            if i == 0 and variables.shape[-1] > 3:
                variable_labels = ["u", "v", "w", "p"]

            data_by_folder[folder] = (time, variables)
        else:
            print(
                f"Warning: File {file_path} does not exist. Skipping folder '{folder}'."
            )

    if points_loc.shape[0] == 0:
        print(
            "No points locations found. Probably the file is empty or does not exist."
        )
        return
    # print points locations for reference
    num_variables = len(variable_labels)
    for i in range(points_loc.shape[0]):
        if "w" in variable_labels:
            print(
                f"Point {i}: x = {points_loc[i, 0]:.2f}, y = {points_loc[i, 1]:.2f}, z = {points_loc[i, 2]:.2f}"
            )
        else:
            print(
                f"Point {i}: x = {points_loc[i, 0]:.2f}, y = {points_loc[i, 1]:.2f}"
            )

    if not data_by_folder:
        print("No data found in any folder.")
        return

    ref_folder = folders[reference]
    if ref_folder not in data_by_folder:
        print(f"Reference folder '{ref_folder}' does not contain valid data.")
        return

    ref_time, ref_variables = data_by_folder[ref_folder]

    # Truncate variables to the smallest time range
    # time_max = min(len(ref_time), *[len(data[0]) for data in data_by_folder.values()])
    # ref_time = ref_time[:time_max]
    # ref_variables = ref_variables[:time_max]

    if time_min is not None:
        valid_indices = ref_time[0] >= time_min
        ref_time = ref_time[0, valid_indices]
        ref_variables = ref_variables[0, valid_indices]
        for folder in data_by_folder:
            time, variables = data_by_folder[folder]
            valid_indices = time >= time_min
            data_by_folder[folder] = (
                time[:, valid_indices],
                variables[:, valid_indices],
            )

    if num_variables == 3:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True)
    else:
        fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True)

    for i, ax in enumerate(axes.flatten()):
        if i >= num_variables:
            break

        for folder, (time, variables) in data_by_folder.items():
            if use_relative and folder == ref_folder:
                continue

            custom_label = folder

            # time = time[:time_max]
            # variables = variables[:time_max]

            for j, p in enumerate(points):
                if use_relative:
                    plot = np.abs(
                        (variables[j, :, i] - ref_variables[j, :, i]) / ref_variables[j, :, i]
                    )
                    custom_label = f"{folder} (vs {ref_folder})"
                else:
                    plot = variables[j, :, i]
                    # truncate the name of folder to last m characters
                    m = 10
                    if len(folder) > m:
                        custom_label = folder[-m:]
                        while custom_label[0] == "_":
                            custom_label = custom_label[1:]
                    if "w" in variable_labels:
                        custom_label = (
                            custom_label
                            + f" point {p}: ({points_loc[p, 0]:.2f}, {points_loc[p, 1]:.2f}, {points_loc[p, 2]:.2f})"
                        )
                    else:
                        custom_label = (
                            custom_label
                            + f" point {p}: ({points_loc[p, 0]:.2f}, {points_loc[p, 1]:.2f})"
                        )
                ax.plot(time[j], plot, label=custom_label)

        if use_relative:
            ax.set_ylabel(f"Relative Error: {variable_labels[i]}")
        else:
            ax.set_ylabel(f"{variable_labels[i]}")
        ax.grid()
        ax.legend()

    if num_variables == 3:
        axes[0].set_xlabel("Time")
        axes[1].set_xlabel("Time")
        axes[2].set_xlabel("Time")
    else:
        axes[-1, 0].set_xlabel("Time")
        axes[-1, 1].set_xlabel("Time")
    plt.tight_layout()
    if save == "":
        plt.show()
    else:
        plt.savefig(save)


if __name__ == "__main__":
    import argparse

    file_name = "HistoryPoints.his"

    parser = argparse.ArgumentParser(
        description=f"Compare relative errors in {file_name} files across folders."
    )
    parser.add_argument("folders", nargs="+", help="List of folders to compare.")
    parser.add_argument(
        "--file_name",
        default=file_name,
        help=f"Name of the file to read (default: {file_name}).",
    )
    parser.add_argument(
        "--points", metavar='int', nargs='+', type=int, default=[0], help="Point number to compare (default: [0]).",
    )
    parser.add_argument(
        "--reference",
        default=0,
        type=int,
        help="Index of the reference folder (default: 0).",
    )
    parser.add_argument(
        "--time_min",
        default=None,
        type=float,
        help="Minimum time value to include in the comparison (default: None).",
    )
    parser.add_argument(
        "--use_relative",
        default=False,
        type=bool,
        help="Use relative error instead of absolute error (default: False).",
    )
    parser.add_argument(
        "--save",
        default="",
        type=str,
        help="Save the plot to a file, empty string to not save (default: '').",
    )
    args = parser.parse_args()

    plot_comparison(
        args.folders,
        file_name=args.file_name,
        points=args.points,
        reference=args.reference,
        time_min=args.time_min,
        use_relative=args.use_relative,
        save=args.save,
    )
