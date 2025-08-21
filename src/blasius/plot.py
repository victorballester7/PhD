import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
import physicalQuantities as pq
from scipy.integrate import cumulative_trapezoid


def read_data(filename):
    data = np.loadtxt(filename, skiprows=3)

    y = data[:, 1]
    u = data[:, 2]
    v = data[:, 3]

    return y, u, v


def plot(x, y, incNS, ufit, vfit, plot_dns, x_eq_L, path_dns, param):
    # plot the solutions
    C = param.deltaStar

    re_x = pq.getRe_x(param.re_deltaStar, C)
    u_approx = []
    v_approx = []
    for uft, vft in zip(ufit, vfit):
        u_approx.append(param.uinf * uft)
        v_approx.append(0.5 * param.uinf / np.sqrt(re_x) * vft)
    u = param.uinf * y[1]

    v = (
        x * y[1] - y[0]
        if incNS
        else y[1] * cumulative_trapezoid(y[3], x, initial=0) - y[0] * y[3]
    )

    v *= 0.5 * param.uinf / np.sqrt(re_x)

    diffU = param.uinf * y[2]
    diffV = x *y[2] if incNS else y[2] * cumulative_trapezoid(y[3], x, initial=0) - y[0] * y[4]
    diffV *= 0.5 * param.uinf / np.sqrt(re_x)
    
    # Create the figure and the primary axis
    fig, ax1 = plt.subplots()
    plt.grid()
    fig, axdiff1 = plt.subplots()
    plt.grid()

    # Plot u with the first axis
    ax1.plot(u, x, label=r"u exact")
    ax1.axvline(param.uinf, color="black", linestyle="--")
    ax1.set_xlabel(r"$U_\infty f'(x)$")

    ax2 = ax1.twiny()
    ax2.plot(v, x, label=r"v exact", linestyle="dashdot")
    ax2.axvline(0.5 * param.uinf / np.sqrt(re_x) * C, color="gray", linestyle="--")
    ax2.set_xlabel(r"$0.5  U_\infty / \sqrt{Re_x}  (x f'(x) - f(x))$")

    # Plot diff u in the second figure
    axdiff1.plot(diffU, x, label="u' exact")
    axdiff1.axvline(0, color="black", linestyle="--")
    axdiff1.set_xlabel("u'")

    axdiff2 = axdiff1.twiny()
    axdiff2.plot(diffV,x,label="v' exact", linestyle="dashdot")
    axdiff2.set_xlabel("v'")

    Unormoo, diffUnormoo = la.norm(u, np.inf), la.norm(diffU, np.inf)
    Vnormoo, diffVnormoo = la.norm(v, np.inf), la.norm(diffV, np.inf)
    UnormC1 = Unormoo + diffUnormoo
    VnormC1 = Vnormoo + diffVnormoo
    print("||u||_C1 = ||u||_oo + ||u'||_oo")
    print("||u||_oo  = ", Unormoo)
    print("||u'||_oo = ", diffUnormoo)
    print("||u||_C1  = ", UnormC1)
    print("||v||_oo  = ", Vnormoo)
    print("||v'||_oo = ", diffVnormoo)
    print("||v||_C1  = ", VnormC1)
    for i, (u_apx, v_apx) in enumerate(zip(u_approx, v_approx)):
        errUoo = la.norm(u - u_apx, np.inf)
        errVoo = la.norm(v - v_apx, np.inf)
        
        
        diffUapx = np.gradient(u_apx, x)
        diffVapx = np.gradient(v_apx, x)
        # diffVapx = x * diffUapx
        # diffVapx *= 0.5 * param.uinf / np.sqrt(re_x)

        errdiffUoo = la.norm(diffU - diffUapx, np.inf)
        errdiffVoo = la.norm(diffV - diffVapx, np.inf)

        argmax = np.argmax(np.abs(diffU - diffUapx))
        print("max of error diffU: ", x[argmax])
        argmax = np.argmax(np.abs(diffV - diffVapx))
        print("max of error diffV: ", x[argmax])


        print(
            f"||u - u_aprox_{i}||_oo / ||u||_oo    = ",
            errUoo / Unormoo            
        )
        print(
            f"||v - v_aprox_{i}||_oo / ||v||_oo    = ",
            errVoo / Vnormoo
        )
        print(
            f"||u' - u_aprox_{i}'||_oo / ||u'||_oo = ",
            errdiffUoo / diffUnormoo
        )
        print(
            f"||v' - v_aprox_{i}'||_oo / ||v'||_oo = ",
            errdiffVoo / diffVnormoo
        )
        
        print(
            f"||u - u_aprox_{i}||_C1 / ||u||_C1    = ",
                (errUoo + errdiffUoo) / UnormC1
        )
        print(
            f"||v - v_aprox_{i}||_C1 / ||v||_C1    = ",
                (errVoo + errdiffVoo) / VnormC1
        )


        ax1.plot(u_apx, x, label=f"u fit_{i}")
        ax2.plot(v_apx, x, label=f"v fit_{i}", linestyle="dashdot")

        axdiff1.plot(diffUapx, x, label=f"u' fit_{i}")
        axdiff2.plot(diffVapx, x, label=f"v' fit_{i}", linestyle="dashdot")

    eps = 0.05
    x1_min = 0
    x1_max = u[-1]
    x1_min -= eps * (x1_max - x1_min)
    x1_max += eps * (x1_max - x1_min)
    ax1.set_xlim(x1_min, x1_max)

    x2_min = 0
    x2_max = v[-1]
    x2_min -= eps * (x2_max - x2_min)
    x2_max += eps * (x2_max - x2_min)
    ax2.set_xlim(x2_min, x2_max)

    if not incNS:
        # plot Temperature as well
        T = y[3]
        ax1.plot(T, x, label=r"$T$ exact")

    if not plot_dns:
        # Add a legend
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        axdiff1.legend(loc="upper left")
        axdiff2.legend(loc="upper right")
        plt.show()
        return

    # data from dns
    x_dns, u_dns, v_dns = read_data(path_dns)
    deltaStar_at_x_eq_L = np.sqrt(1 + x_eq_L * C**2 / param.re_deltaStar)
    Re_deltaStar_at_x_eq_L = (
        param.uinf * deltaStar_at_x_eq_L / (1.0 / param.re_deltaStar)
    )

    Re_x_at_x_eq_L = pq.getRe_x(Re_deltaStar_at_x_eq_L, C)
    print("Re_x_BC = ", Re_x_at_x_eq_L)
    print("deltaStar_BC = ", deltaStar_at_x_eq_L)
    factor = np.sqrt(Re_x_at_x_eq_L) / np.sqrt(re_x)

    # interpolate to x
    x_dns = pq.toEta(x_dns, C, deltaStar_at_x_eq_L)

    # aux =np.dstack((x_dns, u_dns))
    # # print full array
    # np.set_printoptions(threshold=np.inf)
    # print(aux)
    u_dns = np.interp(x, x_dns, u_dns)
    v_dns = np.interp(x, x_dns, v_dns * factor)

    # Plot the DNS data
    ax1.plot(u_dns, x, label="u DNS", color="red")
    ax2.plot(v_dns, x, label="v DNS", color="red")
    print(
        "||u - u_aprox_dns||_oo / ||u||_oo = ",
        la.norm(u - u_dns, np.inf) / la.norm(u, np.inf),
    )
    print(
        "||v - v_aprox_dns||_oo / ||v||_oo = ",
        la.norm(v - v_dns, np.inf) / la.norm(v, np.inf),
    )

    # Add a legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    axdiff1.legend(loc="upper left")
    axdiff2.legend(loc="upper right")
    plt.show()


