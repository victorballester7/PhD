import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
from physicalQuantities import toEta, getRe_x


def read_data(filename):
    data = np.loadtxt(filename, skiprows=3)

    y = data[:, 1]
    u = data[:, 2]
    v = data[:, 3]

    return y, u, v


def plot(x, y, ufit, vfit, uinf, re_x, C):
    # plot the solutions

    u_approx = []
    v_approx = []
    for uft, vft in zip(ufit, vfit):
        u_approx.append(uinf * uft)
        v_approx.append(0.5 * uinf / np.sqrt(re_x) * vft)
    u = uinf * y[1]

    v = 0.5 * uinf / np.sqrt(re_x) * (x * y[1] - y[0])

    # Create the figure and the primary axis
    fig, ax1 = plt.subplots()

    # Plot u with the first axis
    ax1.plot(u, x, label=r"u exact")
    ax1.axvline(uinf, color="black", linestyle="--")
    ax1.set_xlabel(r"$U_\infty f'(x)$")

    ax2 = ax1.twiny()
    ax2.plot(v, x, label=r"v exact")
    ax2.axvline(0.5 * uinf / np.sqrt(re_x) * C, color="gray", linestyle="--")
    ax2.set_xlabel(r"$0.5  U_\infty / \sqrt{Re_x}  (x f'(x) - f(x))$")

    print("||u||_oo = ", la.norm(u, np.inf))
    print("||v||_oo = ", la.norm(v, np.inf))
    for i, (u_apx, v_apx) in enumerate(zip(u_approx, v_approx)):
        print(
            f"||u - u_aprox_{i}||_oo / ||u||_oo = ",
            la.norm(u - u_apx, np.inf) / la.norm(u, np.inf),
        )
        print(
            f"||v - v_aprox_{i}||_oo / ||v||_oo = ",
            la.norm(v - v_apx, np.inf) / la.norm(v, np.inf),
        )

        ax1.plot(u_apx, x, label=f"u fit_{i}")
        ax2.plot(v_apx, x, label=f"v fit_{i}")

    # data from dns
    length = 0

    x_dns, u_dns, v_dns = read_data(
        "../flatSurfaceRe1000IncNS/dns/changedformula_withHighOrderBC/data/points_x" + str(length) + ".dat"
    )

    Re_deltaStar = 1000
    deltaStar_lenght = np.sqrt(1 + length * C**2 / Re_deltaStar)
    Re_deltaStar_length = uinf * deltaStar_lenght / (1. / Re_deltaStar)

    Re_x_length = getRe_x(Re_deltaStar_length, C)
    print("Re_x_BC = ", Re_x_length)
    print("deltaStar_BC = ", deltaStar_lenght)
    factor = np.sqrt(Re_x_length) / np.sqrt(re_x)

    # interpolate to x
    x_dns = toEta(x_dns, C, deltaStar_lenght)

    aux =np.dstack((x_dns, u_dns))
    # print full array
    np.set_printoptions(threshold=np.inf)
    print(aux)
    u_dns = np.interp(x, x_dns, u_dns)
    v_dns = np.interp(x, x_dns, v_dns * factor)
    # x = x_dns

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
    plt.grid()
    plt.show()
