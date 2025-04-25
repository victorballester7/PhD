import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Example data
data = np.array(
    [
        [1, 30, -1],
        [1, 34, -1],
        [1, 38, -1],
        [1, 50, -1],
        [1, 60, -1],
        [1, 70, -1],
        [1, 80, -1],
        [1, 90, -1],
        [1, 110, -1],
        [1, 130, -1],
        [
            1,
            80,
        ],
        [
            1,
            100,
        ],
        [
            1,
            120,
        ],
        [
            2,
            10,
        ],
        [
            2,
            16,
        ],
        [2, 24, -1],
        [2, 28, -1],
        [2, 32, -1],
        [2, 36, -1],
        [2, 44, -1],
        [2, 52, -1],
        [
            2,
            54,
        ],
        [
            2,
            56,
        ],
        [
            2,
            58,
        ],
        [2, 60, 1],
        [2, 65, 1],
        [2, 70, 1],
        [
            2.5,
            20,
        ],
        [
            2.5,
            25,
        ],
        [
            2.5,
            30,
        ],
        [
            2.5,
            35,
        ],
        [
            2.5,
            40,
        ],
        [
            2.5,
            45,
        ],
        [3, 15, -1],
        [
            3,
            15.5,
        ],
        [3, 16, 1],
        [3, 17, 1],
        [3, 18, 1],
        [3, 22, 1],
        [3, 26, 1],
        [
            3.5,
            15,
        ],
        [
            3.5,
            15.5,
        ],
        [
            3.5,
            16,
        ],
        [4, 14, -1],
        [4, 15, -1],
        [
            4,
            15.5,
        ],
        [4, 16, -1],
        [4, 17, 1],
        [4, 18, 1],
        [4, 19, 1],
    ]
)


D = data[:, 0]  # D values
W = data[:, 1]  # W values
Z = data[:, 2]  # Z values

# Create colormap: blue for -1, red for 1, white for NaN
cmap = ListedColormap(["blue", "red"])

plt.figure(figsize=(8, 5))
plt.scatter(W, D, c=Z, cmap=cmap, marker="o", s=20)
plt.xlabel("w/delta*")
plt.ylabel("d/delta*")
plt.title("Heatmap of Z (red=1, blue=-1, white=transition)")
plt.colorbar(ticks=[-1, 1], label="Z value")
plt.show()
