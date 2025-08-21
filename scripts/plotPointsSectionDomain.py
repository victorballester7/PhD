import numpy as np
import matplotlib.pyplot as plt
import os

def read_points_from_file(filename):
    """Reads points from a file and returns them as a numpy array."""
    return np.loadtxt(filename, skiprows=3)

def addDataToPlot(ax, points: np.ndarray):
     # Extract x and y coordinates
    x, y, u, v, p = points[:, 0], points[:, 1], points[:, 2], points[:, 3], points[:, 4]

    # check if the data in x is all the same
    var = np.array([])
    if np.all(x == x[0]):
        var = y
    else:
        var = x

    # Create a figure and axis

    # Plot the points
    ax.plot(u, var, '--', markersize=2, label='u', alpha=0.4)
    ax.plot(v, var, ':', markersize=2, label='v', alpha=0.4)
    abs_sqrt = np.sqrt(u**2 + v**2)
    ax.plot(abs_sqrt, var, '-', markersize=2, label='sqrt(u^2 + v^2)')

    # Set labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('v')

def main(dataFile: np.ndarray):
    """Main function to read data and plot points."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for dF in dataFile:
        # Read data from file
        points = read_points_from_file(dF)
        
        # Add data to plot
        addDataToPlot(ax, points)

    # Set labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('v')

    # Add grid and legend
    ax.grid()
    ax.legend()

    # Show the plot
    plt.show()
    

if __name__ == "__main__":
    # script path
    pathCurrentScript = os.path.dirname(os.path.abspath(__file__))

    basePath = "../src/incNSboeingGapRe1000/directLinearSolver/blowingSuction/d4_w15/wgnMorePoints/data/"
    basePath = os.path.join(pathCurrentScript, basePath)

    dataFile = [
        # "points73_x200_n300.dat",
        "points73_x500_n800.dat",
        # "points73_x800_n300.dat",
        ]
    dataFile = [os.path.join(basePath, f) for f in dataFile]
    dataFile = np.array(dataFile)

    main(dataFile)
