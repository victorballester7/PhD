import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import subprocess
from typing import Tuple


def readData(filename: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    data = np.loadtxt(filename)

    omega_r = data[:, 0]
    omega_i = data[:, 1]
    alpha_r = data[:, 2]

    return omega_r, omega_i, alpha_r


def getMaxTemporalAnalysis(
    omega_r: np.ndarray, omega_i: np.ndarray, alpha_r: np.ndarray
) -> int:
    # Find the index of the maximum value of omega_i (most unstable mode)
    max_index = int(np.argmax(omega_i))

    return max_index


def domega_rdalpha_r(omega_r: np.ndarray, alpha_r: np.ndarray, max_index: int) -> float:
    # Calculate the derivative of omega_r with respect to alpha_r using non-uniform grid (just in case)

    h0 = alpha_r[max_index] - alpha_r[max_index - 1]
    h1 = alpha_r[max_index + 1] - alpha_r[max_index]

    diff = (
        omega_r[max_index + 1] * h0 / (h1 * (h0 + h1))
        + omega_r[max_index] * (h1 - h0) / (h0 * h1)
        - omega_r[max_index - 1] * h1 / (h0 * (h0 + h1))
    )
    return diff


def gasterTransform(
    omega_r: np.ndarray, omega_i: np.ndarray, alpha_r: np.ndarray
) -> float:
    max_index = getMaxTemporalAnalysis(omega_r, omega_i, alpha_r)
    diff = domega_rdalpha_r(omega_r, alpha_r, max_index)

    omega_i_temp = omega_i[max_index]

    alpha_i = -omega_i_temp / diff

    return alpha_i


def editFile(pathFile: Path, replacement_line, line_startswith) -> None:
    # Read the file and replace the specified line
    with open(pathFile, "r") as file:
        lines = file.readlines()

    with open(pathFile, "w") as file:
        for line in lines:
            linechanged = False
            # loop in the i,j in (replacement_line, line_startswith)
            for rep_line, line_start in zip(replacement_line, line_startswith):
                if line.strip().startswith(line_start):
                    file.write(rep_line + "\n")
                    linechanged = True
                    break
            if not linechanged:
                file.write(line)


def getDatafromDNS(n_interp_dns, pathCurrentScript: str) -> np.ndarray:
    # Define the x positions
    xpositions = np.arange(50, 1001, 50)
    xpositions = np.insert(xpositions, 0, 20)

    # Create the string to replace the X= line
    values_str = " ".join(str(x) for x in xpositions)
    replacement_line = np.array([f"X=({values_str})", f"N={n_interp_dns}"])
    line_startswith = np.array(["X=(", "N="])

    # Path to the script
    filenameScript = "../scripts/createPointsOfSectionDomain.sh"
    filenameScript = Path(os.path.join(pathCurrentScript, filenameScript))

    # Read and modify the script
    editFile(filenameScript, replacement_line, line_startswith)

    # Make the script executable and run it
    subprocess.run([filenameScript], check=True)

    return xpositions


def runOStemporalAnalysis(
    x: int, widthGap: int, n_interp_dns: int, tomlFile: Path
) -> None:
    replacement_line = f'filenameUprofile = "/home/victor/Desktop/PhD/src/boeingGapRe1000IncNS/baseflow/dns/d4_w{widthGap}/data/points_x{x}_n{n_interp_dns}.dat"'
    line_startswith = "filenameUprofile = "

    # Read and modify the toml file
    editFile(tomlFile, replacement_line, line_startswith)

    dirMakefile = Path(os.path.join(os.path.dirname(tomlFile), "../"))

    # run 'make run' in the dirMakefile directory
    subprocess.run(["make", "run"], cwd=dirMakefile, check=True)

    return


def setupToml(
    filenameToml: Path, alpha_r_min: float, alpha_r_max: float, alpha_r_num: int
) -> None:
    line_startswith = np.array(
        [
            "n = ",
            "re = ",
            "branch = ",
            "problem = ",
            "doPlot = ",
            "use_c = ",
            "run_multiple = ",
            "plotUprofile = ",
            "vars_r = ",
        ]
    )
    replacement_line = np.array(
        [
            "n = 200",
            "re = 1000",
            'branch = "temporal" # Options are: "temporal", "spatial"',
            'problem = "Custom" # Options are: "BoundaryLayer, "Poiseuille", "Couette", "Custom"',
            "doPlot = false",
            "use_c = false # When temporal branch is used, plot in terms of c instead of omega (omega = alpha * c)",
            "run_multiple = true",
            "plotUprofile = false",
            f"vars_r = {{min = {alpha_r_min}, max = {alpha_r_max}, num = {alpha_r_num}}}",
        ]
    )
    editFile(filenameToml, replacement_line, line_startswith)

    return

def computeNfactor(a, b, alpha_i_a, alpha_i_b, nfactor_a):
    trapezoidal = (a + b) * (alpha_i_b + alpha_i_a) / 2
    nfactor_b = nfactor_a + trapezoidal
    return nfactor_b

def plotNfactor(xpositions, nfactor):
    plt.plot(xpositions, nfactor, marker="o", label="N-factor")
    plt.xlabel("x")
    plt.ylabel("n(x)")
    plt.grid()
    plt.legend()
    plt.show()

def main():
    # PARAMETERS TO CHANGE
    widthGap = 15
    n_interp_dns = 400
    alpha_r_min = 0.05
    alpha_r_max = 0.4
    alpha_r_num = 50

    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))
    xpositions = getDatafromDNS(n_interp_dns, pathCurrentScript)

    tomlFile = "../src/boeingGapRe1000IncNS/orrSommerfeld/config/input.toml"
    tomlFile = Path(os.path.join(pathCurrentScript, tomlFile))
    filename_ev = "../src/boeingGapRe1000IncNS/orrSommerfeld/data/eigenvalues.dat"
    filename_ev = Path(os.path.join(pathCurrentScript, filename_ev))

    alphas_i = np.array([0.0])
    nfactor = np.array([0.0])

    # Setup the toml file
    setupToml(tomlFile, alpha_r_min, alpha_r_max, alpha_r_num)

    x_old = widthGap
    for x in xpositions:
        runOStemporalAnalysis(x, widthGap, n_interp_dns, tomlFile)
        omega_r, omega_i, alpha_r = readData(filename_ev)

        alpha_i_x = gasterTransform(omega_r, omega_i, alpha_r)

        alphas_i = np.append(alphas_i, alpha_i_x)

        n_x = computeNfactor(x_old, x, alphas_i[-2], alphas_i[-1], nfactor[-1])
        nfactor = np.append(nfactor, n_x)

    plotNfactor(xpositions, nfactor)


if __name__ == "__main__":
    main()
