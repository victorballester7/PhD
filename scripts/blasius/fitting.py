import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import cumulative_trapezoid
import scipy.linalg as la
import matplotlib.pyplot as plt


def fitting(x, y, incNS, p, limit_u, limit_v):
    lenParams = 2 * p - 1
    pu = np.ones(2 * p - 1)  # initial guess for the coefficients
    pv = np.ones(2 * p)  # initial guess for the coefficients

    # def u_fit_scipy(eta, *params):
    #     return u_fit_func(eta, p, limit_u, *params)  # Add return here

    # def v_fit_scipy(eta, *params):
    #     return v_fit_func(eta, p, limit_v, *params)  # Add return here

    f_tofit_u = y[1]
    f_tofit_v = (
        x * y[1] - y[0]
        if incNS
        else y[1] * cumulative_trapezoid(y[3], x, initial=0) - y[0] * y[3]
    )

    ufit_coeffs, _ = curve_fit(
        lambda eta, *params: u_fit_func(eta, p, limit_u, *params),
        x, 
        f_tofit_u, 
    p0=pu
    )
    # vfit_coeffs, _ = curve_fit(
    #     lambda eta, *params: u_fit_func(eta, p, limit_v, *params),
    #     x,
    #     f_tofit_v,
    #     p0=pu
    # )
    vfit_coeffs, _ = curve_fit(
        lambda eta, *params: v_fit_func(eta, p, limit_v, *params),
        x,
        f_tofit_v,
        p0=pv
    )

    if incNS:
        printCoeffs([ufit_coeffs, vfit_coeffs], p, [limit_u, limit_v])

    ufit = u_fit_func(x, p, limit_u, *ufit_coeffs)
    # vfit = u_fit_func(x, p, limit_v, *vfit_coeffs)

    ffit = cumulative_trapezoid(ufit, x, initial=0) 

    vfit = x * ufit - ffit

    return ufit, vfit


def fitting_comNS(x, y, p, limits, param):
    lenParams = 2 * p - 1
    p0 = np.ones(lenParams)  # initial guess for the coefficients

    limit_rho, limit_rhou, limit_rhov, limit_E1, limit_E2 = limits

    def rho_fit_scipy(eta, *params):
        return rho_fit_func(eta, p, limit_rho, *params)

    def rhou_fit_scipy(eta, *params):
        return u_fit_func(eta, p, limit_rhou, *params)

    def rhov_fit_scipy(eta, *params):
        return u_fit_func(eta, p, limit_rhov, *params)

    def E1_fit_scipy(eta, *params):
        return u_fit_func(eta, p, limit_E1, *params)

    def E2_fit_scipy(eta, *params):
        return u_fit_func(eta, p, limit_E2, *params)

    f_tofit_rho = 1 / y[3]
    f_tofit_rhou = y[1] / y[3]
    f_tofit_rhov = y[1] / y[3] * cumulative_trapezoid(y[3], x, initial=0) - y[0]
    # we split the energy equation into two parts:
    f_tofit_E1 = y[1] ** 2 / y[3]
    f_tofit_E2 = (
        y[1] / np.sqrt(y[3]) * cumulative_trapezoid(y[3], x, initial=0)
        - y[0] * np.sqrt(y[3])
    ) ** 2

    rho_fit_coeffs, _ = curve_fit(rho_fit_scipy, x, f_tofit_rho, p0=p0)
    rhou_fit_coeffs, _ = curve_fit(rhou_fit_scipy, x, f_tofit_rhou, p0=p0)
    rhov_fit_coeffs, _ = curve_fit(rhov_fit_scipy, x, f_tofit_rhov, p0=p0)
    E1_fit_coeffs, _ = curve_fit(E1_fit_scipy, x, f_tofit_E1, p0=p0)
    E2_fit_coeffs, _ = curve_fit(E2_fit_scipy, x, f_tofit_E2, p0=p0)

    y2eta_coeffs = approx_y2eta_comNS(x, y, param)

    printCoeffs_comNS(
        [
            rho_fit_coeffs,
            rhou_fit_coeffs,
            rhov_fit_coeffs,
            E1_fit_coeffs,
            E2_fit_coeffs,
            y2eta_coeffs,
        ],
        p,
        limits,
    )

    rho_fit = rho_fit_func(x, p, limit_rho, *rho_fit_coeffs)
    rhou_fit = u_fit_func(x, p, limit_rhou, *rhou_fit_coeffs)
    rhov_fit = u_fit_func(x, p, limit_rhov, *rhov_fit_coeffs)
    E1_fit = u_fit_func(x, p, limit_E1, *E1_fit_coeffs)
    E2_fit = u_fit_func(x, p, limit_E2, *E2_fit_coeffs)

    return rho_fit, rhou_fit, rhov_fit, E1_fit, E2_fit


