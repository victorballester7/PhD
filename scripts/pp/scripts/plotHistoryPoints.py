import matplotlib.pyplot as plt
import numpy as np
from pp.fft import fftFreqs
from pp.filterData import timeFilter
from pp.inputargs import parseArgs
from pp.colors import colors
from pp.fileManagement import extract_width_depth, readDataHistoryPointsMultiple


def createFigure(dynamicalSystem: bool):
    """
    Create a figure for plotting history points.

    Args:
        dynamicalSystem (bool): Flag to indicate if the plot is for a dynamical system.

    Returns:
        tuple: Figure and axes objects.
    """

    if dynamicalSystem:
        fig, axes = plt.subplots(1, 1, figsize=(8, 6))
        axes = np.array([axes])  # Ensure axes is iterable
        axes[0].set_xlabel("u")
        axes[0].set_ylabel("v")
        # axes[0].set_aspect('equal', adjustable='box')
    else:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True)
        labels = ["u", "v", "w"]
        for i in range(3):
            axes[i].set_xlabel("t")
            axes[i].set_ylabel(labels[i])

    for ax in axes:
        ax.grid(True)


    return fig, axes



def main():
    """
    Main function to plot history points from one or multiple folders as a function of time or in phase space (u vs v). The points are stored in the historyPoints.dat file in each folder.
    """
    args = parseArgs()

    folders = args.folders


    data = readDataHistoryPointsMultiple(folders)

    fig, axes = createFigure(args.dynamicalSystem)

    for f in folders:
        points, time, fields = data[f]
        time, fields = timeFilter(time, fields, args.time_min, args.time_max)
        
        depth, width = extract_width_depth(f)

        print(f"Processing folder: {f}")
        for i, p in enumerate(points):
            print(f"Point {i}: x = {p[0]}, y = {p[1]}")

        for i, p in enumerate(args.points):
            label = f"d{depth}_w{width}_x{points[p, 0]}_y{points[p, 1]}"
            for j, ax in enumerate(axes):
                if args.dynamicalSystem:
                    ax.plot(fields[p, :, 0], fields[p, :, 1], label=f"u vs v (x = {points[p, 0]}, y = {points[p, 1]})")
                    ax.set_xlabel("u")
                    ax.set_ylabel("v")
                else:
                    ax.plot(time, fields[p, :, j], label=label)
                    ax.set_xlabel("t")
                    ax.set_ylabel("u" if j == 0 else "v" if j == 1 else "p")

                if args.fft and j < 2: # only for u and v
                    signal_reconstructed = fftFreqs(time, fields[p, :, j], "u" if j == 0 else "v")
                    ax.plot(time, signal_reconstructed, linestyle="--", label=f"IFT∘FT {label}")

    plt.legend()
    plt.show()



if __name__ == "__main__":
    main()
