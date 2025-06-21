import numpy as np
import matplotlib.pyplot as plt
import os

def read_points_from_file(filename):
    """Reads points from a file and returns them as a numpy array."""
    return np.loadtxt(filename, skiprows=3)

def main(dataFile):
    """Main function to read data and plot points."""
    # Read data from file
    points = read_points_from_file(dataFile)

    # Extract x and y coordinates
    x, y, u, v, p = points[:, 0], points[:, 1], points[:, 2], points[:, 3], points[:, 4]


    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the points
    ax.plot(x, v, 'o', markersize=2, label='Points')

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

    dataFile = "../src/incNSboeingGapRe1000/arnoldiLinearSolver/d2.25_w32/data/points_y1_n800.dat"
    dataFile = os.path.join(pathCurrentScript, dataFile)


    main(dataFile)