def plot_comNS(x, y, fits, plot_dns, x_eq_L, path_dns, param):
    rho_fit, rhou_fit, rhov_fit, E1_fit, E2_fit = fits

    # plot the solutions
    C = param.deltaStar

    re_x = pq.getRe_x(param.re_deltaStar, C)
    rho_approx = param.rhoinf * rho_fit
    rhou_approx = param.rhoinf * param.uinf * rhou_fit
    rhov_approx = 0.5 * param.rhoinf * param.uinf / np.sqrt(re_x) * rhov_fit
    E_approx = (
        param.rhoinf
        * param.uinf**2
        * (
            0.5 * E1_fit
            + 0.125 / np.sqrt(re_x) * E2_fit
            + 1.0 / ((param.gamma - 1) * param.gamma * param.Mainf**2)
        )
    )


    rho = param.rhoinf / y[3]
    rhou = param.rhoinf * param.uinf * y[1] / y[3]
    rhov = (
        0.5
        * param.rhoinf
        * param.uinf
        / np.sqrt(re_x)
        * (y[1] / y[3] * cumulative_trapezoid(y[3], x, initial=0) - y[0])
    )
    E = (
        param.rhoinf
        * param.uinf**2
        * (
            0.5 * y[1] ** 2 / y[3]
            + 0.125
            / np.sqrt(re_x)
            * (
                y[1] / np.sqrt(y[3]) * cumulative_trapezoid(y[3], x, initial=0)
                - np.sqrt(y[3]) * y[0]
            )
            ** 2
            + 1.0 / ((param.gamma - 1) * param.gamma * param.Mainf**2)
        )
    )
    E = E/ E[-1]  # normalize E
    E_approx = E_approx / E_approx[-1]  # normalize E_approx

    real = [rho, rhou, rhov, E]
    approx = [rho_approx, rhou_approx, rhov_approx, E_approx]
    labels = ["ρ", "ρu", "ρv", "E"]

    # Create the figure and the primary axis
    fig, ax1 = plt.subplots()

    # Plot u with the first axis
    ax1.plot(rho, x, label="ρ exact", color="orange")
    ax1.plot(rhou, x, label="u exact", color="blue")
    ax1.plot(E, x, label="E / lim E exact", color="purple")
    ax1.axvline(param.rhoinf * param.uinf, color="black", linestyle="--")
    ax1.set_xlabel("u")

    ax2 = ax1.twiny()
    ax2.plot(rhov, x, label="v exact", color="green")
    ax2.axvline(0.5 * param.uinf / np.sqrt(re_x) * C, color="gray", linestyle="--")
    ax2.set_xlabel("v")

    for real_val, approx_val, lab in zip(real, approx, labels):
        print(f"||{lab} - {lab}_approx||_oo / ||{lab}||_oo = {la.norm(real_val - approx_val, np.inf) / la.norm(real_val, np.inf)}")

    ax1.plot(rho_approx, x, label="ρ fit", color="orange", linestyle="dotted")
    ax1.plot(rhou_approx, x, label="u fit", color="blue", linestyle="dotted")
    ax2.plot(rhov_approx, x, label="v fit", color="green", linestyle="dotted")
    ax1.plot(E_approx, x, label="E / lim E fit", color="purple", linestyle="dotted")

    eps = 0.05
    x1_min = 0
    x1_max = rhou[-1]
    x1_min -= eps * (x1_max - x1_min)
    x1_max += eps * (x1_max - x1_min)
    ax1.set_xlim(x1_min, x1_max)

    x2_min = 0
    x2_max = rhov[-1]
    x2_min -= eps * (x2_max - x2_min)
    x2_max += eps * (x2_max - x2_min)
    ax2.set_xlim(x2_min, x2_max)

    # data from dns
    # x_dns, u_dns, v_dns = read_data(path_dns)
    # deltaStar_at_x_eq_L = np.sqrt(1 + x_eq_L * C**2 / param.re_deltaStar)
    # Re_deltaStar_at_x_eq_L = (
    #     param.uinf * deltaStar_at_x_eq_L / (1.0 / param.re_deltaStar)
    # )

    # Re_x_at_x_eq_L = pq.getRe_x(Re_deltaStar_at_x_eq_L, C)
    # print("Re_x_BC = ", Re_x_at_x_eq_L)
    # print("deltaStar_BC = ", deltaStar_at_x_eq_L)
    # factor = np.sqrt(Re_x_at_x_eq_L) / np.sqrt(re_x)

    # # interpolate to x
    # x_dns = pq.toEta(x_dns, C, deltaStar_at_x_eq_L)

    # # aux =np.dstack((x_dns, u_dns))
    # # # print full array
    # # np.set_printoptions(threshold=np.inf)
    # # print(aux)
    # u_dns = np.interp(x, x_dns, u_dns)
    # v_dns = np.interp(x, x_dns, v_dns * factor)

    # # Plot the DNS data
    # ax1.plot(u_dns, x, label="u DNS", color="red")
    # ax2.plot(v_dns, x, label="v DNS", color="red")
    # print(
    #     "||u - u_aprox_dns||_oo / ||u||_oo = ",
    #     la.norm(u - u_dns, np.inf) / la.norm(u, np.inf),
    # )
    # print(
    #     "||v - v_aprox_dns||_oo / ||v||_oo = ",
    #     la.norm(v - v_dns, np.inf) / la.norm(v, np.inf),
    # )

    # Add a legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.grid()
    plt.show()
    return
