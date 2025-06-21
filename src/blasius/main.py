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


def writeSol2File(x, y, filename, re_deltaStar, uinf, deltaStar, max_x):
    re_x = pq.getRe_x(re_deltaStar, deltaStar)

    # normalize x so that delta* = 1
    x_norm = x / deltaStar
    with open(filename, "w") as f:
        f.write(
            "# Blasius solution at Re_deltaStar = "
            + str(re_deltaStar)
            + " and using deltaStar = 1\n"
        )
        f.write("# y u v u_y u_yy\n")
        for i in range(len(x)):
            if x[i] > max_x:
                break

            u = y[1][i]
            u_y = y[2][i]
            u_yy = -y[0][i] * y[2][i] / 2
            v = 0.5 * uinf / np.sqrt(re_x) * (x[i] * y[1][i] - y[0][i])
            f.write(f"{x_norm[i]} {u} {v} {u_y} {u_yy}\n")

        if x[-1] < max_x:
            dx = x[-1] - x[-2]
            xnew = x[-1]
            u = y[1][-1]
            u_y = y[2][-1]
            u_yy = -y[0][-1] * y[2][-1] / 2
            v = 0.5 * uinf / np.sqrt(re_x) * (x[-1] * y[1][-1] - y[0][-1])
            while xnew < max_x:
                xnew += dx
                f.write(f"{xnew} {u} {v} {u_y} {u_yy}\n")


def main():
    uinf = 1.0
    re_deltaStar = 1000

    # Numerical parameters
    dim_system = 3
    eta_max = 15
    p = 11  # order of the polynomial for the interpolation
    # Initial mesh and guess
    N = 501  # discretization
    x = np.linspace(0, eta_max, N)  # Initial mesh
    incNS = False

    if incNS:
        solution = sbvp.solve_BVP_incNS(dim_system, x)
    else:
        Pr = 0.72
        rhoInf = 1
        deltaStar_comNS = 1
        muInf = rhoInf * uinf * deltaStar_comNS / re_deltaStar 
        TInf = 1 

        solution = sbvp.solve_BVP_comNS(dim_system, x)
    # Take the results
    y = solution.sol(x)

    delta = pq.computeDelta(x, y[1])
    deltaStar = pq.computeDeltaStar(x, y[0])
    theta = pq.computeTheta(y[1], x)
    shapeFactor = deltaStar / theta

    limit_u = uinf
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
    if incNS:
        print("Using INCOMPRESSIBLE Navier-Stokes equations")
    else:
        print("Using COMPRESSIBLE Navier-Stokes equations")

    print("delta        = ", delta, "* x / sqrt(Re_x)")
    print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
    print("theta        = ", theta, "* x / sqrt(Re_x)")
    print("delta/delta* = ", delta / deltaStar)
    print("H            = ", shapeFactor)

    max_x = 75
    writeSol2File(
        x,
        y,
        "/home/victor/Desktop/orrSommerfeld/data/blasius.dat.normalized",
        re_deltaStar,
        uinf,
        deltaStar,
        max_x,
    )

    # filter out x >= 15
    x_limit = 15
    # x, y, ufit, vfit = filter_out(x, y, ufit, vfit, x_limit)

    pt.plot(x, y, ufit, vfit, uinf, re_deltaStar, deltaStar)


if __name__ == "__main__":  # Physical parameters
    main()
