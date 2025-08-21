import numpy as np
import physicalQuantities as pq

def filter_out(x, y, ufit, vfit, x_limit):
    # Filter out the values where x is greater than x_limit
    idx = np.where(x < x_limit)[0]
    x = x[idx]
    y = y[:, idx]
    ufit = ufit[:, idx]
    vfit = vfit[:, idx]
    return x, y, ufit, vfit


def writeSol2File(x, y, filename, max_x, param):
    re_x = pq.getRe_x(param.re_deltaStar, param.deltaStar)

    # normalize x so that delta* = 1
    x_norm = x / param.deltaStar
    with open(filename, "w") as f:
        f.write(
            "# Blasius solution at Re_deltaStar = "
            + str(param.re_deltaStar)
            + " and using deltaStar = 1\n"
        )
        f.write("# y u v u_y u_yy\n")
        for i in range(len(x)):
            if x[i] > max_x:
                break

            u = y[1][i]
            u_y = y[2][i]
            u_yy = -y[0][i] * y[2][i] / 2
            v = 0.5 * param.uinf / np.sqrt(re_x) * (x[i] * y[1][i] - y[0][i])
            f.write(f"{x_norm[i]} {u} {v} {u_y} {u_yy}\n")

        if x[-1] < max_x:
            dx = x[-1] - x[-2]
            xnew = x[-1]
            u = y[1][-1]
            u_y = y[2][-1]
            u_yy = -y[0][-1] * y[2][-1] / 2
            v = 0.5 * param.uinf / np.sqrt(re_x) * (x[-1] * y[1][-1] - y[0][-1])
            while xnew < max_x:
                xnew += dx
                f.write(f"{xnew} {u} {v} {u_y} {u_yy}\n")



