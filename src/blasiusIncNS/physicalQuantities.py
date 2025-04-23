import numpy as np

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
def computeDeltaStar(x, f):
    # to compute deltaStar, we need to integrate (1-y[1]) from 0 to infinity (actually till etamax, as approximated)
    # deltaStar = quad(lambda x: 1 - np.polyval(coeffs_fprime, x), 0, eta_max)[0]
    # print("deltaStar = ", deltaStar)
    # use numpy to compute the integral (they are basically the same, around 1e-7 difference for N = 10000)
    # deltaStar = np.trapezoid(1 - fprime, x)
    # print("deltaStar = ", deltaStar)

    # exact value is (eta - f(eta))|_0^inf = lim_{eta->inf} eta - f(eta) + f(0) = lim_{eta->inf} eta - f(eta)
    deltaStar = x[-1] - f[-1]
    return deltaStar


# momentum thickness
def computeTheta(fprime, x):
    # to compute theta, we need to integrate f'(1-f') from 0 to infinity (actually till etamax, as approximated)
    theta = np.trapezoid(fprime * (1 - fprime), x)
    return theta

def getRe_x(Re_deltaStar_x, C):
    return (Re_deltaStar_x / C) ** 2

def toEta(y, C, deltaStar_x):
    """
    Convert y to eta using the given parameters.
    """
    return y * C / deltaStar_x
