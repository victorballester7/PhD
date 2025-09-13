import numpy as np
from typing import Tuple


def timeFilter(
    time: np.ndarray, fields: np.ndarray, time_min: float, time_max: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Filters the time and fields arrays based on the specified time range.

    Args:
        time (np.ndarray): Array of time values.
    fields (np.ndarray): Array of field values (e.g., u, v, p) at every point (axis 0) and timestep (axis 1).
        time_min (float): Minimum time value to include in the comparison.
        time_max (float): Maximum time value to include in the comparison.
    Returns:
        tuple[np.ndarray, np.ndarray]: Filtered time and fields arrays.
    """

    # Ensure time is a 1D array
    if time.ndim != 1:
        raise ValueError("Time array must be 1-dimensional.")

    # Create a boolean mask for the time range
    mask = (time >= time_min) & (time <= time_max)

    # Filter the time and fields arrays using the mask
    filtered_time = time[mask]
    filtered_fields = fields[:, mask, :]

    return filtered_time, filtered_fields

def getRMS(data: np.ndarray) -> np.ndarray:
    """
    Computes the RMS of the fields array along the time axis.
    """
    u = data[:, :, 2]
    v = data[:, :, 3]
    uu = data[:, :, 5]
    vv = data[:, :, 7]
    rms = np.sqrt(np.abs(u**2 + v**2 + uu + vv))
    return rms

