import numpy as np
import matplotlib.pyplot as plt
import os
import re
from matplotlib.axes import Axes

def read_points_from_file(filename):
    """Reads points from a file and returns them as a numpy array."""
    return np.loadtxt(filename, skiprows=3)

# def addDataToPlot(ax, points: np.ndarray):
#      # Extract x and y coordinates
#     x, y, u, v, p = points[:, 0], points[:, 1], points[:, 2], points[:, 3], points[:, 4]

#     # check if the data in x is all the same
#     var = np.array([])
#     if np.all(x == x[0]):
#         var = y
#     else:
#         var = x

#     # Create a figure and axis

#     # Plot the points
#     ax.plot(u, var, '--', markersize=2, label='u', alpha=0.4)
#     ax.plot(v, var, ':', markersize=2, label='v', alpha=0.4)
#     abs_sqrt = np.sqrt(u**2 + v**2)
#     ax.plot(abs_sqrt, var, '-', markersize=2, label='sqrt(u^2 + v^2)')

#     # Set labels and title
#     ax.set_xlabel('x')
#     ax.set_ylabel('v')

def plotSections(dataFile: np.ndarray, line: bool, ax: Axes):
    """Main function to read data and plot points."""
    # fig, ax = plt.subplots(figsize=(8, 6))
    
    rms = []

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
            data_tmp.append(tmp) # we only store u and v
        data.append(data_tmp)

    data = np.array(data)

    # u is in column 2, v is in column 3
    # rms = np.sqrt(np.mean(data[:, :, :, 2] ** 2 + data[:, :, :, 3] ** 2, axis=0))

    rms = np.sqrt(np.abs(data[:, :, :, -1]))[0]
    rmsaux = np.sqrt(np.abs(data[:, :, :, -4] + data[:, :, :, -2]))[0]
    # rms = np.mean(data[:, :, :, 0], axis=0)

    # normalize each rms by the maximum value in each column
    # for i in range(rms.shape[0]):
    #     y = 0.3
    #     yindx = np.argmin(np.abs(yvals - y))
    #     max = np.max(rms[i, yindx:])
    #     rms[i, :] = rms[i, :] / max 

    
    # get index where var[i] is closes to 100
    # ymaxAsymptote = 80
    # yminAsymptote = 40
    # yindx_max = np.argmin(np.abs(var - ymaxAsymptote))
    # yindx_min = np.argmin(np.abs(var - yminAsymptote))

    # print(f"yindx_max: {yindx_max}, yindx_min: {yindx_min}")
    # fig, ax = plt.subplots(figsize=(8, 6))

    diff = np.abs(rms - rmsaux)
    Loo = np.max(diff, axis=1)/np.max(rmsaux, axis=1)

    for i in range(len(xvals)):
        print(f"x = {xvals[i]}, Loo = {Loo[i]}")
        ax.plot(rms[i], yvals, "-", markersize=2, label=f"x = {xvals[i]} {line}", linestyle='--' if line else '-')
        ax.plot(rmsaux[i], yvals, "-", markersize=2, label=f"x = {xvals[i]} {line}", linestyle='--')

    # # Add grid and legend
    # ax.grid()
    # ax.legend()




    # L2s = []
    # # yMaxIntegration = 20
    # # yindx20 = np.argmin(np.abs(var - yMaxIntegration))
    # afterGap = 100

    # for i in range(len(labels)):
    #     rms_i = rms[i]
    #     # grads/= rms_i
    #     # find first index where grads is less than tol
    #     tol = 25.e-7
    #     if labels[i] >= afterGap:
    #         ymaxAsymptote = 80
    #         yminAsymptote = 40
    #         yindx_max = np.argmin(np.abs(var - ymaxAsymptote))
    #         yindx_min = np.argmin(np.abs(var - yminAsymptote))
    #         yMaxIntegration = 50
    #         yMaxIntegration = np.argmin(np.abs(var - yMaxIntegration))
    #         avg_verticalLine = np.mean(rms_i[yindx_min:yindx_max])
    #     elif labels[i] == -25:
    #         ymaxAvg = 10
    #         yminAvg = 4
    #         yindx_max = np.argmin(np.abs(var - ymaxAvg))
    #         yindx_min = np.argmin(np.abs(var - yminAvg))
    #         yMaxIntegration = 10
    #         yMaxIntegration = np.argmin(np.abs(var - yMaxIntegration))
    #         avg_verticalLine = np.mean(rms_i[yindx_min:yindx_max])
    #     else:
    #         grads = np.gradient(rms_i, var)
    #         newGrads = np.empty_like(grads)
    #         chunckSize = 20
    #         for j in range(len(grads)):
    #             if j < chunckSize:
    #                 newGrads[j] = np.mean(grads[:j+1])
    #             elif j >= len(grads) - chunckSize:
    #                 newGrads[j] = np.mean(grads[j:])
    #             else:
    #                 newGrads[j] = np.mean(grads[j-chunckSize//2:j+chunckSize//2])
    #         y = 6
    #         yindx_min = np.argmin(np.abs(var - y))
    #         y = 40
    #         yindx_max = np.argmin(np.abs(var - y))
    #         newGradscut = newGrads[yindx_min:yindx_max]
    #         # get first value to reach tol
    #         yMaxIntegration = np.argmax(np.abs(newGradscut) < tol) + yindx_min
    #         # print(np.abs(newGradscut - tol))
    #         # print(f"y[MaxIntegration]: {var[yMaxIntegration]}")
    #         avg_verticalLine = rms_i[yMaxIntegration]
    #         # ax.plot(newGrads, var, ':', markersize=2, label=f'x = {labels[i]}')



    #     L2 = (rms_i - avg_verticalLine)**2
    #     ax.plot((rms_i - avg_verticalLine)[:yMaxIntegration], var[:yMaxIntegration], '-', markersize=2, label=f'x = {labels[i]}')
    #     
    #     # compute the integral of the rms - avg_verticalLine from 0 to yindx_min
    #     L2 = np.trapezoid(L2[:yMaxIntegration], var[:yMaxIntegration])
    #     L2s.append(np.sqrt(L2))
    # ax.grid()
    # ax.legend()

    # fig, ax = plt.subplots(figsize=(8, 6))

    # print(L2s)
    # nx = np.log(L2s/L2s[0])

    # ax.plot(labels, nx, markersize=2)


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