# rational function for f' (both incNS and comNS)
def u_fit_func(eta, p, limit_u, *params):
    num = sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = (
        1
        + sum(params[p + j] * eta ** (j + 1) for j in range(p - 1))
        + params[p - 1] / limit_u * eta**p
    )  # we impose that the function is 1 at infinity
    return num / den


def v_fit_func(eta, p, limit_u, *params):
    num = sum(
        params[i] * eta ** (i + 2) for i in range(p)
    )  # we impose that the function and its first derivative are zero at the origin
    den = (
        1
        + sum(params[p + j] * eta ** (j + 1) for j in range(p))
        + params[p - 1] / limit_u * eta ** (p + 1)
    )  # we impose that the function is 1 at infinity
    return num / den


# rational function for f' (both incNS and comNS)
# def v_fit_func(eta, p, limit_u, *params):
#     num = sum(
#         params[i + 1] * eta ** (i + 2) for i in range(p - 1)
#     )  # we impose that the function and its first derivative are zero at the origin
#     den = (
#         1
#         + sum(params[p + j] * eta ** (j + 1) for j in range(p - 1))
#         + params[p - 1] / limit_u * eta**p
#     )  # we impose that the function is 1 at infinity
#     return num / den


def rho_fit_func(eta, p, limit_rho, *params):
    num = sum(
        params[i] * eta ** (i + 1) for i in range(p)
    )  # we impose that the function is zero at the origin
    den = 1 + sum(
        params[p + j] * eta ** (j + 1) for j in range(p - 1)
    )  # we impose that the function is 1 at infinity
    return limit_rho + num / den


def approx_y2eta_comNS(x, y, param):
    lenParams = 4
    p0 = np.ones(lenParams)  # initial guess for the coefficients

    deltaStar_inflow = np.sqrt(
        1 + param.x_inflow * param.deltaStar**2 / param.re_deltaStar
    )

    y_physical_inflow = (
        deltaStar_inflow / param.deltaStar * cumulative_trapezoid(y[3], x, initial=0)
    )

    def int_rho_fit(y, *params):
        a, b, alpha, beta = params
        return a + b * y + alpha * np.tanh(beta * y)

    f_tofit = cumulative_trapezoid(1 / y[3], y_physical_inflow, initial=0)

    fit_coeffs, _ = curve_fit(int_rho_fit, y_physical_inflow, f_tofit, p0=p0)

    print(f"Approximation of η(x,y) at x_inflow (x = {param.x_inflow}):")
    print(
        f"η(x_inflow,y) = {param.deltaStar / deltaStar_inflow} [ {fit_coeffs[0]} + {fit_coeffs[1]} * y + {fit_coeffs[2]} * tanh({fit_coeffs[3]} * y) ]"
    )

    # plot int_0^y rho dy
    xplot = y_physical_inflow
    yplot_real = cumulative_trapezoid(1 / y[3], y_physical_inflow, initial=0)
    yplot_fit = int_rho_fit(xplot, *fit_coeffs)

    print(f"|| int_0^y rho dy - fit ||_oo = {la.norm(yplot_real - yplot_fit, np.inf)}")

    plt.plot(xplot, yplot_real, label="real")
    plt.plot(xplot, yplot_fit, label="fit")
    plt.plot(xplot, xplot, label="y", linestyle="--")
    plt.xlabel("x")
    plt.ylabel("int_0^y rho dy")
    plt.grid()
    plt.legend()
    plt.show()

    return fit_coeffs


