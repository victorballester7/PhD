import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.axes import Axes
from pp.codenamesNfactor import code_names
from pp.fileManagement import extract_width_depth, readAvgDataPoints
from pp.filterData import getRMS

def addNxplot(dataFile: str, ax: Axes, doLoo: bool):
    """Main function to read data and plot points."""

    w, d = extract_width_depth(dataFile)
    print(f"Processing w = {w}, d = {d}")

    xvals, yvals, data = readAvgDataPoints(dataFile)

    rms = getRMS(data)

    if doLoo:
        Loo = np.max(np.abs(rms), axis=1)
        A = Loo
    else:
        # integrate from 0 to ymax
        ymax = 150
        yindx = np.argmin(np.abs(yvals - ymax))

        L2 = np.sqrt(np.trapezoid(rms[:, :yindx] ** 2, yvals[:yindx]))

        A = L2

    A0_arg = np.argmin(A)
    A0 = A[A0_arg]
    A = A[A0_arg:]
    xvals = xvals[A0_arg:]

    Nx = np.log(A / A0)
    ax.plot(xvals, Nx, markersize=2, label="w = {:.2f}, d = {:.2f}".format(w, d))


def main():
    """
    Read the data files that contain the time averaged reynolds stresses for several x and y locations, computes the amplitude in the y direction (L2 or Loo) and then computes the N factor as Nx = log(A/A0) where A0 is the amplitude at the first x location.
    Plots the N factor for several cases (gap configurations) in the same plot as well as the flat plate case for comparison.
    """

    # Parameters to change
    n = 600  # number of points in the wall normal direction
    doLoo = False  # if False, L2 norm is computed

    # script path
    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))

    basePath = "../../../src/incNSboeingGapRe1000/directLinearSolver/blowingSuctionWGNinsideDomain/"
    basePath = os.path.join(pathCurrentScript, basePath)

    fig, ax = plt.subplots(figsize=(8, 6))

    code_names2 = [
        "d0.5_w10",
        "d0.5_w101",
        "d0.5_w102",
    ]
    for dw in code_names2:
        dataFile_dw = os.path.join(basePath, dw, "data", f"pointsavg_all_n{n}.dat")
        addNxplot(dataFile_dw, ax, doLoo)

    # flat plate case
    dataFile_flat = f"../../../src/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgnInsideDomainDivFree/data/pointsavg_all_n{n}.dat"
    dataFile_flat = os.path.join(pathCurrentScript, dataFile_flat)
    addNxplot(dataFile_flat, ax, doLoo)

    ax.set_title(f"N factor using {'Loo' if doLoo else 'L2'} norm")
    ax.legend()
    ax.grid()

    plt.show()


if __name__ == "__main__":
    main()