def getDataFileList(basePath: str, n: int, extension:str) -> np.ndarray:
    """Get all the data files of the form points{chk}_all_n{n}.dat inside basePath."""
    chkfiles = get_chkfiles_numbers(basePath, n)
    dataFile = [f"points{chk}_all_n{n}{extension}.dat" for chk in chkfiles]
    dataFile = [os.path.join(basePath, f) for f in dataFile]
    return np.array(dataFile)

def main():
    # script path
    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))

    n = 800
    extension = ""

    _, ax = plt.subplots(figsize=(8, 6))

    # basePath = "../src/incNSboeingGapRe1000/nonLinearPerturbations/d3_w15/data/"
    # basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/d4_w15/wgnInsideDomain/data/"
    basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/d4_w15/wgnInsideDomainSameMagnitudeNektarAveraged/data/"
    # basePath = "../src/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn/data/"
    # basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/oldSetups/bs_withOmegaFromOrrSommerfeld/d4_w15/expBC_omega0.0465/data/"
    basePath = os.path.join(pathCurrentScript, basePath)
    # dataFile = getDataFileList(basePath, n, extension)
    dataFile = [os.path.join(basePath, "pointsavg_all_n600.dat")]
    dataFile = np.array(dataFile)

    plotSections(dataFile,False, ax)
    # basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/d4_w15/wgnInsideDomainNektarAveraged/data/"
    # # basePath = "../src/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn/data/"
    # # basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/oldSetups/bs_withOmegaFromOrrSommerfeld/d4_w15/expBC_omega0.0465/data/"
    # basePath = os.path.join(pathCurrentScript, basePath)
    # # dataFile = getDataFileList(basePath, n, extension)
    # dataFile = [os.path.join(basePath, "pointsavg_all_n600.dat")]
    # dataFile = np.array(dataFile)

    # plotSections(dataFile, True, ax)
    ax.grid()
    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()