def printCoeffs(coeffs, p, limits):
    # for rational function
    labels = ["u", "v"]
    for coeff, limit, label in zip(coeffs, limits, labels):
        for i, c in enumerate(coeff):
            if i < p:
                print(f"<p> a{i + 1}_{label} = {c} </p>")
            else:
                print(f"<p> b{i - p + 1}_{label} = {c} </p>")
        print(f"<p> b{p}_{label} = {coeff[p - 1] / limit} </p>")


def printCoeffs_comNS(coeffs, p, limits):
    # for rational function
    labels = ["rho", "rhou", "rhov", "E1", "E2"]
    coeffs_y2eta = coeffs.pop()
    print("")  # extra space
    for coeffs, limit, label in zip(coeffs, limits, labels):
        for i, c in enumerate(coeffs):
            if i < p:
                print(f"      <p> a{i + 1}_{label} = {c} </p>")
            else:
                print(f"      <p> b{i - p + 1}_{label} = {c} </p>")
        if label == "rho":
            continue  # rho does not have the last bp coeff
        print(f"      <p> b{p}_{label} = {coeffs[p - 1] / limit} </p>")

    print("""    </PARAMETERS>

    <VARIABLES>
      <V ID="0"> rho  </V>
      <V ID="1"> rhou </V>
      <V ID="2"> rhov </V>
      <V ID="3"> E    </V>
    </VARIABLES>
     
    <BOUNDARYREGIONS>
      <B ID="0"> C[1] </B>    <!-- inlet !-->  
      <B ID="1"> C[2] </B>    <!-- outlet !-->
      <B ID="2"> C[3] </B>    <!-- top !-->
      <B ID="3"> C[4] </B>    <!-- bottom + left & right gap walls !-->
    </BOUNDARYREGIONS>    

    <BOUNDARYCONDITIONS>
      <REGION REF="0">  <!-- inlet !-->""")
    eta = (
        f"{coeffs_y2eta[0]}"
        f"{' + ' if coeffs_y2eta[1] >= 0 else ' - '}{abs(coeffs_y2eta[1])} * y"
        f"{' + ' if coeffs_y2eta[2] >= 0 else ' - '}{abs(coeffs_y2eta[2])} * tanh({coeffs_y2eta[3]} * y)"
    )
    for label in labels[:3]:
        freestreamLabel = f"{label}Inf"
        multiplierSign = " + " if label == "rho" else " * "
        lastRangeP = p - 1 if label == "rho" else p
        print(f"""        <D VAR="{label}" VALUE="{freestreamLabel}{multiplierSign}( 
                   (
                     ({" + ".join([f"a{i + 1}_{label}*({eta})^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_{label}*({eta})^{i + 1}" for i in range(lastRangeP)])})
                   ) * (y<yMax) + 
                   (
                     ({" + ".join([f"a{i + 1}_{label}*etaMax^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_{label}*etaMax^{i + 1}" for i in range(lastRangeP)])})
                   ) * (y>=yMax))" />""")

    # energy equation
    print(f"""        <D VAR="E" VALUE="E0Inf + E1Inf * (
                   (
                     ({" + ".join([f"a{i + 1}_E1*({eta})^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_E1*({eta})^{i + 1}" for i in range(p)])})
                   ) * (y<yMax) + 
                   (
                     ({" + ".join([f"a{i + 1}_E1*etaMax^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_E1*etaMax^{i + 1}" for i in range(p)])})
                   ) * (y>=yMax)) + E2Inf * (
                   (
                     ({" + ".join([f"a{i + 1}_E2*({eta})^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_E2*({eta})^{i + 1}" for i in range(p)])})
                   ) * (y<yMax) + 
                   (
                     ({" + ".join([f"a{i + 1}_E2*etaMax^{i + 1}" for i in range(p)])}) / 
                     (1 + {" + ".join([f"b{i + 1}_E2*etaMax^{i + 1}" for i in range(p)])})
                   ) * (y>=yMax))" />""")

    print("""      </REGION>""")
