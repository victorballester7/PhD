import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.stats import normaltest
from statsmodels.tsa.stattools import acf
import argparse
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from plotHistoryPoints import read_all_folders, reduceLengthFolder
import re
from scipy.fft import rfft, irfft, rfftfreq, fft, fftfreq
from typing import Tuple
from scipy.signal import hilbert, spectrogram
from scipy.stats import entropy
from scipy.interpolate import griddata, NearestNDInterpolator,SmoothBivariateSpline
import os
from scipy.spatial import Delaunay, ConvexHull
import plotStabilityCurve_wVSd
from scipy.ndimage import gaussian_filter

# dictionary of signal types
signal_types = {
    "sinusoidal": "Sinusoidal signal",
    "wave_packet": "Wave packet signal",
    "gaussian_noise": "White Gaussian noise",
}


def extract_width_depth(filenameFolder: str) -> Tuple[float, float]:
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
        print(
            f"Could not extract width from filename: {filenameFolder}. Returning default values : depth = {depth}, width = {width}"
        )
    return float(width), float(depth)


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


def get_amplitude_wave_packet(
    indices: np.ndarray, t: np.ndarray, data: np.ndarray
) -> float:
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


def get_amplitude(
    t: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    use_u: bool,
    signal_type: str,
) -> float:
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
    if signal_type == signal_types["wave_packet"]:
        # data = u if use_u else v

        # indx of the maxima in u
        idx_max_u = np.argsort(u)[-5:]

        interval_time = 500

        idx1 = 0
        idx2 = len(t) - 1
        for i in idx_max_u:
            if t[i] < interval_time or t[i] > t[-1] - interval_time:
                continue
            else:
                # get idx1 = time[i] - interval_time
                idx1 = np.where(t < t[i] - interval_time)[0][-1]
                # get idx2 = time[i] + interval_time
                idx2 = np.where(t > t[i] + interval_time)[0][0]
                break

        t = t[idx1:idx2]
        u = u[idx1:idx2]
        v = v[idx1:idx2]

        # get x, y corresponding to the 3 greatest maxima
        A_max_u = get_amplitude_wave_packet(np.argsort(u)[-3:], t, u)
        A_min_u = get_amplitude_wave_packet(np.argsort(u)[:3], t, u)
        # A_max_v = get_amplitude_wave_packet(np.argsort(v)[-3:], t, v)
        # A_min_v = get_amplitude_wave_packet(np.argsort(v)[:3], t, v)

        A = np.mean([A_max_u, -A_min_u]).astype(np.float64)
        # A = np.mean([A_max_u, A_max_v, -A_min_u, -A_min_v]).astype(np.float64)

    elif signal_type == signal_types["sinusoidal"]:
        # we assume that the sinusoidal signal is stabilized, so we can use the maxima
        times_max = getTimesMaxima(t, u if use_u else v)

        A = getAmplitudes(times_max, t, u if use_u else v)

        # separate the maxima and minima
        A_plus = A[A > A.mean()]
        A_minus = A[A < A.mean()]

        num_peaks2average = 3
        A = (
            0.5
            * (
                np.mean(A_plus[-num_peaks2average:])
                - np.mean(A_minus[-num_peaks2average:])
            )
        ).astype(np.float64)

        # hold the process for a while to see the plot

    else:  # is_wgn
        data = u if use_u else v
        # num_peaks2average = 1
        # data_sorted = np.sort(data)
        # A_max = data_sorted[-num_peaks2average:]
        # A_min = data_sorted[:num_peaks2average]
        # A = 0.5 * (np.mean(A_max) - np.mean(A_min)).astype(np.float64)

        # rms error
        A = np.sqrt(np.mean(u**2 + v**2)).astype(np.float64)

    return A


# def is_gaussian_noise(signal, alpha=0.005, acf_lags=20):
#     """
#     Returns True if the signal looks like white Gaussian noise.

#     Args:
#         signal (np.ndarray): 1D array of signal values.
#         alpha (float): Significance level for the normality test.
#         acf_lags (int): Number of lags to check for whiteness (autocorrelation).

#     Returns:
#         bool: True if signal is Gaussian and white.
#     """
#     # Test for Gaussianity
#     stat, p_normal = normaltest(signal)
#     print(f"p-value for normality test: {p_normal}")
#     print(f"Significance level: {alpha}")
#     is_gaussian = p_normal > alpha

#     return is_gaussian


