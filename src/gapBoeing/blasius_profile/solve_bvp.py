import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Physical parameters
U_inf = 1.0
Re_deltaStar = 1000

# Numerical parameters
dim_system = 3
eta_max = 9
eta_max_int = 10  # for the integral and interpolation
p = 11  # order of the polynomial for the interpolation
# Initial mesh and guess
N = 1000  # discretization
x_int = np.linspace(0, eta_max_int, N)  # Extend to large x for "infinity"
x = np.linspace(0, eta_max, N)  # Initial mesh


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
    solution = solve_bvp(odes, bc, x, y_guess, tol=1e-8, max_nodes=10000)

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
    for i, coeff in enumerate(coeffs_u):
        print("<p> c" + str(i) + "_u", "=", coeff, "</p>")

    for i, coeff in enumerate(coeffs_v):
        print("<p> c" + str(i) + "_v", "=", coeff, "</p>")
    return coeffs_u, coeffs_v


def plot(x, y, coeffs_u, coeffs_v, Uinf, Re_x):
    # plot the solutions
    fitted_poly_u = np.poly1d(np.hstack([coeffs_u, 0]))  # Add 0 for the constant term
    fitted_poly_v = np.poly1d(np.hstack([coeffs_v, 0]))  # Add 0 for the constant term

    u = Uinf * y[1]
    u_aprox = Uinf * fitted_poly_u(x)
    v = 0.5 * Uinf / np.sqrt(Re_x) * (x * y[1] - y[0])
    v_aprox = 0.5 * Uinf / np.sqrt(Re_x) * fitted_poly_v(x)

    print("u_inf = ", u[-1])
    print("v_inf = ", v[-1])

    # Create the figure and the primary axis
    fig, ax1 = plt.subplots()

    # Plot u with the first axis
    ax1.plot(u, x, label=r"$U_\infty f'(x)$")
    ax1.plot(u_aprox, x, label=r"$Uinf*f'(x)$ polyfit")

    # Show the plot
    ax1.set_xlabel(r"$U_\infty f'(x)$")

    # Create the second x-axis sharing the same y-axis
    ax2 = ax1.twiny()

    # Plot v with the second x-axis
    ax2.plot(
        v, x, label=r"$0.5 U_\infty / \sqrt{Re_x} (x f'(x) - f(x))$", color="green"
    )
    ax2.plot(
        v_aprox,
        x,
        label=r"$0.5 * Uinf / \sqrt{ Re_x } * (x * f'(x) - f(x))$ polyfit",
        color="red",
    )
    ax2.set_xlabel(r"$0.5  U_\infty / \sqrt{Re_x}  (x f'(x) - f(x))$")

    plt.grid()
    plt.show()


solution = solve_BVP(dim_system, x_int)
# Take the results
y_int = solution.sol(x_int)
y = solution.sol(x)

coeffs_u, coeffs_v = computeCoeffs(x_int, y_int, p)

delta = computeDelta(x_int, y_int[1])
deltaStar = computeDeltaStar(y_int[0], eta_max_int)
theta = computeTheta(y_int[1], x_int)
shapeFactor = deltaStar / theta
print("delta        = ", delta, "* x / sqrt(Re_x)")
print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
print("theta        = ", theta, "* x / sqrt(Re_x)")
print("delta/delta* = ", delta / deltaStar)
print("H            = ", shapeFactor)

Re_x = getRe_x(Re_deltaStar, deltaStar)

plot(x, y, coeffs_u, coeffs_v, U_inf, Re_x)
