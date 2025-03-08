import numpy as np
import matplotlib.pyplot as plt
import time
import EVproblem as evp
import postprocessing as pp
import readData as rd


def runFixedAlpha(N, Re, alpha, D, D2, D4, y_cheb, U, U_yy, Doprint=True):
    start = time.time()
    L, M = evp.getOSMatrices(N, Re, alpha, D, D2, D4, U, U_yy)
    if Doprint:
        print("Time to construct matrices: ", time.time() - start)

    start = time.time()
    omega, c, vv =evp.solveEVproblem(L, M, alpha)
    if Doprint:
        print("Time to solve eigenvalue problem: ", time.time() - start)

    EVvariable = c
    max, vv = pp.getMostUnstableEV(EVvariable, vv)
    EVlabel = r"\omega" if EVvariable is omega else "c"
    if Doprint:
        print(f"Leading eigenvalue {EVlabel} = ", max)

    if Doprint:
        pp.printEVSorted(EVvariable)
        pp.printSpectrum(EVvariable, EVlabel)
        pp.printEVector(y_cheb, vv)
    return max, EVlabel

def runMultipleAplha(N, Re, alphas, D, D2, D4, y_cheb, U, U_yy):
    maxEVs = np.zeros(len(alphas))
    label = ""
    for i, alpha in enumerate(alphas):
       # for theta in range(100):
           # alpha = alpha * np.exp(1j * theta)
       if i % 10 == 0:
           print(f"Running {i} of {len(alphas)}")
       maxEV, label = runFixedAlpha(N, Re, alpha, D, D2, D4, y_cheb, U, U_yy, False)
       maxEVs = np.append(maxEVs, maxEV)
    pp.printSpectrum(maxEVs, label)



if __name__ == "__main__":
    deltaStar = 1
    re_deltaStar = 800
    # alpha = np.linspace(1, 20, 100)
    alpha = 1
    # filename = "data/points_x254.dat"
    filename = "../data/blasius.dat"
    
    eta_max = 40
    N = 1000
    x = np.linspace(0, eta_max, N)
    uinf = 1.0
   
    rd.blasius_profile(x, filename, uinf, re_deltaStar)

    # must be even to avoid errors
    N = 100

    # y = np.linspace(-1, 1, 2000)
    # U = poiseuille_flow(y)
    y, U, V = rd.read_baseflow(filename)

    # plt.plot(U, y, label="U")
    # plt.plot(V, y, label="V")
    # plt.legend()
    # plt.show()

    U_yy = np.gradient(np.gradient(U, y), y)

    y_cheb, D, D2, D4 = evp.getChebMatrices(N)
    y_cheb, D, D2, D4 = evp.adjustCoordinates(y_cheb, D, D2, D4, y[0], y[-1])
    
    U, U_yy = evp.interpolateCheb(y, y_cheb, U, U_yy)

    # plt.plot(U, y_cheb)
    # plt.show()

    runFixedAlpha(N, re_deltaStar, alpha, D, D2, D4, y_cheb, U, U_yy)

    # alphas = np.linspace(1, 15, 100)
    # runMultipleAplha(N, re_deltaStar, alphas, D, D2, D4, y_cheb, U, U_yy)
