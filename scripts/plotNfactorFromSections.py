import numpy as np
import matplotlib.pyplot as plt
import os
import re
from matplotlib.axes import Axes


def read_points_from_file(filename):
    """Reads points from a file and returns them as a numpy array."""
    return np.loadtxt(filename, skiprows=3)


def addNxplot(dataFile: np.ndarray, ax: Axes):
    """Main function to read data and plot points."""

    points_tmp = []

    rms = []
    var = np.array([])

    data = []

    xvals = np.array([])
    yvals = np.array([])

    for dF in dataFile:
        data_dF = read_points_from_file(dF)
        data_tmp = []
        if len(xvals) == 0:
            xvals = np.unique(data_dF[:, 0])
        if len(yvals) == 0:
            yvals = np.unique(data_dF[:, 1])
            yvals.sort()
        for x in xvals:
            tmp = data_dF[data_dF[:, 0] == x]
            tmp = tmp[:, [2, 3]]
            data_tmp.append(tmp) # we only store u and v
        data.append(data_tmp)

    data = np.array(data)


    rms = np.sqrt(np.mean(data[:, :, :, 0] ** 2 + data[:, :, :, 1] ** 2, axis=0))

    # for i in range(len(xvals)):
    #     ax.plot(rms[i], yvals, "-", markersize=2, label=f"x = {xvals[i]}")


    # compute the maximum value of each TS mode
    
    # we skip the first points
    doLoo = True
    if doLoo:
        ymin = 0.2
        yindx = np.argmin(np.abs(yvals - ymin))
        Loo = np.max(np.abs(rms[:, yindx:]), axis=1)

        A = Loo
        
    else:
        ymax = 60
        yindx = np.argmin(np.abs(yvals - ymax))

        L2 = np.trapezoid(rms[:, :yindx] ** 2, yvals[:yindx]) 

        A = np.sqrt(L2)

    A = A[1:]  # skip the first point
    xvals = xvals[1:]
    Nx = np.log(A / A[0])
    ax.plot(xvals, Nx, markersize=2, label="Nx (Loo)" if doLoo else "Nx (L2)")

    doLoo = False
    if doLoo:
        ymin = 0.2
        yindx = np.argmin(np.abs(yvals - ymin))
        Loo = np.max(np.abs(rms[:, yindx:]), axis=1)

        A = Loo
        
    else:
        ymax = 150
        yindx = np.argmin(np.abs(yvals - ymax))

        L2 = np.trapezoid(rms[:, :yindx] ** 2, yvals[:yindx]) 

        A = np.sqrt(L2)

    A = A[1:]  # skip the first point
    Nx = np.log(A / A[0])
    ax.plot(xvals, Nx, markersize=2, label="Nx (Loo)" if doLoo else "Nx (L2)")

def get_chkfiles_numbers(basePath: str, n: int) -> np.ndarray:
    """Get all the chk numbers of the files of the form points{chk}_all_n{n}.dat inside basePath."""
    pattern = re.compile(rf"points(\d+)_all_n{n}\.dat")
    chkfiles = []
    for filename in os.listdir(basePath):
        match = pattern.match(filename)
        if match:
            chkfiles.append(int(match.group(1)))
    chkfiles.sort()
    return np.array(chkfiles)


def getDataFileList(basePath: str, n: int) -> np.ndarray:
    """Get all the data files of the form points{chk}_all_n{n}.dat inside basePath."""
    chkfiles = get_chkfiles_numbers(basePath, n)
    dataFile = [f"points{chk}_all_n{n}.dat" for chk in chkfiles]
    dataFile = [os.path.join(basePath, f) for f in dataFile]
    return np.array(dataFile)


def main():
    # script path
    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))

    code_names = np.array(
        [
            # "d4_w10",
            "d4_w15",
            # "d3.75_w10",
            # "d3.75_w15",
            # "d3.5_w10",
            # "d3.5_w15",
            # "d3.25_w10",
            # "d3.25_w15",
            # "d3_w10",
            # "d3_w15",
            # "d2.75_w10",
            # "d2.75_w15",
            # "d2.5_w10",
            # "d2.5_w15",
            # "d2.5_w20",
            # "d2.25_w10",
            # "d2.25_w16",
            # "d2.25_w20",
            # "d2.25_w25",
            # "d2.25_w31",
            # "d2_w10",
            # "d2_w16",
            # "d2_w20",
            # "d2_w24",
            # "d2_w28",
            # "d2_w32",
            # "d2_w36",
            # "d1.75_w10",
            # "d1.75_w15",
            # "d1.75_w20",
            # "d1.75_w25",
            # "d1.75_w30",
            # "d1.75_w35",
            # "d1.75_w40",
            # "d1.75_w45",
            # "d1.5_w10",
            # "d1.5_w15",
            # "d1.5_w20",
            # "d1.5_w25",
            # "d1.5_w30",
            # "d1.5_w35",
            # "d1.5_w40",
            # "d1.5_w45",
            # "d1.5_w50",
            # "d1.25_w10",
            # "d1.25_w15",
            # "d1.25_w20",
            # "d1.25_w25",
            # "d1.25_w30",
            # "d1.25_w35",
            # "d1.25_w40",
            # "d1.25_w45",
            # "d1.25_w50",
            # "d1.25_w60",
            # "d1.25_w70",
            # # "d1.25_w80",
            # "d1_w10",
            # "d1_w15",
            # "d1_w20",
            # "d1_w25",
            # "d1_w30",
            # "d1_w34",
            # "d1_w38",
            # "d1_w45",
            # "d1_w50",
            # "d1_w60",
            # "d1_w70",
            # "d0.75_w10",
            # "d0.75_w20",
            # "d0.75_w30",
            # "d0.75_w40",
            # "d0.75_w50",
            # "d0.75_w60",
            # "d0.75_w70",
            # "d0.5_w10",
            # "d0.5_w20",
            # "d0.5_w30",
            # "d0.5_w40",
            # "d0.5_w50",
            # "d0.5_w60",
            # "d0.5_w70",
        ]
    )

    basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/"
    basePath = os.path.join(pathCurrentScript, basePath)

    n = 800

    fig, ax = plt.subplots(figsize=(8, 6))

    for dw in code_names:
        basePath_dw = os.path.join(basePath, dw, "wgnInsideDomain/data")
        # get all the chk numbers of the files of the form points{chk}_all_n{n}.dat inside basePath_dw
        dataFile = getDataFileList(basePath_dw, n)

        addNxplot(dataFile, ax)

    n = 80
    # flat plate case
    basePath = (
        "../src/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn/data/"
    )
    basePath = os.path.join(pathCurrentScript, basePath)
    dataFile = getDataFileList(basePath, n)

    # addNxplot(dataFile, ax)

    # addNxplot(dataFile, ax)
    ax.legend()
    ax.grid()

    plt.show()


if __name__ == "__main__":
    main()
