import numpy as np
import argparse
import matplotlib.pyplot as plt
from plotHistoryPoints import read_all_folders, reduceLengthFolder
import re


def extract_width(filenameFolder: str) -> float:
    """
    Extract width (YYY) from the filename of the form *dXXX_wYYY*
    Args:
        filenameFolder: Path to the folder containing the file.
    Returns:
        Width value extracted from the filename.
    """

    match = re.search(r"d(\d+(?:\.\d+)?)_w(\d+(?:\.\d+)?)", filenameFolder)
    depth = 0
    width = 0
    if match:
        depth = float(match.group(1))
        width = float(match.group(2))
    if not match:
        # raise ValueError(f"Could not extract width from filename: {filenameFolder}")
        print(f"Could not extract width from filename: {filenameFolder}. Returning default values : depth = {depth}, width = {width}")
    return float(width)


def getTimesMaxima(t: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Get the maximums of the signal (after it stabilizes) from the time and variable arrays.
    Args:
        t: Time array.
        v: V velocity array.
    Returns:
        Array of maximum values.
    """

    diff_v = np.gradient(v, t)
    max_indices = np.where(np.diff(np.sign(diff_v)))[0]
    
    times_max = []
    for i in max_indices:
        fi = diff_v[i]
        fi1 = diff_v[i + 1]
        ti = t[i]
        ti1 = t[i + 1]
        t_zero = ti - fi * (ti1 - ti) / (fi1 - fi)
        times_max.append(t_zero)

    times_max = np.array(times_max)
    return times_max


def getAmplitudes(
    times_max: np.ndarray, time: np.ndarray, var: np.ndarray
) -> np.ndarray:
    """
    Interpolate the variable to the times of the maximums and return the amplitudes.
    Args:
        times_max: Array of maximum times.
        var: Variable array (U or V velocity).
    Returns:
        Array of amplitudes.
    """
    var_interpolated = np.interp(times_max, time, var)
    return var_interpolated

def get_amplitude_wave_packet(indices: np.ndarray, t: np.ndarray, data: np.ndarray) -> float:
    """
    Get the amplitude of the wave packet based on the indices of the maxima.
    Args:
        indices: Indices of the maxima.
        t: Time array.
        data: Data array (U or V velocity).
    Returns:
        Amplitude value.
    """
    times_max = t[indices]
    data_max = data[indices]

    # get interpolation of the maxima based on 2nd order polynomial
    coeffs = np.polyfit(times_max, data_max, 2)
    # get the vertex of the parabola (the maximum)
    vertex_time = -coeffs[1] / (2 * coeffs[0])
    # get the maximum value at the vertex time
    A_critical = np.polyval(coeffs, vertex_time)

    return A_critical

def get_amplitude(t: np.ndarray, u: np.ndarray, v: np.ndarray, use_u: bool, is_wave_packet: bool) -> float:
    """
    Get the amplitude of the signal (after it stabilizes) from the time and variable arrays.
    Args:
        t: Time array.
        u: U velocity array.
        v: V velocity array.
        use_u: If True, return amplitude of U velocity; otherwise, return amplitude of V velocity.
    Returns:
        Amplitude value.
    """
    if is_wave_packet:
        # data = u if use_u else v

        # get x, y corresponding to the 3 greatest maxima
        A_max_u = get_amplitude_wave_packet(np.argsort(u)[-3:], t, u)
        A_max_v = get_amplitude_wave_packet(np.argsort(v)[-3:], t, v)
        A_min_u = get_amplitude_wave_packet(np.argsort(u)[:3], t, u)
        A_min_v = get_amplitude_wave_packet(np.argsort(v)[:3], t, v)

        A = np.mean([A_max_u, A_max_v, -A_min_u, -A_min_v]).astype(np.float64)


    else:
        times_max = getTimesMaxima(t, v)

        A = getAmplitudes(times_max, t, u if use_u else v)

        # separate the maxima and minima
        A_plus = A[A > A.mean()]
        A_minus = A[A < A.mean()]

        num_peaks2average = 3
        A = (0.5 * (np.mean(A_plus[-num_peaks2average:]) - np.mean(A_minus[-num_peaks2average:]))).astype(np.float64)

    return A


def plot_nFactor(
    folders: list[str],
    file_name: str = "HistoryPoints.his",
    save: str = "",
) -> None:
    """
    Plot nFactor curve from values from HistoryPoints.his files in different folders.

    Args:
        folders: List of folder paths to compare.
        file_name: Name of the file to read in each folder (default: "HistoryPoints.his").
        save: Path to save the plot (default: "").
    """

    data_by_folder, variables = read_all_folders(folders, file_name, slice(None))

    heightBL = 1
    XafterGap = -35
    use_u = False  # otherwise use v
    is_wave_packet = True  # if True, use wave packet amplitude calculation

    fig, ax = plt.subplots(figsize=(8, 5))

    for folder, (points_loc, time, variables) in data_by_folder.items():
        width = extract_width(folder)
        X = []
        n_x = []
        baseAmplitudeSet = False
        baseAmplitude = 0
        print(f"Folder: {folder}")
        for p, point in enumerate(points_loc):
            if point[1] != heightBL or point[0] < XafterGap + width:
                continue
            t = time[p]
            print(
                    f"    Point {p}: x = {points_loc[p, 0]:.2f}, y = {points_loc[p, 1]:.2f}, z = {points_loc[p, 2]:.2f}"
                )
            # if p % 100 == 0:
            A = get_amplitude(t, variables[p, :, 0], variables[p, :, 1], use_u, is_wave_packet)

            if not baseAmplitudeSet:
                baseAmplitude = A
                baseAmplitudeSet = True

            X.append(point[0])
            n_x.append(np.log(A / baseAmplitude))

        X = np.array(X)
        n_x = np.array(n_x)
        ax.plot(X, n_x, label=reduceLengthFolder(folder, 14))

    ax.set_xlabel("x / delta*")
    ax.set_ylabel("n(x)")
    ax.legend()
    ax.set_title("n(x) curve")
    ax.grid()
    if save == "":
        plt.show()
    else:
        plt.savefig(save)


if __name__ == "__main__":
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
        "--save",
        default="",
        type=str,
        help="Save the plot to a file, empty string to not save (default: '').",
    )
    args = parser.parse_args()

    plot_nFactor(
        args.folders,
        file_name=args.file_name,
        save=args.save,
    )
