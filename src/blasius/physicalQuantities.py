import numpy as np

# BL thickness
def computeDelta(x, y, incNS):
    # thinkness boundary layer (as first index of x_plot such that y_plot[1] > 0.99)
    fprime = y[1]
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
def computeDeltaStar(x, y, incNS):
    # to compute deltaStar, we need to integrate [1 - rho * u / (rhoInf * uInf)] from 0 to infinity (actually till etamax, as approximated)
    # in the incNS setting this means integrating (1-y[1]) from 0 to infinity (actually till etamax, as approximated)
    # in the comNS setting this means integrating (1-y[1]/y[3]) from 0 to infinity (actually till etamax, as approximated)

    # deltaStar = quad(lambda x: 1 - np.polyval(coeffs_fprime, x), 0, eta_max)[0]
    # print("deltaStar = ", deltaStar)
    # use numpy to compute the integral (they are basically the same, around 1e-7 difference for N = 10000)
    # deltaStar = np.trapezoid(1 - fprime, x)
    # print("deltaStar = ", deltaStar)

    # exact value is (eta - f(eta))|_0^inf = lim_{eta->inf} eta - f(eta) + f(0) = lim_{eta->inf} eta - f(eta)
    if incNS:
        f = y[0]
        deltaStar = x[-1] - f[-1]
    else:
        f = y[0]
        g = y[3]
        deltaStar = np.trapezoid(g , x) - f[-1]
    return deltaStar


# momentum thickness
def computeTheta(x, y, incNS):
    # to compute theta, we need to integrate [rho * u / (rhoInf * uInf) * (1 - u / uInf)] from 0 to infinity (actually till etamax, as approximated)
    # in th incNS setting this means integrating y[1](1-y[1]) from 0 to infinity (actually till etamax, as approximated)
    # in the comNS setting this means integrating y[1] / y[3] * (1 - y[1]) from 0 to infinity (actually till etamax, as approximated)
    fprime = y[1]
    theta = np.trapezoid(fprime * (1 - fprime), x)
    return theta


def getRe_x(Re_deltaStar_x, C):
    return (Re_deltaStar_x / C) ** 2


def toEta(y, C, deltaStar_x):
    """
    Convert y to eta using the given parameters.
    """
    return y * C / deltaStar_x
