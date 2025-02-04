import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Physical parameters
U_inf = 1.0
Re_deltaStar = 1000

# Numerical parameters
dim_system = 3
eta_max = 10
p = 11  # order of the polynomial for the interpolation
# Initial mesh and guess
N = 1000  # discretization
x = np.linspace(0, eta_max, N)  # Initial mesh

limit_u = 1.0 
limit_v = 1.7207876575205 # from wikipedia

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


def getRe_x(Re_deltaStar, deltaStar):
    return (Re_deltaStar / deltaStar) ** 2


# BL thickness
def computeDelta(x, fprime):
    # thinkness boundary layer (as first index of x_plot such that y_plot[1] > 0.99)
    limit = 0.99
    aux = np.abs(fprime - limit)
    idx = np.where(aux == np.min(aux))[0]
    if fprime[idx] < limit:
        idx1 = idx
        idx2 = idx + 1
    else:
        idx1 = idx - 1
        idx2 = idx

    L = fprime[idx2] - fprime[idx1]  # which is > 0
    d1 = limit - fprime[idx1]
    d2 = L - d1
    delta = ((d1 * x[idx2] + d2 * x[idx1]) / L)[0]
    return delta


# displacement thickness
def computeDeltaStar(f, eta_max):
    # to compute deltaStar, we need to integrate (1-y[1]) from 0 to infinity (actually till etamax, as approximated)
    # deltaStar = quad(lambda x: 1 - np.polyval(coeffs_fprime, x), 0, eta_max)[0]
    # print("deltaStar = ", deltaStar)
    # use numpy to compute the integral (they are basically the same, around 1e-7 difference for N = 10000)
    # deltaStar = np.trapezoid(1 - fprime, x)
    # print("deltaStar = ", deltaStar)

    # exact value is (eta - f(eta))|_0^inf = lim_{eta->inf} eta - f(eta) + f(0) = lim_{eta->inf} eta - f(eta)
    deltaStar = eta_max - f[-1]
    return deltaStar


# momentum thickness
def computeTheta(fprime, x):
    # to compute theta, we need to integrate f'(1-f') from 0 to infinity (actually till etamax, as approximated)
    theta = np.trapezoid(fprime * (1 - fprime), x)
    return theta


# def u_fit(x, a1, a2, a3, a4):
#     return a1 * np.tanh(a2 * x) + a3 * x * np.exp(-a4 * x)

# def u_fit(x, a1, a2, a3, a4):
#     return 1 -a1 * np.exp(-a2 * x) - a3 * np.exp(-a4 * x)

# def u_fit(x, A1, A2, A3, A4, A5, A6, B1, B2, B3, B4):
#     return 1 - (A1 * x + A2 * x**2 + A3 * x**3 + A4 * x**4 + A5 * x**5) * np.exp(-B1 * x) - \
#                (A6 * x**2) * np.exp(-B2 * x) - \
#                (A3 * x**3) * np.exp(-B3 * x) - \
#                (A4 * x**4) * np.exp(-B4 * x)

# rational function for f'
def u_fit(eta, *params):
    num = sum(params[i] * eta**(i+1) for i in range(p))  # we impose that the function is zero at the origin
    den = 1 + sum(params[p + j] * eta**(j + 1) for j in range(p-1)) + params[p-1]/limit_u * eta**p # we impose that the function is 1 at infinity 
    return num / den

# def v_fit(x, a1, a2, a3, a4):
#     return a1 * x * np.exp(-a2 * x) + a3 * x ** 2 * np.exp(-a4 * x)

# def v_fit(x, a1, a2, a3, a4):
#     return a1 * x**2 * np.exp(-a2 * x) + a3 * np.tanh(a4 * x)

# def v_fit(x, A1, A2, A3, A4, A5, A6, B1, B2, B3, B4):
#     return (A1 * x + A2 * x**2 + A3 * x**3 + A4 * x**4 + A5 * x**5) * np.exp(-B1 * x) + \
#            (A6 * x**2) * np.exp(-B2 * x) + \
#            (A3 * x**3) * np.exp(-B3 * x) + \
#            (A4 * x**4) * np.exp(-B4 * x)

# rational function for x f' - f
def v_fit(eta, *params):
    num = sum(params[i] * eta**(i+1) for i in range(p))  # we impose that the function is zero at the origin
    den = 1 + sum(params[p + j] * eta**(j + 1) for j in range(p-1)) + params[p-1]/limit_v * eta**p # we impose that the function is 1 at infinity 
    return num / den

def constrained_polyfit(x, y, p):
    """
    Fit a polynomial of order p to data (x, y), constrained to pass through the origin.
    Args:
        x (array-like): x data points
        y (array-like): y data points
        p (int): Polynomial order (excluding constant term)
    Returns:
        coeffs (ndarray): Coefficients of the fitted polynomial [a_1, a_2, ..., a_p]
    """
    # Create the Vandermonde matrix without the constant term
    X = np.vander(x, p + 1)[
        :, :-1
    ]  # Drop the last column corresponding to the constant term

    # Solve the linear least-squares problem
    coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    return coeffs


def computeCoeffs(x, y, p):
    # interpolate with polynomial of order p, the solutions y_plot[1] and y_plot[3]
    coeffs_u = constrained_polyfit(x, y[1], p)
    coeffs_v = constrained_polyfit(x, x * y[1] - y[0], p)
    return coeffs_u, coeffs_v

