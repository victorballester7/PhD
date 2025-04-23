import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

# script to compare the decay of the energy of a mode when added to the baseflow vs the theoretical decay
# you will need to change the values of Emode_u, Emode_v, BF_uL2, BF_vL2, lamb to the values of the mode you are interested in


class Constants:
    ev_uL2: float
    ev_vL2: float
    bf_uL2: float
    bf_vL2: float
    lamb: float

    def __init__(
        self, ev_uL2: float, ev_vL2: float, bf_uL2: float, bf_vL2: float, lamb: float
    ):
        self.ev_uL2 = ev_uL2
        self.ev_vL2 = ev_vL2
        self.bf_uL2 = bf_uL2
        self.bf_vL2 = bf_vL2
        self.lamb = lamb


def read_history_points(file_path: str, use_u) -> Tuple[np.ndarray, np.ndarray]:
    """Read EnergyFile.mdl file and extract time and non-temporal variables.

    Args:
        file_path: Path to the file to read.

    Returns:
        A NumPy array containing the data with time and non-temporal variables.
    """
    data = np.loadtxt(file_path, skiprows=1)
    time = data[:, 0]
    if use_u:
        energy = data[:, 1]
    else:
        energy = data[:, 3]

    return time, energy


def plot_comparison(
    folder: str,
    file_name: str,
    use_log: bool,
    use_u: bool,
    time_min: Optional[float] = None,
    time_max: Optional[float] = None,
    scaling: float = 1,
    save: str = "",
) -> None:

    # w15
    config = Constants(ev_uL2=0.170774, ev_vL2=0.059097, bf_uL2=201.923, bf_vL2=0.508331, lamb=-0.00278899)

    # w16.5 (from SFD baseflow)
    # config = Constants(ev_uL2=0.190408, ev_vL2=0.0583767, bf_uL2=202.182, bf_vL2=0.511387, lamb=-0.00258415)

    # w16.5 (from SFD + DNS baseflow)
    # config = Constants(ev_uL2=0.189956, ev_vL2=0.0580036, bf_uL2=202.182, bf_vL2=0.511387, lamb=-0.00258418)

    # w26
    # config = Constants(ev_uL2=0.065906, ev_vL2=0.0549096, bf_uL2=203.854, bf_vL2=0.531642, lamb=0.00887819)

    file_path = os.path.join(folder, file_name)

    time, energy = np.array([]), np.array([])

    if os.path.exists(file_path):
        time, energy = read_history_points(file_path, use_u)
    else:
        print(f"Warning: File {file_path} does not exist. Skipping folder '{folder}'.")

    # Truncate variables to the smallest time range
    # time_max = min(len(ref_time), *[len(data[0]) for data in data_by_folder.values()])
    # ref_time = ref_time[:time_max]
    # ref_variables = ref_variables[:time_max]

    if time_min is not None:
        valid_indices = time >= time_min
        time, energy = time[valid_indices], energy[valid_indices]
    if time_max is not None:
        valid_indices = time <= time_max
        time, energy = time[valid_indices], energy[valid_indices]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.title.set_text("L2 norm of the energy of the" + (" u" if use_u else " v") + "-component")
    
    # truncate the name of folder to last m characters
    m = 12
    custom_label = folder
    if len(folder) > m:
        custom_label = folder[-m:]
        while custom_label[0] == "_":
            custom_label = custom_label[1:]
    if use_u:
        energy = energy / config.bf_uL2
    else:
        energy = energy / config.bf_vL2
    if use_log:
        energy = np.log10(energy)
    ax.plot(time, energy, label="Perturb. in NL sim.") 

    if use_u:
        E0 = config.ev_uL2 / config.bf_uL2
    else:
        E0 = config.ev_vL2 / config.bf_vL2
    E0 *= scaling
    energy_mode = E0 * np.exp(config.lamb * (time - time[0]))

    if use_log:
        energy_mode = np.log10(energy_mode)
        ax.plot(time, energy_mode, label=r"$\sim\lambda t$")
    else:
        ax.plot(time, energy_mode, label=r"$E_0 e^{\lambda t}$")

    ax.grid()
    ax.legend()

    # set x-axis to log scale

    ax.set_xlabel("Time")
    if use_u:
        ax.set_ylabel("Energy (u)")
    else:
        ax.set_ylabel("Energy (v)")
    plt.tight_layout()
    if save == "":
        plt.show()
    else:
        if save.endswith("/"):
            save += "energyL2_error_" + ("u" if use_u else "v") + ".png"
        plt.savefig(save)


def input(file_name: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Compare relative errors in {file_name} files across folders."
    )
    parser.add_argument("folder", help="Folder containing the files to compare.")
    parser.add_argument(
        "--file_name",
        default=file_name,
        help=f"Name of the file to read (default: {file_name}).",
    )
    parser.add_argument(
        "--use_log",
        action="store_true",
        help="Use log scale for the energy (default: False).",
    )
    parser.add_argument(
        "--use_u",
        action="store_true",
        help="Use u energy (default: True).",
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
        "--scaling",
        default=1,
        type=float,
        help="Scaling factor for the energy (default: 1).",
    )
    parser.add_argument(
        "--save",
        default="",
        type=str,
        help="Save the plot to a file, empty string to not save (default: '').",
    )

    return parser.parse_args()


if __name__ == "__main__":
    file_name = "ErrorEnergy.err"

    args = input(file_name)

    plot_comparison(
        args.folder,
        file_name=args.file_name,
        use_log=args.use_log,
        use_u=args.use_u,
        time_min=args.time_min,
        time_max=args.time_max,
        scaling=args.scaling,
        save=args.save,
    )