# def is_wave_packet_signal(data: np.ndarray) -> bool:
#     # check if the 5 greatest maxima are within x% to each other
#     eps = 0.05
#     indices = np.argsort(data)[-5:]
#     max_values = data[indices]
#     print(f"Max values: {max_values}")
#     max_diff = np.max(max_values) - np.min(max_values)

#     ref_var = 1e-7
#     var = np.var(data)

#     print(f"Variance: {var}")
#     print(f"Max difference: {max_diff}")
#     print(f"max diff / mean: {max_diff / np.mean(max_values)}")
#     if max_diff / np.mean(max_values) < eps and var > ref_var:
#         return False  # not a wave packet
#     else:
#         return True


def classify_signal(time, signal):
    N = len(signal)

    # FFT
    freqs = fftfreq(N, d=(time[1] - time[0]))
    fft_mag = np.abs(fft(signal))
    positive_freqs = freqs[: N // 2]
    positive_mag = fft_mag[: N // 2]

    # Spectral entropy
    # psd = positive_mag**2
    # psd_norm = psd / np.sum(psd)
    # spectral_entropy = entropy(psd_norm)

    # Time localization (via envelope)
    envelope = np.abs(
        hilbert(signal)
    )  # hilbert return the analytic signal: X(t) + i * Y(t), where Y(t) is the Hilbert transform of X(t). For sinusoidal signals, H(sin(t)) = cos(t), and so, the envelope (amplitude) is sqrt(X(t)^2 + Y(t)^2) = sqrt(sin(t)^2 + cos(t)^2) = 1, so std of envelope is 0.
    envelope_std = np.std(envelope)

    # Peakiness of spectrum
    peak_ratio = np.max(positive_mag) / np.mean(positive_mag)
    print(f"Peak ratio: {peak_ratio}")
    # print(f"Spectral entropy: {spectral_entropy}")
    print(f"Envelope std: {envelope_std}")

    # Heuristics for classification
    if peak_ratio < 10:
        return signal_types["gaussian_noise"]
    elif envelope_std < 0.1:
        return signal_types["sinusoidal"]
    else:
        return signal_types["wave_packet"]


def getBaseAmplitude(X: np.ndarray, n_x: np.ndarray) -> Tuple[float, float]:
    XmaxBaseAmplitude = 0  # maximum amplitude to consider it as the base amplitude

    index = np.where(X < XmaxBaseAmplitude)[0]
    n_x_first = n_x[index]

    # get the minimum positive value of n_x_first
    threshold = 1e-8
    X_first = X[index][n_x_first > threshold]
    n_x_first = n_x_first[n_x_first > threshold]
    index_min = np.argmin(n_x_first)
    return X_first[index_min], n_x_first[index_min]


def nfactor_wgn(
    points_loc: np.ndarray,
    time: np.ndarray,
    variables: np.ndarray,
    ax,
    use_u: bool,
    heightBL: float,
    XafterGap: float,
    width: float,
) -> None:
    x_loc = []
    y_loc = []
    ffts = []
    freqs = []

    time0 = 3000
    count = 0

    for p, point in enumerate(points_loc):
        if point[1] != heightBL or point[0] < XafterGap + width:
            continue
        idx1 = np.where(time[p] < time0)[0][0]
        t = time[p][idx1:]
        data = variables[p, idx1:, 0] if use_u else variables[p, idx1:, 1]
        fft_data = rfft(data)
        freq = rfftfreq(len(data), d=(t[1] - t[0]))
        x_loc.append(point[0])
        y_loc.append(point[1])
        ffts.append(fft_data)
        if count == 0:
            count += 1
            freqs = freq

    ffts = np.abs(np.array(ffts))
    x_loc = np.array(x_loc)
    y_loc = np.array(y_loc)
    freqs = np.array(freqs) * 2 * np.pi  # convert to angular frequency

    # find index freq 0.2
    min_freq = 0.015
    max_freq = 0.2
    idx_freq_max = np.where(freqs > max_freq)[0][0]
    idx_freq_min = np.where(freqs < min_freq)[0][-1]
    print(
        f"Using frequencies from {freqs[idx_freq_min]} to {freqs[idx_freq_max]} rad/s"
    )

    print(f"points x_loc: {x_loc}")
    # freqs = freqs[idx_freq_min:idx_freq_max]
    ffts = ffts[:, idx_freq_min:idx_freq_max]

    # we approximate the value of -alpha_i(x_j) with max_k A'_k(x_j)/A_k(x_j) = max_k [(A_k(x_j+1) - A_k(x_j)) / A_k(x_j) ] / (x_j+1 - x_j)
    ratios = np.log(ffts[1:, :] / ffts[:-1, :])

    print(f"ffts.shape = {ffts.shape}")

    # freq_ratios = np.column_stack((freqs, ratios[1, :]))

    # np.set_printoptions(threshold=np.inf)
    # print(f"freq_ratios: {freq_ratios[:1000]}")

    # x_loc_diff = np.diff(x_loc)
    idxmax = np.argmax(ratios, axis=1)
    # freqs_max = freqs[idxmax]
    ratio_max = np.max(ratios, axis=1) / 20

    # alpha_i = -ratio_max / x_loc_diff

    # for i in range(1, len(ratio_max)):
    #     #     # we add a normalization factor to the ratio to proopperly cancellout the amplitudes when adding the logarithms
    #     print(f"i = {i}, ratio_max[i] = {ratio_max[i]}")
    #     print(f"         ffts[i+1, idxmax[i]] = {ffts[i + 1, idxmax[i]]}")
    #     print(f"         ffts[i, idxmax[i]] = {ffts[i, idxmax[i]]}")
    #     print(
    #         f"         log(ffts[i+1, idxmax[i]] / ffts[i, idxmax[i]]) = {np.log(ffts[i + 1, idxmax[i]] / ffts[i, idxmax[i]])}"
    #     )
    #     ratio_max[i] += np.log(ffts[i, idxmax[i]] / ffts[i, idxmax[i - 1]])

    # Weighted average ratio instead of max
    # weights = ffts[:-1, :]
    # ratio_max = np.sum(weights * ratios, axis=1) / np.sum(weights, axis=1)

    # Smooth the growth rate

    # ell = 4
    # print(f"Using x_loc[{ell}] = {x_loc[ell]}")
    # print(f"Using y_loc[{ell}] = {y_loc[ell]}")

    # rel_ratio = ratios[ell, :] / ratio_max[ell]
    # fig, ax2 = plt.subplots(figsize=(8, 5))

    # myfreq = [0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02]
    # for i in myfreq:
    #     idx_freq = np.where(np.abs(freqs - i) < 1e-3)[0][0]

    #     ax2.plot(x_loc, ffts[:, idx_freq], label=f"FFT at freq = {i:.3f} rad/s")
    # # ax2.plot(freqs, rel_ratio, label="Relative ratio of max freq")

    # # rel_ratio_smooth = gaussian_filter1d(rel_ratio, sigma=20)

    # # ax2.plot(freqs, rel_ratio_smooth, label="Smoothed relative ratio", linestyle="--")

    # plt.legend()
    # plt.grid()
    # plt.show()

    # # we approximate the value of -alpha_i(x_j)

    # data_max = np.column_stack((x_loc[:-1],freqs_max, ratio_max))
    # print("Max frequencies and ratios:")
    # print(data_max)

    # nfactor = [0]
    # for i in range(1, len(x_loc)):
    #     nx = np.trapezoid(-alpha_i[:i], x_loc[:i])
    #     nfactor.append(nx)

    nfactor = np.concatenate(([0], np.cumsum(ratio_max)))

    ax.plot(x_loc, nfactor, label="n(x) from fft wgn")


def nfactor_sinus(
    points_loc: np.ndarray,
    time: np.ndarray,
    variables: np.ndarray,
    ax,
    use_u: bool,
    heightBL: float,
    XafterGap: float,
    width: float,
) -> None:
    pass
    # data = variables[:, :, 0] if use_u else variables[:, :, 1]
    # amplitude_envelope = []
    # tmax_data = 4500
    # idx1 = np.where(time[0] < tmax_data)[0][0]
    # time = time[:, idx1:]
    # data = data[:, idx1:]
    # points_loc_choosen = []
    # for p, point in enumerate(points_loc):
    #     if point[1] != heightBL or point[0] < XafterGap + width:
    #         continue
    #     data_p = data[p, :]
    #     asignal = hilbert(data_p)
    #     aenvelope = np.abs(asignal)
    #     amplitude_envelope.append(aenvelope)
    #     points_loc_choosen.append(point)

    # points_loc_choosen = np.array(points_loc_choosen)
    # amplitude_envelope = np.array(amplitude_envelope)
    # omega_0 = 0.13
    # omega_1 = 0.01
    # Tmax = 8200
    # freqs = omega_0 + 2*(omega_1 - omega_0) * time[0] / Tmax

    # print(f"freqs.shape = {freqs.shape}")
    # print(f"amplitude_envelope.shape = {amplitude_envelope.shape}")

    # amplitude_envelope_quotients = amplitude_envelope[:, 1:] / amplitude_envelope[:, :-1]
    # amplitude_envelope_quotients = np.max(amplitude_envelope_quotients, axis=1)

    # print(f"amplitude_envelope_quotients.shape = {amplitude_envelope_quotients.shape}")

    # plt.plot(points_loc_choosen, amplitude_envelope_quotients)
    # plt.show()


# def triangulate(depths: np.ndarray, widths: np.ndarray) -> np.ndarray:
#     points = np.column_stack((widths, depths))
#     tri = Delaunay(points)

#     return tri.simplices


def copy2dat(
    depths: np.ndarray, widths: np.ndarray, nfactor: np.ndarray, pathDat: str
) -> None:
    """
    Updates the TikZ plot inside the .tex file by replacing the coordinates
    of the nFactor points with the new data.
    """
    sizeGrid = 100
    X = np.linspace(np.min(widths), np.max(widths), sizeGrid)
    Y = np.linspace(np.min(depths), np.max(depths), sizeGrid)
    X_grid, Y_grid = np.meshgrid(X, Y)

    max_depth_full_stability = 1.375
    width_instability_max_depth_full_stability = 62

    borders = np.concatenate(
        [
            plotStabilityCurve_wVSd.unstable_line1,
            plotStabilityCurve_wVSd.hopf,
            np.array(
                [
                    [
                        max_depth_full_stability,
                        width_instability_max_depth_full_stability,
                    ],
                ]
            ),
        ]
    )

    borders_d = borders[:, 0]
    borders_w = borders[:, 1]

 
    # Interpolate/extrapolate over the grid
    points = np.column_stack((widths, depths))
    Nnan = -1
    Z_grid = griddata(
        points, nfactor, (X_grid, Y_grid), method="cubic", fill_value=np.nan
    )

    # Step 2: Fill NaNs using nearest neighbor extrapolation
    nearest = NearestNDInterpolator(points, nfactor)
    Z_grid = np.where(np.isnan(Z_grid), nearest(X_grid, Y_grid), Z_grid)

    Z_grid = gaussian_filter(Z_grid, sigma=0.7)

    # Write to .dat file
    with open(pathDat, "w") as f:
        for i in range(len(Y)):
            if i == 0:
                # Write the border points
                f.write(f"{0:.6f} {0:.6f} {0:.6f}\n")
                for j in range(len(X)):
                    f.write(f"{X[j]:.6f} {0:.6f} {0:.6f}\n")
                f.write("\n")  # Newline to separate rows

            for j in range(len(X)):
                if j == 0:
                    # Write the border points
                    f.write(f"{0:.6f} {Y[i]:.6f} {0:.6f}\n")
                x = X[j]
                y = Y[i]
                z = Z_grid[i, j]
                # if np.isnan(z):
                #     continue  # Skip undefined regions
                f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
            f.write("\n")  # Newline to separate rows

    print(f"Data written to {pathDat}.")

def method_variance_threshold(time, signal, window_size=100, threshold_factor=3.0):
        """
        Método 1: Detección basada en varianza móvil
        
        Parameters:
        -----------
        window_size : int
            Tamaño de la ventana móvil
        threshold_factor : float
            Factor multiplicativo del umbral de varianza
        
        Returns:
        --------
        filtered_time : np.ndarray
        filtered_signal : np.ndarray
        """
        # Calcular varianza móvil
        variance = np.array([np.var(signal[max(0, i-window_size):i+1]) 
                           for i in range(len(signal))])
        
        # Varianza base (primeros puntos, asumiendo régimen estacionario)
        base_variance = np.mean(variance[:window_size])
        threshold = base_variance * threshold_factor
        
        # Encontrar primer punto donde se supera el umbral
        oscillation_start = np.where(variance > threshold)[0]
        
        if len(oscillation_start) > 0:
            idx_start = oscillation_start[0]
            t_0 = time[idx_start]
        else:
            t_0 = time[0]
        
        mask = time >= t_0
        filtered_time = time[mask]
        filtered_signal = signal[mask]
        return filtered_time, filtered_signal

def getCurrentData(pathCurrentData: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Get the current data from the specified path.
    Args:
        pathCurrentData: Path to the current data file.
    Returns:
        Tuple of width, depth, and nFactors arrays.
    """
    if not os.path.exists(pathCurrentData):
        print(f"Path {pathCurrentData} does not exist. No current to skip.")
         # FileNotFoundError(f"Path {pathCurrentData} does not exist.")
        return np.array([]), np.array([]), np.array([])

    data = np.loadtxt(pathCurrentData, delimiter=" ")
    d, w, nFactors = data[:, 0], data[:, 1], data[:, 2]

    return d, w, nFactors

def plot_nFactor(
    folders: list[str],
    file_name: str = "HistoryPoints.his",
    use_DELTA_N: bool = False,
    pathTex: str = "",
    pathCurrentData: str = "",
    save: str = "",
) -> None:
    """
    Plot nFactor curve from values from HistoryPoints.his files in different folders.

    Args:
        folders: List of folder paths to compare.
        file_name: Name of the file to read in each folder (default: "HistoryPoints.his").
        save: Path to save the plot (default: "").
    """
    heightBL = 1
    XafterGap = -100
    use_u = True  # otherwise use v
    # use_DELTA_N = False # if True, use DELTA_N wiwth reference point the first folder
    count = 0
    x_ref = np.array([])
    n_x_ref = np.array([])
    # d_w = []
    time0 = 1200
    time1 = 4500
    n_x_amplification = []


    if use_DELTA_N:
        d, w, nFactors = getCurrentData(
            pathCurrentData
        )
        d_w_current = np.column_stack((d, w, nFactors))

        folders_full = folders.copy()

        for f in folders_full:
            # exctract width and depth from folder name
            width, depth = extract_width_depth(f)

            # check if the pair (depth, width) is already in d_w
            if np.any((d_w_current[:, 0] == depth) & (d_w_current[:, 1] == width)):
                print(
                    f"Pair (depth={depth}, width={width}) already exists in current data. Skipping loading the data for folder {f}."
                )
                # remove f from folders
                folders.remove(f)
                
                idx = np.where((d_w_current[:, 0] == depth) & (d_w_current[:, 1] == width))[0][0]
                n_x_amplification.append([depth, width, d_w_current[idx, 2]])

                continue


    data_by_folder, variables = read_all_folders(folders, file_name, slice(None))

    # check if data comes from NL runs (in this case we need to read the data from the last dt of the baseflow and substract it from the data)
    # check if "nonLinear" is in the file_name
    for folder in folders:
        if "nonLinear" in folder:
            print("Data comes from NL runs. Reading the last dt of the baseflow and substracting it from the data.")
            # substitute path/to/folder/*nonLinear*/codename with path/to/folder/baseflow/dns/codename
            base_path = re.sub(r'/[^/]*nonLinear[^/]*/', '/baseflow/dns/', folder)

            print("New baseflow path:", base_path)
            baseflow_data, _ = read_all_folders([base_path], file_name, slice(None))

            points_nlpert , variables_nlpert = data_by_folder[folder][0], data_by_folder[folder][2]

            points_baseflow, variables_baseflow = baseflow_data[base_path][0], baseflow_data[base_path][2]

            #check if points_nlpert and points_baseflow are the same
            if not np.array_equal(points_nlpert, points_baseflow):
                raise ValueError(
                    f"Points in NL perturbed data and baseflow data are not the same for folder {folder}."
                )

            # substract the baseflow data from the perturbed data
            # last timestep baseflow data
            steadystate= variables_baseflow[:, -1, :]

            variables_nlpert -= steadystate[:, np.newaxis, :]
            data_by_folder[folder] = (points_nlpert, data_by_folder[folder][1], variables_nlpert)

            




    fig, ax = plt.subplots(figsize=(8, 5))

    for folder, (points_loc, time, variables) in data_by_folder.items():
        # we try to do automatic detection of either wave packet (from Transient growth runs) or sinusoidal signal (from blowing-suction runs)
        width, depth = extract_width_depth(folder)
        codename = "d" + str(depth) + "_w" + str(width)
        # d_w.append([d_w, width])
        X = []
        n_x = []
        baseAmplitude = 9000
        print(f"Folder: {folder}")
        x_loc_ref = -80
        p_ref = np.where(points_loc[:, 0] >= x_loc_ref)[0][0]
        print(f"    Reference point index: {p_ref}")
        print(
            f"    First point ({p_ref}): x = {points_loc[p_ref, 0]}, y = {points_loc[p_ref, 1]}"
        )

        # idx1 = np.where(time[p_ref] < time0)[0][-1]
        # time_ref = time[p_ref, idx1:]
        # data = variables[p_ref, idx1:, 0] if use_u else variables[p_ref, idx1:, 1]
        # # is_wave_packet = is_wave_packet_signal(data)
        # # is_wgn = is_gaussian_noise(data)

        # idx2 = np.where(time_ref > time1)[0][0]
        # time_ref = time_ref[:idx2]
        # data = data[:idx2]

        time_ref = time[p_ref, len(time[p_ref]) // 3 : len(time[p_ref]) * 2 // 3]
        data = variables[p_ref, len(time[p_ref]) // 3 : len(time[p_ref]) * 2 // 3, 0] if use_u else variables[p_ref, len(time[p_ref]) // 3 : len(time[p_ref]) * 2 // 3, 1]

        signal = classify_signal(time_ref, data)
        if signal == signal_types["wave_packet"]:
            print(
                "    Detected wave packet signal. Computing amplitude using interpolated maxima."
            )
        elif signal == signal_types["gaussian_noise"]:
            print(
                "    Detected white Gaussian noise signal. Computing amplitude using noise statistics."
            )
        else:
            print(
                "    Detected sinusoidal signal. Computing amplitude using stabilized maxima."
            )

        for p, point in enumerate(points_loc):
            if point[1] != heightBL or point[0] < XafterGap:
                continue
            t = time[p]
            # idx1 = np.where(t < time0)[0][-1]
            # t = t[idx1:]
            # var = variables[p, idx1:, :]

            # tmax = 4500
            # idx2 = np.where(t > tmax)[0][0]
            # t = t[:idx2]
            # var = variables[p, :idx2, :]
            var = variables[p, :, :]

            

            print(
                f"    Point {p}: x = {points_loc[p, 0]:.2f}, y = {points_loc[p, 1]:.2f}, z = {points_loc[p, 2]:.2f}"
            )
            # if p % 100 == 0:
            print(f"    shape of variables: {var.shape}")
            if p == 3:
                print(var[:, 0])
            
            tfilt1, ufilt = method_variance_threshold(t, var[:, 0])

            tfilt2, vfilt = method_variance_threshold(t, var[:, 1])

            tfilt = np.array([])
            if len(tfilt1) < len(tfilt2):
                tfilt = tfilt1
                vfilt = vfilt[len(tfilt2) - len(tfilt1):]
            else:
                tfilt = tfilt2
                ufilt = ufilt[len(tfilt1) - len(tfilt2):]

            # ufilt = var[:, 0]
            # vfilt = var[:, 1]
            # tfilt = t
            # A = get_amplitude(t, var[:, 0], var[:, 1], use_u, signal)
            A = get_amplitude(tfilt, ufilt, vfilt, use_u, signal)

            X.append(point[0])
            n_x.append(A)

        X = np.array(X)
        n_x = np.array(n_x)
        print(f"    X: {X}")
        print(f"    n_x: {n_x}")
        x_min, baseAmplitude = getBaseAmplitude(X, n_x)

        print(f"    Base amplitude: {baseAmplitude} at x = {x_min}")

        X_old = X.copy()
        X = X[X_old > x_min]
        n_x = n_x[X_old > x_min]


        # mask = X > 1
        # multiplier = np.ones_like(n_x)
        # # if depth != 0:
        # #     multiplier[mask] = 0.5
        # n_x = n_x / multiplier
        print("Amplitude at y = 1:", n_x)

        n_x = np.log(n_x / baseAmplitude)
        # use log plot
        # ymax = max(ymax, np.max(n_x))

        if use_DELTA_N and count == 0: # flat plate case, e.g. reference value to compute DeltaN = N - Nref
            count += 1
            x_ref = X
            n_x_ref = n_x
            continue

        if use_DELTA_N:
            # interpolate n_x_ref to the current X
            n_x_ref_interp = np.interp(X, x_ref, n_x_ref)
            n_x = n_x - n_x_ref_interp

            lenghtaveraging = 100
            x0 = width + 60
            x1 = width + lenghtaveraging


            idx0 = np.where(X < x0)[0][-1]
            idx1 = np.where(X > x1)[0][0]

            n_x = np.mean(n_x[idx0:idx1])
            n_x_amplification.append([depth, width, float(n_x)])
            
            # append to file pathCurrentData
            with open(pathCurrentData, "a") as f:
                f.write(f"{depth} {width} {n_x}\n")


        if not use_DELTA_N:
            # save data to file
            with open(f"data/n_x_{codename}.dat", "w") as f:
                for x, n in zip(X, n_x):
                    f.write(f"{x} {n}\n")
            ax.plot(X, n_x, label=codename)
            # ax.semilogy(X, n_x, label=codename)
            # plt.legend()
            # plt.show()

        # if signal == signal_types['gaussian_noise']:
        #     nfactor_wgn(
        #         points_loc, time, variables, ax, use_u, heightBL, XafterGap, width
        #     )

        if signal == signal_types["sinusoidal"]:
            nfactor_sinus(
                points_loc, time, variables, ax, use_u, heightBL, XafterGap, width
            )

    if use_DELTA_N:
        print(f"n_x_amplification: {n_x_amplification}")
        n_x_amplification = np.array(n_x_amplification)
        # heat map with points at n_x_amplification[:, 0] and n_x_amplification[:, 1] and color = n_x_amplification[:, 2]
        # create colormap from 0 (white) to N = 9  (dark blue)
        depths = n_x_amplification[:, 0]
        widths = n_x_amplification[:, 1]
        DeltaN = n_x_amplification[:, 2]

        # intepolation to get smooth countour
        N = 100
        xi = np.linspace(np.min(widths), np.max(widths), N)
        yi = np.linspace(np.min(depths), np.max(depths), N)
        X_grid, Y_grid = np.meshgrid(xi, yi)

        points = np.array(list(zip(widths, depths)))

        # Interpolate DeltaN values on the grid
        DeltaN_grid = griddata(points, DeltaN, (X_grid, Y_grid), method="cubic")

        # Parameters
        nfactor_max = int(np.ceil(np.max(DeltaN)))
        vmin = -0.5
        vmax = nfactor_max + 0.5
        contour_levels = np.arange(0, nfactor_max+1, 1)

        # Define the bounds and normalization
        bounds = np.linspace(vmin, vmax, int(np.ceil(vmax + 1)))
        number_of_colors = len(bounds) - 1
        norm = mcolors.BoundaryNorm(boundaries=bounds, ncolors=number_of_colors)

        # Get the discrete colormap
        cmap = plt.get_cmap("Blues", number_of_colors)

        # Create a contour plot
        co = ax.contourf(
            X_grid, Y_grid, DeltaN_grid, levels=contour_levels, cmap=cmap, alpha=0.7
        )
        # Your scatter plot
        sc = ax.scatter(
            widths,
            depths,
            c=DeltaN,
            cmap=cmap,
            norm=norm,
            s=50,
            edgecolor="black",
            linewidth=0.5,
            label="n_x amplification",
        )

        # Add colorbar with ticks at the bin centers
        cbar = plt.colorbar(
            sc, ax=ax, boundaries=bounds, ticks=bounds, label="n_x amplification"
        )
        cbar.ax.set_yticklabels([f"{b:.1f}" for b in bounds])
        copy2dat(depths, widths, DeltaN, pathTex)

    if use_DELTA_N:
        ax.set_xlabel("w/delta*")
        ax.set_ylabel("d/delta*")
        ax.set_title("Delta N")
    else:
        ax.set_xlabel("x / delta*")
        ax.set_ylabel("n(x)")
        ax.set_title("n(x) curve")
        ax.legend()
    # ax.set_ylim(0, ymax * 1.1)
    ax.grid()
    if save == "":
        plt.show()
    else:
        plt.savefig(save)


if __name__ == "__main__":
    file_name = "HistoryPoints.his"

    pathScript = os.path.dirname(os.path.abspath(__file__))
    pathTex = "../latex/Images/data/DeltaN.dat"
    pathCurrentData = "data/DeltaN.dat"
    pathTex = os.path.join(pathScript, pathTex)
    pathCurrentData = os.path.join(pathScript, pathCurrentData)

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
        "--use_DELTA_N",
        action="store_true",
        help="Use DELTA_N with reference point the first folder.",
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
        use_DELTA_N=args.use_DELTA_N,
        pathTex=pathTex,
        pathCurrentData=pathCurrentData,
        save=args.save,
    )
