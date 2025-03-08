import numpy as np
import sys
import os

# Add boeingGap to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from blasiusProfile_IncNS2D import solve_bvp as sbvp
from blasiusProfile_IncNS2D import physicalQuantities as pq


def read_baseflow(filename: str):
    data = np.loadtxt(filename, skiprows=3)
    y = data[:, 1]
    U = data[:, 2]
    V = data[:, 3]
    return y, U, V


def poiseuille_flow(y: np.ndarray):
    return 1 - y**2

def writeSol2File(x, y, filename, u_inf, re_x):
    with open(filename, "w") as file:
        file.write("# Blasius solution\n")
        file.write("\n")
        file.write("# x y U V\n")
        for i in range(x.size):
            u = u_inf * y[1][i]
            v = 0.5 * u_inf / np.sqrt(re_x) * (x[i] * y[1][i] - y[0][i])
            file.write("0 " + str(x[i]) + " " + str(u) + " " + str(v) + "\n")

def blasius_profile(x: np.ndarray, filename: str, u_inf: float, re_deltaStar: float):
    solution = sbvp.solve_BVP(3, x)
    y = solution.sol(x)
    re_x = pq.getRe_x(re_deltaStar,  pq.computeDeltaStar(y[0], x[-1]))
    writeSol2File(x, y, filename, u_inf, re_x)
    return




