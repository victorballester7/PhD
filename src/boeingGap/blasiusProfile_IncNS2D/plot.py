import matplotlib.pyplot as plt
import numpy as np

def plot(x, xlarge, y, ufit, vfit, coeffs_u, coeffs_v,ufit_large, vfit_large, uinf, re_x):
    # plot the solutions
    fitted_poly_u = np.poly1d(np.hstack([coeffs_u, 0]))  # Add 0 for the constant term
    fitted_poly_v = np.poly1d(np.hstack([coeffs_v, 0]))  # Add 0 for the constant term

    u = uinf * y[1]
    u_polyaprox = uinf * fitted_poly_u(x)
    u_aprox = uinf * ufit

    v = 0.5 * uinf / np.sqrt(re_x) * (x * y[1] - y[0])
    v_polyaprox = 0.5 * uinf / np.sqrt(re_x) * fitted_poly_v(x)
    v_aprox = 0.5 * uinf / np.sqrt(re_x) * vfit

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
    ax1.axvline(uinf, color="black", linestyle="--")

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
    ax2.axvline(0.5 * uinf / np.sqrt(re_x) * 1.7207876389249748, color="gray", linestyle="--")

    # Add a legend
    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")
    plt.grid()
    plt.show()


