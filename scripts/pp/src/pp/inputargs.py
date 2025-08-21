import argparse
import numpy as np


def parseArgs() -> argparse.Namespace:
    """
    Parse command line arguments for multiple python scripts in a folder.
    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Parse arguments for multiple python scripts in a folder."
    )

    parser.add_argument(
        "folders", 
        nargs="+", 
        help="List of folders to compare."
    )

    parser.add_argument(
        "--use_DELTA_N",
        action="store_true",
        help="Use DELTA_N with reference point the first folder.",
    )

    parser.add_argument(
        "--time_min",
        default=0.0,
        type=float,
        help="Minimum time value to include in the comparison (default: None).",
    )
    parser.add_argument(
        "--time_max",
        default=np.inf,
        type=float,
        help="Maximum time value to include in the comparison (default: None).",
    )

    parser.add_argument(
        "--fft",
        action="store_true",
        help="Use FFT to get frequency data (default: False).",
    )

    parser.add_argument(
        "--dynamicalSystem",
        action="store_true",
        help="Plot the u vs v phase space for dynamical systems (default: False).",
    )

    parser.add_argument(
        "--points",
        metavar="int",
        nargs="+",
        type=int,
        default=[0],
        help="Point number to compare (default: [0]).",
    )

    return parser.parse_args()
