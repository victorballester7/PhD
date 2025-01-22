import numpy as np
from scipy.integrate import solve_bvp, quad
import matplotlib.pyplot as plt

Uinf = 1.0
dim_system = 3
eta_max = 9
# Initial mesh and guess
N = 10000  # discretization
x = np.linspace(0, eta_max, N)  # Extend to large x for "infinity"


def solve_BVP(dim_system):
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
    y_guess[1, :] = 1  # Approximate guess for f'(x)

    # Solve the BVP
    solution = solve_bvp(odes, bc, x, y_guess)

    # Check if the solution was successful
    if solution.success:
        print("BVP solved successfully!")
    else:
        print("BVP solution failed.")

    return solution

# BL thickness
def computeDelta(fprime):
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
def computeDeltaStar(coeffs_fprime, f, fprime, eta_max):
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
def computeTheta(coeffs_fprime, eta_max):
    # to compute theta, we need to integrate f'(1-f') from 0 to infinity (actually till etamax, as approximated)
    theta = quad(lambda x: np.polyval(coeffs_fprime, x) * (1 - np.polyval(coeffs_fprime, x)), 0, eta_max)[0]
    return theta

def computeCoeffs(y, p):
    # interpolate with polynomial of order p, the solutions y_plot[1] and y_plot[3]
    coeffs_f = np.polyfit(x, y[1], p)
    for i, coeff in enumerate(coeffs_f):
        print("<p> c" + str(i) + "_u", "=", coeff, "</p>")

    return coeffs_f


def plot(y, coeffs_fprime, Uinf):
    # plot the solutions
    plt.figure(figsize=(10, 6))

    # u plot
    plt.plot(Uinf * y[1], x, label=r"$Uinf*f'(x)$")
    plt.plot(Uinf * np.polyval(coeffs_fprime, x), x, label=r"$Uinf*f'(x)$ polyfit")

    # v plot
    # plt.plot(0.5 * (x_plot * y_plot[1] - y_plot[0]), x_plot, label=r"$0.5 * \sqrt{Uinf * \nu} * (x * f'(x) - f(x))$")

    plt.xlabel("x")
    plt.ylabel("Solution")
    plt.title("Solution of Coupled BVP")
    plt.legend()
    plt.grid()
    plt.show()


solution = solve_BVP(dim_system)
# Take the results
y = solution.sol(x)

coeffs_fprime = computeCoeffs(y, 8)

delta = computeDelta(y[1])
deltaStar = computeDeltaStar(coeffs_fprime, y[0], y[1], eta_max)
theta = computeTheta(coeffs_fprime, eta_max)
shapeFactor = deltaStar / theta
print("delta        = ", delta, "* x / sqrt(Re_x)")
print("delta*       = ", deltaStar, "* x / sqrt(Re_x)")
print("theta        = ", theta, "* x / sqrt(Re_x)")
print("delta/delta* = ", delta / deltaStar)
print("H            = ", shapeFactor)

plot(y, coeffs_fprime, Uinf)
