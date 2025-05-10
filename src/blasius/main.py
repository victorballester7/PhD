import numpy as np
import physicalQuantities as pq
import fitting as ft
import plot as pt
import solve_bvp as sbvp


def filter_out(x, y, ufit, vfit, x_limit):
    # Filter out the values where x is greater than x_limit
    idx = np.where(x < x_limit)[0]
    x = x[idx]
    y = y[:, idx]
    ufit = ufit[:, idx]
    vfit = vfit[:, idx]
    return x, y, ufit, vfit


def main():
    u_inf = 1.0
    re_deltaStar = 1000

    # Numerical parameters
    dim_system = 3
    eta_max = 15
    p = 11  # order of the polynomial for the interpolation
    q = 1
    # Initial mesh and guess
    N = 501  # discretization
    x = np.linspace(0, eta_max, N)  # Initial mesh

    solution = sbvp.solve_BVP(dim_system, x)
    # Take the results
    y = solution.sol(x)

    delta = pq.computeDelta(x, y[1])
    deltaStar = pq.computeDeltaStar(x, y[0])
    theta = pq.computeTheta(y[1], x)
    shapeFactor = deltaStar / theta

    limit_u = u_inf
    limit_v = deltaStar

    ufit1, vfit1 = ft.fitting(
        x, y, ft.u_fit, ft.v_fit, p, 2 * p - 1, limit_u, limit_v
    )  # fitting


    # ufit2, vfit2 = ft.fitting(
    #     x, y, ft.u_fit_exp, ft.v_fit_exp, p, 2 * p + q, limit_u, limit_v
    # )  # fitting with exponential decay

    ufit = np.array([ufit1])
    vfit = np.array([vfit1])

    # take first p+1 coefficients to u_fit and last p to v_fit
    # ufit = u_fit(x, *p0)
    # vfit = v_fit(x, *p0)

    print("delta        = ", delta, "* x / sqrt(Re_x)")
    print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
    print("theta        = ", theta, "* x / sqrt(Re_x)")
    print("delta/delta* = ", delta / deltaStar)
    print("H            = ", shapeFactor)

    re_x = pq.getRe_x(re_deltaStar, deltaStar)

    # writeSol2File(x, y, "../orrSommerfeldSquire/data/blasius.dat", Re_x)
    
    # filter out x >= 15
    x_limit = 15
    # x, y, ufit, vfit = filter_out(x, y, ufit, vfit, x_limit)

    pt.plot(x, y, ufit, vfit, u_inf, re_x, deltaStar)


if __name__ == "__main__":  # Physical parameters
    main()
