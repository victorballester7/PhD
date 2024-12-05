import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Define beta parameter
m = 0
beta = 2 * m / (m + 1)  # Modify as needed

sweep = 30
sweep_rad = np.deg2rad(sweep)
Ut = 1.0
Uinf = Ut * np.cos(sweep_rad)
Winf = Ut * np.sin(sweep_rad)


# Define the system of ODEs
def odes(x, y):
    y1, y2, y3, y4, y5 = y
    dy1_dx = y2
    dy2_dx = y3
    dy3_dx = -y1 * y3 - beta * (1 - y2**2)
    dy4_dx = y5
    dy5_dx = -y1 * y5
    return np.vstack((dy1_dx, dy2_dx, dy3_dx, dy4_dx, dy5_dx))


# Define the boundary conditions
def bc(ya, yb):
    return np.array(
        [
            ya[0],  # y1(0) = f(0) = 0
            ya[1],  # y2(0) = f'(0) = 0
            ya[3],  # y4(0) = g(0) = 0
            yb[1] - 1,  # y2(inf) = f'(inf) = 1
            yb[3] - 1,  # y4(inf) = g(inf) = 1
        ]
    )


# Initial mesh and guess
eta_max = 9
N = 50
x = np.linspace(0, eta_max, N)  # Extend to large x for "infinity"
y_guess = np.zeros((5, x.size))
y_guess[1, :] = 1  # Approximate guess for f'(x)

# Solve the BVP
solution = solve_bvp(odes, bc, x, y_guess)

# Check if the solution was successful
if solution.success:
    print("BVP solved successfully!")
else:
    print("BVP solution failed.")

# Plot the results
x_plot = np.linspace(0, eta_max, 200)
y_plot = solution.sol(x_plot)

# interpolate with polynomial of order p, the solutions y_plot[1] and y_plot[3]
p = 8
coeffs_f = np.polyfit(x_plot, y_plot[1], p)
coeffs_g = np.polyfit(x_plot, y_plot[3], p)

for i,coeff in enumerate(coeffs_f):
    print("<p> c"+str(i)+"_u","=",coeff,"</p>")


for i,coeff in enumerate(coeffs_g):
    print("<p> c"+str(i)+"_w","=",coeff,"</p>")
# plot the solutions


plt.figure(figsize=(10, 6))
plt.plot(Uinf * y_plot[1], x_plot, label=r"$Uinf*f'(x)$")
plt.plot(Winf * y_plot[3], x_plot, label=r"$Winf*g(x)$")
plt.plot(Uinf * np.polyval(coeffs_f, x_plot), x_plot, label=r"$Uinf*f'(x)$ polyfit")
plt.plot(Winf * np.polyval(coeffs_g, x_plot), x_plot, label=r"$Winf*g(x)$ polyfit")
plt.xlabel("x")
plt.ylabel("Solution")
plt.title("Solution of Coupled BVP")
plt.legend()
plt.grid()
plt.show()