def plotCoeffs(coeffs_u, coeffs_v):
    # for rational function
    for i, coeff in enumerate(coeffs_u):
        if i < p:
            print("<p> a" + str(i+1) + "_u", "=", coeff, "</p>")
        else:
            print("<p> b" + str(i-p+1) + "_u", "=", coeff, "</p>")
    print("<p> b" + str(p) + "_u", "=", coeffs_u[p-1]/limit_u, "</p>")

    for i, coeff in enumerate(coeffs_v):
        if i < p:
            print("<p> a" + str(i+1) + "_v", "=", coeff, "</p>")
        else:
            print("<p> b" + str(i-p+1) + "_v", "=", coeff, "</p>")
    print("<p> b" + str(p) + "_v", "=", coeffs_v[p-1]/limit_v, "</p>")

def plot(x, xlarge, y, ufit, vfit, coeffs_u, coeffs_v,ufit_large, vfit_large, Uinf, Re_x):
    # plot the solutions
    fitted_poly_u = np.poly1d(np.hstack([coeffs_u, 0]))  # Add 0 for the constant term
    fitted_poly_v = np.poly1d(np.hstack([coeffs_v, 0]))  # Add 0 for the constant term

    u = Uinf * y[1]
    u_polyaprox = Uinf * fitted_poly_u(x)
    u_aprox = Uinf * ufit

    v = 0.5 * Uinf / np.sqrt(Re_x) * (x * y[1] - y[0])
    v_polyaprox = 0.5 * Uinf / np.sqrt(Re_x) * fitted_poly_v(x)
    v_aprox = 0.5 * Uinf / np.sqrt(Re_x) * vfit


    print("u_inf = ", u[-1])
    print("v_inf = ", v[-1])

    print("||u - u_polyaprox||_oo = ", np.max(np.abs(u - u_polyaprox)))
    print("||u - u_aprox||_oo = ", np.max(np.abs(u - u_aprox)))
    print("||v - v_polyaprox||_oo = ", np.max(np.abs(v - v_polyaprox)))
    print("||v - v_aprox||_oo = ", np.max(np.abs(v - v_aprox)))

    # Create the figure and the primary axis
    fig, ax1 = plt.subplots()

    # Plot u with the first axis
    ax1.plot(u, x, label=r"$U_\infty f'(x)$")
    ax1.plot(u_polyaprox, x, label=r"$Uinf*f'(x)$ polyfit")
    ax1.plot(u_aprox, x, label=r"$Uinf*f'(x)$ exp fit")
    # ax1.plot(ufit_large, xlarge, label=r"$Uinf*f'(x)$ exp fit large")

    
    # plot a dashed line at Uinf
    ax1.axvline(Uinf, color="black", linestyle="--")

    # Show the plot
    ax1.set_xlabel(r"$U_\infty f'(x)$")

    # Create the second x-axis sharing the same y-axis
    ax2 = ax1.twiny()

    # Plot v with the second x-axis
    ax2.plot(
        v, x, label=r"$0.5 U_\infty / \sqrt{Re_x} (x f'(x) - f(x))$", color="green"
    )
    ax2.plot(
        v_polyaprox,
        x,
        label=r"$0.5 * Uinf / \sqrt{ Re_x } * (x * f'(x) - f(x))$ polyfit",
        color="red",
    )
    ax2.plot(
        v_aprox,
        x,
        label=r"$0.5 * Uinf / \sqrt{ Re_x } * (x * f'(x) - f(x))$ exp fit",
        color="orange",
    )
    # ax2.plot(
    #     vfit_large,
    #     xlarge,
    #     label=r"$0.5 * Uinf / \sqrt{ Re_x } * (x * f'(x) - f(x))$ exp fit large",
    #     color="purple",
    # )
    ax2.set_xlabel(r"$0.5  U_\infty / \sqrt{Re_x}  (x f'(x) - f(x))$")
    ax2.axvline(0.5 * Uinf / np.sqrt(Re_x) * 1.7207876389249748, color="gray", linestyle="--")

    # Add a legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    solution = solve_BVP(dim_system, x)
    # Take the results
    y = solution.sol(x)

    coeffs_u, coeffs_v = computeCoeffs(x, y, p)

    # p0 = [0.5, 0.1, 0.05, 0.02, 0.01, 0.005, 1, 1, 1, 1]  # Adjusted initial guesses
    p0 = np.ones(2*p - 1)
    ufit_coeffs, _ = curve_fit(u_fit, x, y[1], p0=p0)
    vfit_coeffs, _ = curve_fit(v_fit, x, x * y[1] - y[0], p0=p0)

    plotCoeffs(ufit_coeffs, vfit_coeffs)

    ufit = u_fit(x, *ufit_coeffs)
    vfit = v_fit(x, *vfit_coeffs)

    largeX = np.linspace(0, 10000, 1000)
    ufit_large = u_fit(largeX, *ufit_coeffs)
    vfit_large = v_fit(largeX, *vfit_coeffs)
    # take first p+1 coefficients to u_fit and last p to v_fit
    # ufit = u_fit(x, *p0)
    # vfit = v_fit(x, *p0)


    delta = computeDelta(x, y[1])
    deltaStar = computeDeltaStar(y[0], eta_max)
    theta = computeTheta(y[1], x)
    shapeFactor = deltaStar / theta
    print("delta        = ", delta, "* x / sqrt(Re_x)")
    print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
    print("theta        = ", theta, "* x / sqrt(Re_x)")
    print("delta/delta* = ", delta / deltaStar)
    print("H            = ", shapeFactor)

    Re_x = getRe_x(Re_deltaStar, deltaStar)

    plot(x, largeX, y, ufit, vfit, coeffs_u, coeffs_v, ufit_large, vfit_large, U_inf, Re_x)
