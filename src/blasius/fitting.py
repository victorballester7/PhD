import numpy as np
from scipy.optimize import curve_fit


def fitting(x, y, func_u, func_v, p, lenParams, limit_u, limit_v):
    p0 = np.ones(lenParams)   # initial guess for the coefficients

    def u_fit_scipy(eta, *params):
        return func_u(eta, p, limit_u, *params)  # Add return here

    def v_fit_scipy(eta, *params):
        return func_v(eta, p, limit_v, *params)  # Add return here

    ufit_coeffs, _ = curve_fit(u_fit_scipy, x, y[1], p0=p0)
    vfit_coeffs, _ = curve_fit(v_fit_scipy, x, x * y[1] - y[0], p0=p0)

    printCoeffs(ufit_coeffs, vfit_coeffs, p, limit_u, limit_v)

    ufit = func_u(x, p, limit_u, *ufit_coeffs)
    vfit = func_v(x, p, limit_v, *vfit_coeffs)

    return ufit, vfit


# rational function for f'
def u_fit(eta, p, limit_u, *params):
    num = sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = (
        1
        + sum(params[p + j] * eta ** (j + 1) for j in range(p - 1))
        + params[p - 1] / limit_u * eta**p
    )  # we impose that the function is 1 at infinity
    return num / den


# rational function for x f' - f
def v_fit(eta, p, limit_v, *params):
    num = sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = (
        1
        + sum(params[p + j] * eta ** (j + 1) for j in range(p - 1))
        + params[p - 1] / limit_v * eta**p
    )  # we impose that the function is 1 at infinity
    return num / den


def u_fit_exp(eta, p, limit_u, *params):
    num = limit_u + sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = 1 + sum(
        params[p + j] * eta ** (j + 1) for j in range(p)
    )  # we impose that the function is 1 at infinity
    return limit_u - num / den * np.exp(-eta * params[2 * p])


# rational function for x f' - f
def v_fit_exp(eta, p, limit_v, *params):
    num = limit_v + sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = 1 + sum(
        params[p + j] * eta ** (j + 1) for j in range(p)
    )  # we impose that the function is 1 at infinity
    return limit_v - num / den * np.exp(-eta * params[2 * p])


def printCoeffs(coeffs_u, coeffs_v, p, limit_u, limit_v):
    # for rational function
    for i, coeff in enumerate(coeffs_u):
        if i < p:
            print("<p> a" + str(i + 1) + "_u", "=", coeff, "</p>")
        else:
            print("<p> b" + str(i - p + 1) + "_u", "=", coeff, "</p>")
    print("<p> b" + str(p) + "_u", "=", coeffs_u[p - 1] / limit_u, "</p>")

    for i, coeff in enumerate(coeffs_v):
        if i < p:
            print("<p> a" + str(i + 1) + "_v", "=", coeff, "</p>")
        else:
            print("<p> b" + str(i - p + 1) + "_v", "=", coeff, "</p>")
    print("<p> b" + str(p) + "_v", "=", coeffs_v[p - 1] / limit_v, "</p>")
