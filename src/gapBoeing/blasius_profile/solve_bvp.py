import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

Uinf = 1.0
dim_system = 3

# Define the system of ODEs
def odes(x, y):
    y1, y2, y3 = y
    dy1_dx = y2
    dy2_dx = y3
    dy3_dx = -0.5 * y1 * y3 
    return np.vstack((dy1_dx, dy2_dx, dy3_dx))


# Define the boundary conditions
def bc(ya, yb):
    return np.array(
        [
            ya[0],  # y1(0) = f(0) = 0
            ya[1],  # y2(0) = f'(0) = 0
            yb[1] - 1,  # y2(inf) = f'(inf) = 1
        ]
    )


# Initial mesh and guess
eta_max = 9
N = 50
x = np.linspace(0, eta_max, N)  # Extend to large x for "infinity"
y_guess = np.zeros((dim_system, x.size))
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

aux = np.abs(y_plot[1] - 0.99)
idx = np.where(aux == np.min(aux))[0]
if y_plot[1][idx] < 0.99:
    idx1 = idx
    idx2 = idx + 1
else:
    idx1 = idx - 1
    idx2 = idx

# we take the BL thickness delta as a mean of the two closest points to 0.99
L = y_plot[1][idx2] - y_plot[1][idx1] # which is > 0
d1 = 0.99 - y_plot[1][idx1]
d2 = L - d1
delta = ((d1 * x_plot[idx2] + d2 * x_plot[idx1]) / L)[0]

# thinkness boundary layer (as first index of x_plot such that y_plot[1] > 0.99)
print("delta = ", delta)


# interpolate with polynomial of order p, the solutions y_plot[1] and y_plot[3]
p = 8
coeffs_f = np.polyfit(x_plot, y_plot[1], p)

for i,coeff in enumerate(coeffs_f):
    print("<p> c"+str(i)+"_u","=",coeff,"</p>")


# plot the solutions

plt.figure(figsize=(10, 6))

# u plot
plt.plot(Uinf * y_plot[1], x_plot, label=r"$Uinf*f'(x)$")
plt.plot(Uinf * np.polyval(coeffs_f, x_plot), x_plot, label=r"$Uinf*f'(x)$ polyfit")\

# v plot
# plt.plot(0.5 * (x_plot * y_plot[1] - y_plot[0]), x_plot, label=r"$0.5 * \sqrt{Uinf * \nu} * (x * f'(x) - f(x))$")

plt.xlabel("x")
plt.ylabel("Solution")
plt.title("Solution of Coupled BVP")
plt.legend()
plt.grid()
plt.show()
