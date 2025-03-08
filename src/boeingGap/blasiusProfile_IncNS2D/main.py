import numpy as np
from scipy.optimize import curve_fit
from . import physicalQuantities as pq 
from . import fitting as ft
from . import plot as pt
from . import solve_bvp as sbvp

if __name__ == "__main__":# Physical parameters
    u_inf = 1.0
    re_deltaStar = 1000

    # Numerical parameters
    dim_system = 3
    eta_max = 40
    p = 11  # order of the polynomial for the interpolation
    # Initial mesh and guess
    N = 1000  # discretization
    x = np.linspace(0, eta_max, N)  # Initial mesh

    limit_u = 1.0 
    limit_v = 1.7207876575205 # from wikipedia

    solution = sbvp.solve_BVP(dim_system, x)
    # Take the results
    y = solution.sol(x)

    coeffs_u, coeffs_v = ft.computeCoeffs(x, y, p)

    # p0 = [0.5, 0.1, 0.05, 0.02, 0.01, 0.005, 1, 1, 1, 1]  # Adjusted initial guesses
    p0 = np.ones(2*p - 1)
    def u_fit_scipy(eta, *params):
        return ft.u_fit(eta, p, limit_u, *params)  # Add return here

    def v_fit_scipy(eta, *params):
        return ft.v_fit(eta, p, limit_v, *params)  # Add return here

    ufit_coeffs, _ = curve_fit(u_fit_scipy, x, y[1], p0=p0)
    vfit_coeffs, _ = curve_fit(v_fit_scipy, x, x * y[1] - y[0], p0=p0)
 

    ft.plotCoeffs(ufit_coeffs, vfit_coeffs, p, limit_u, limit_v)

    ufit = ft.u_fit(x, p, limit_u, *ufit_coeffs)
    vfit = ft.v_fit(x, p, limit_v, *vfit_coeffs)

    largeX = np.linspace(0, 10000, 1000)
    ufit_large = ft.u_fit(largeX, p, limit_u, *ufit_coeffs)
    vfit_large = ft.v_fit(largeX, p, limit_v, *vfit_coeffs)
    # take first p+1 coefficients to u_fit and last p to v_fit
    # ufit = u_fit(x, *p0)
    # vfit = v_fit(x, *p0)


    delta = pq.computeDelta(x, y[1])
    deltaStar = pq.computeDeltaStar(y[0], eta_max)
    theta = pq.computeTheta(y[1], x)
    shapeFactor = deltaStar / theta
    print("delta        = ", delta, "* x / sqrt(Re_x)")
    print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
    print("theta        = ", theta, "* x / sqrt(Re_x)")
    print("delta/delta* = ", delta / deltaStar)
    print("H            = ", shapeFactor)

    re_x = pq.getRe_x(re_deltaStar, deltaStar)

    # writeSol2File(x, y, "../orrSommerfeldSquire/data/blasius.dat", Re_x)

    pt.plot(x, largeX, y, ufit, vfit, coeffs_u, coeffs_v, ufit_large, vfit_large, u_inf, re_x)
