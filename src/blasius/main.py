import numpy as np
import physicalQuantities as pq
import physicalParameters as pp
from misc import writeSol2File, filter_out
import fitting as ft
import plot as pt
import solve_bvp as sbvp
from scipy.integrate import cumulative_trapezoid


def main():
    # Numerical parameters
    eta_max = 11.5
    p = 11  # order of the polynomial for the interpolation
    # Initial mesh and guess
    N = 401  # discretization
    x = np.linspace(0, eta_max, N)  # Initial mesh

    param = pp.PhysicalParameters(
        x_inflow=-100,
        incNS=True,
        uinf=1.0,
        rhoinf=1.0,
        re_deltaStar=1000,
        Mainf=0.8,
        Pr=0.72,
        Tinf=1.0,
        Twall_dimensionless=1.0,  # = Tinf
        gamma=1.4,
        adiabatic=False,  # False => isothermal wall
    )
    dim_system = 3 if param.incNS else 5

    if param.incNS:
        solution = sbvp.solve_BVP_incNS(dim_system, x)
    else:
        solution = sbvp.solve_BVP_comNS(dim_system, x, param)

    # Take the results
    y = solution.sol(x)

    param.delta = pq.computeDelta(x, y, param.incNS)
    param.deltaStar = pq.computeDeltaStar(x, y, param.incNS)
    param.theta = pq.computeTheta(x, y, param.incNS)
    param.shapeFactor = param.deltaStar / param.theta

    limit_u = 1.0
    limit_v = param.deltaStar if param.incNS else np.trapezoid(y[3], x) - y[0][-1]

    ufit1, vfit1 = ft.fitting(
        x, y, param.incNS, p, limit_u, limit_v
    )  # fitting

    limit_rho = 1.0
    rho_fit, rhou_fit, rhov_fit, E1_fit, E2_fit = 0, 0, 0, 0, 0
    if not param.incNS:
        limits = [
            limit_rho,
            limit_rho * limit_u,
            limit_rho * limit_v,
            limit_u**2,
            limit_v**2,
        ]
        rho_fit, rhou_fit, rhov_fit, E1_fit, E2_fit = ft.fitting_comNS(
            x, y, p, limits, param
        )

    # ufit2, vfit2 = ft.fitting(
    #     x, y, ft.u_fit_exp, ft.v_fit_exp, p, 2 * p + q, limit_u, limit_v
    # )  # fitting with exponential decay

    ufit = np.array([ufit1])
    vfit = np.array([vfit1])

    # take first p+1 coefficients to u_fit and last p to v_fit
    # ufit = u_fit(x, *p0)
    # vfit = v_fit(x, *p0)
    if param.incNS:
        #change color of print
        print("\nUsing "+  "\033[92m" + "INCOMPRESSIBLE"+  "\033[0m" + " Navier-Stokes equations\n")
    else:
        print("\nUsing " + "\033[92m" + "COMPRESSIBLE" + "\033[0m" + " Navier-Stokes equations\n")

    print(param)

    max_x = 75
    # ask the user if he wants to write the solution to a file
    write_path = "/home/victor/Desktop/orrSommerfeld/data/blasius.dat.normalized"
    print(f"Do you want to write the solution to a '{write_path}'? (y/n) Default: n")
    write_to_file = input().strip().lower() == "y"
    if write_to_file:
        print("Writing solution to file...")
        writeSol2File(
            x,
            y,
            write_path,
            max_x,
            param,
        )
        print("Solution written to blasius.dat")

    # filter out x >= 15
    x_limit = 15
    # x, y, ufit, vfit = filter_out(x, y, ufit, vfit, x_limit)
    x_eq_L = -100  # x at which we want to compare with DNS data
    path_dns = (
        "../flatSurfaceRe1000IncNS/linearSolver_blowingSuction/data/points_x"
        + str(x_eq_L)
        + "_n800.dat"
    )

    print(
        f"Do you want to plot as well the DNS data from '{path_dns}'? (y/n) Default: n"
    )
    plot_dns = input().strip().lower() == "y"

    pt.plot(
        x,
        y,
        param.incNS,
        ufit,
        vfit,
        plot_dns,
        x_eq_L,
        path_dns,
        param,
    )

    if not param.incNS:
        pt.plot_comNS(
            x,
            y,
            [rho_fit, rhou_fit, rhov_fit, E1_fit, E2_fit],
            plot_dns,
            x_eq_L,
            path_dns,
            param,
        )


if __name__ == "__main__":  # Physical parameters
    main()
