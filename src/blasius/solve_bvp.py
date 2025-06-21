import numpy as np
from scipy.integrate import solve_bvp


def solve_BVP_incNS(dim_system, x):
    # Define the system of ODEs
    def odes(x, y):
        f0, f1, f2 = y
        df0_dx = f1
        df1_dx = f2
        df2_dx = -0.5 * f0 * f2
        return np.vstack((df0_dx, df1_dx, df2_dx))

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

    if solution.success:
        print("BVP solved successfully!")
    else:
        print("BVP solution failed.")

    return solution


def solve_BVP_comNS(dim_system, x, Pr, muInf, TInf, uInf, vinf, cp):
    # ref values for Sutherland's law
    muRef = 1.716e-5
    TRef = 273.15
    S = 110.4

    # total enthalpy at infinity
    h0Inf = cp * TInf + 0.5 * (uInf**2 + vinf**2)

    # Define the system of ODEs
    def odes(x, y):
        f0, f1, f2, g0, g1 = y

        T = (TInf + uInf**2 / (2 * cp)) * g0 - uInf**2 / (2 * cp) * f1**2
        dT = (TInf + uInf**2 / (2 * cp)) * g1 - uInf**2 / cp * f1 * f2
        C = muRef / muInf * (TInf * T**0.5 / TRef**1.5) * (TRef + S) / (T + S)
        dC = (1 / (2 * T) - 1 / (T + S)) * C * dT

        df0_dx = f1
        df1_dx = f2
        df2_dx = -dC / C * f2 - 1 / C * f0 * f2
        dg0_dx = g1
        dg1_dx = (
            -dC / C * g1
            - uInf**2 / h0Inf * Pr / C * f2**2
            - Pr / C * f0 * g1
        )
        return np.vstack((df0_dx, df1_dx, df2_dx, dg0_dx, dg1_dx))

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

    if solution.success:
        print("BVP solved successfully!")
    else:
        print("BVP solution failed.")

    return solution
