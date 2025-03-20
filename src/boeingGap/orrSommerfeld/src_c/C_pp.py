import matplotlib.pyplot as plt
import readData as rd
import os
import numpy as np

if __name__ == "__main__":
    filenameEVs = "../data/EValues.dat"
    dir_script = os.path.dirname(os.path.realpath(__file__))
    filenameEVs = os.path.join(dir_script, filenameEVs)


    isTemporal = True
    beta = 0.0
    alpha = 0.2
    deltaStar = 1.7207876573

    isBL = True
    doPlot = True

    # for plotting
    xmin = 0.2
    xmax = 1.1
    ymin = -1.
    ymax = 0.1

    # xmin, xmax, ymin, ymax = pp.updateLimits(isTemporal, isBL, xmin, xmax, ymin, ymax)

    # xmin = 0
    # xmax = 1.1
    # ymin = -0.6
    # ymax = 0.1
    plotargs = [xmin, xmax, ymin, ymax]

    eigs = rd.readEValues(filenameEVs)

    alpha = alpha / deltaStar

    eigs = eigs / alpha   


    idx = np.argsort(-eigs.imag)
    EVaux = eigs[idx]

    threshold_realpart = 0.95
    EVaux = EVaux[abs(EVaux.real) < threshold_realpart]


    for i in range(10):
        print(f"EV {i}: {EVaux[i].real}    {EVaux[i].imag}i")
    print("...")

    plt.figure()
    plt.plot(eigs.real, eigs.imag, "o")

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.grid()

    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.show()


    # pp.postProc(eigs, xmin, xmax, ymin, ymax, "c", isTemporal, isBL)
