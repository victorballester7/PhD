import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import os
from pp.fileManagement import readAvgDataPoints
from pp.filterData import getRMS

def addDataToPlot(dataFile: str, ax: Axes):
    xvals, yvals, data = readAvgDataPoints(dataFile)

    rms = getRMS(data)

    # Plot the points
    for i in range(len(xvals)):
        ax.plot(rms[i], yvals, "-", markersize=2, label=f"x = {xvals[i]}")


def main():
    """Main function to read data and plot points."""
    # script path
    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))

    basePath = (
        "../../../src/incNSboeingGapRe1000/directLinearSolver/blowingSuctionWGNinsideDomain/"
    )
    basePath = os.path.join(pathCurrentScript, basePath)

    code_names = [
        "d0.5_w10",
    ]
    n = 600

    fig, ax = plt.subplots(figsize=(8, 6))

    for dw in code_names:
        dataFile_dw = os.path.join(basePath, dw, "data", f"pointsavg_all_n{n}.dat")
        addDataToPlot(dataFile_dw, ax)

    # Set labels and title
    ax.set_xlabel("x")
    ax.set_ylabel("sqrt(u^2 + v^2)")

    # Add grid and legend
    ax.grid()
    ax.legend()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
