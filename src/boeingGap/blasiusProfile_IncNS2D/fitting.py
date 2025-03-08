import numpy as np

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
def u_fit(eta, p, limit_u, *params):
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
def v_fit(eta, p, limit_v, *params):
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

def plotCoeffs(coeffs_u, coeffs_v,p, limit_u, limit_v):
    # for rational function
    for i, coeff in enumerate(coeffs_u):
        if i < p:
            print("<p> a" + str(i+1) + "_u", "=", coeff, "g")
        else:
            print("<p> b" + str(i-p+1) + "_u", "=", coeff, "g")
    print("<p> b" + str(p) + "_u", "=", coeffs_u[p-1]/limit_u, "g")

    for i, coeff in enumerate(coeffs_v):
        if i < p:
            print("<p> a" + str(i+1) + "_v", "=", coeff, "g")
        else:
            print("<p> b" + str(i-p+1) + "_v", "=", coeff, "g")
    print("<p> b" + str(p) + "_v", "=", coeffs_v[p-1]/limit_v, "g")
