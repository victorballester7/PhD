import numpy as np
from scipy.integrate import solve_bvp

def solve_BVP(dim_system, x):
    # Define the system of ODEs
    def odes(x, y):
        y1, y2, y3 = y
        dy1_dx = y2
        dy2_dx = y3
        dy3_dx = -0.5 * y1 * y3
        return np.vstack((dy1_dx, dy2_dx, dy3_dx))

    # Define the boundary conditions
    def bc(ya, yb):
        return np.array(
            [
                ya[0],  # y1(0) = f(0) = 0
                ya[1],  # y2(0) = f'(0) = 0
                yb[1] - 1,  # y2(inf) = f'(inf) = 1
            ]
        )

    y_guess = np.zeros((dim_system, x.size))
    eta_max = x[-1]
    y_guess[1, :] = x / eta_max  # Approximate guess for f'(x)

    # Solve the BVP
    solution = solve_bvp(odes, bc, x, y_guess, tol=1e-10, max_nodes=10000)

    # Check if the solution was successful
    if solution.success:
        print("BVP solved successfully!")
    else:
        print("BVP solution failed.")

    return solution

