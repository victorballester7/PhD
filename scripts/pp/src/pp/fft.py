import numpy as np
from scipy.fft import rfft, rfftfreq, irfft

def fftFreqs(
    time: np.ndarray, signal: np.ndarray, variable_label: str
) -> np.ndarray:
    """
    Perform FFT on the given signal and print frequencies with amplitudes above a threshold.
        Args:
            time (np.ndarray): Array of time values.
            signal (np.ndarray): Signal data to perform FFT on.
            variable_label (str): Label for the variable being analyzed (e.g., 'u', 'v').
        Returns:
            np.ndarray: Reconstructed signal from the highest frequencies.
    """
    # use fft to get the frequency
    fft_data = rfft(signal)

    freq = rfftfreq(len(signal), d=(time[1] - time[0]))
    omega = 2 * np.pi * freq

    eps = 0.1
    threshold = eps * np.max(
        np.abs(fft_data[1:])
    )  # we skip the mean value (fft_data[0])
    # fft_data[np.abs(fft_data) < threshold] = 0

    idx_to_print = []

    print(f"Frequencies greater than the {eps*100}% of the highest amplitude (excluding mean mode, thus {threshold:.8f}) for variable {variable_label}")
    for i in range(len(fft_data)):
        if np.abs(fft_data[i]) > threshold:
            idx_to_print.append([i, np.abs(fft_data[i])])
    idx_to_print = np.array(idx_to_print)
    
    if len(idx_to_print) == 0:
        print("No frequencies found above the threshold.")
        return

    # sort by amplitude
    idx_to_print = idx_to_print[np.argsort(np.abs(idx_to_print[:, 1]))][::-1]

    for i, A in idx_to_print:
        print(
            f"ω (2 π f): {omega[int(i)]:.8f}, Amplitude: {A:.8f}"
        )

    # reconstruct the signal from the highest frequencies
    signal_reconstructed = irfft(fft_data, n=len(signal))

    return signal_reconstructed


