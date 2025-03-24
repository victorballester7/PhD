import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional


def read_history_points(file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Read EnergyFile.mdl file and extract time and non-temporal variables.

    Args:
        file_path: Path to the file to read.

    Returns:
        A NumPy array containing the data with time and non-temporal variables.
    """
    data = np.loadtxt(file_path, skiprows=1)
    time = data[:, 0]
    energy = data[:, 1]

    return time, energy


def plot_comparison(
    folders: List[str],
    file_name: str,
    time_min: Optional[float] = None,
    time_max: Optional[float] = None,
    save: str = "",
) -> None:
    data_by_folder: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}

    oldHistoryPoints = file_name + ".old"

    for i, folder in enumerate(folders):
        file_path = os.path.join(folder, file_name)
        if os.path.exists(file_path):
            time, energy = read_history_points(file_path)

            if os.path.exists(os.path.join(folder, oldHistoryPoints)):
                print(
                    f"Warning: File {oldHistoryPoints} exists in folder '{folder}'. Appending data from this file."
                )
                old_times, old_energies = read_history_points(
                    os.path.join(folder, oldHistoryPoints)
                )
                time = np.append(old_times, time)
                energy = np.append(old_energies, energy)

            data_by_folder[folder] = (time, energy)
        else:
            print(
                f"Warning: File {file_path} does not exist. Skipping folder '{folder}'."
            )

    if not data_by_folder:
        print("No data found in any folder.")
        return

    # Truncate variables to the smallest time range
    # time_max = min(len(ref_time), *[len(data[0]) for data in data_by_folder.values()])
    # ref_time = ref_time[:time_max]
    # ref_variables = ref_variables[:time_max]

    if time_min is not None:
        for folder in data_by_folder:
            time, energy = data_by_folder[folder]
            valid_indices = time >= time_min
            data_by_folder[folder] = (time[valid_indices], energy[valid_indices])
    if time_max is not None:
        for folder in data_by_folder:
            time, energy = data_by_folder[folder]
            valid_indices = time <= time_max
            data_by_folder[folder] = (time[valid_indices], energy[valid_indices])

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    mytime = np.array([])

    for folder, (time, energy) in data_by_folder.items():
        mytime = time
        custom_label = folder

        # time = time[:time_max]
        # variables = variables[:time_max]

        # truncate the name of folder to last m characters
        m = 12
        if len(folder) > m:
            custom_label = folder[-m:]
            while custom_label[0] == "_":
                custom_label = custom_label[1:]
        energy = np.log(energy)
        ax.plot(time, energy, label=custom_label)

    # global mode comparison
    lamb = -0.00258415 
    Emode_u = 0.0252569
    Emode_v = 0.00912989
    E0 = Emode_u
    energy_mode = (
        E0 * np.exp(lamb * (mytime - mytime[0]))  
    )

    # print(data_by_folder[folders[0]][1][-1])

    energy_mode = np.log(energy_mode)
    ax.plot(mytime, energy_mode, label="Global Mode")

    ax.grid()
    ax.legend()

    # set x-axis to log scale

    ax.set_xlabel("Time")
    ax.set_ylabel("Energy")
    plt.tight_layout()
    if save == "":
        plt.show()
    else:
        plt.savefig(save)


if __name__ == "__main__":
    file_name = "EnergyFile.mdl"

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
        "--time_min",
        default=None,
        type=float,
        help="Minimum time value to include in the comparison (default: None).",
    )
    parser.add_argument(
        "--time_max",
        default=None,
        type=float,
        help="Maximum time value to include in the comparison (default: None).",
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
        time_min=args.time_min,
        time_max=args.time_max,
        save=args.save,
    )
