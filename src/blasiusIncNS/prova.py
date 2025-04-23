import numpy as np
import matplotlib.pyplot as plt

# Constants
Uinf = 1
deltaStar_le = 1
Re_deltaStar_le = 1000
a = 1.7207876575203542
lengthBeforeGap = 50

# Derived constants
Kinvis = Uinf * deltaStar_le / Re_deltaStar_le
deltaStar_BC = np.sqrt(1 - lengthBeforeGap * a**2 / Re_deltaStar_le)
Re_deltaStar_BC = Uinf * deltaStar_BC / Kinvis
eta_99 = 4.910287765963463
delta_BC = deltaStar_BC * eta_99 / a
y2eta = eta_99 / delta_BC
etaMax = 9.84
yMax = etaMax / y2eta
Re_x_BC = (Re_deltaStar_BC / a) ** 2
Vinf = 0.5 * Uinf / np.sqrt(Re_x_BC)

# Coefficients
a_u = [0, 0.33263899291846005, 8830.512069032215, 58.97366593890366, 615.0518197268191, 32.12385528953152, -17.16678907227338, 11.02175978217767, -1.9645118354438575, 0.5010442307141161, -0.0645796009748346, 0.006179765415827125]
b_u = [0, 26593.41072503167, 176.8055649980844, 1855.7665505833227, 272.5391794254054, -39.221863541559394, 36.24230326537252, -0.07795052580215707, -0.8421866779902756, 0.44410766209840075, -0.06341415789453857, 0.006179765415827125]
a_v = [0, -1.9959025216159896e-05, 0.16695529626584846, -0.575204509312059, -0.4341004660550698, 299.3706050451578, -93.83786038348894, 16.266365937513303, -1.8990540751356129, 0.33729889822536685, -0.04383523593037588, 0.0034080097149121807]
b_v = [0, -3.380409827085182, -3.1753939961101696, 1805.0761851180248, -569.1055835320207, 102.77873382853763, 4.5614994586104824, -2.027219234693251, -0.01875987489840645, 0.1441683101478324, -0.024466672927746642, 0.0019804940487676533]

# Polynomial evaluation
def rational_poly(y, a_coeffs, b_coeffs):
    powers = np.array([y**i for i in range(1, 12)])
    num = sum(a * p for a, p in zip(a_coeffs[1:], powers))
    den = 1 + sum(b * p for b, p in zip(b_coeffs[1:], powers))
    return num / den

print(yMax)
Vinf = Uinf
# u and v definitions
def u(y):
    val = y * y2eta
    if y < yMax:
        return Uinf * rational_poly(val, a_u, b_u)
    else:
        val = yMax * y2eta
        return Uinf * rational_poly(val, a_u, b_u)

def v(y):
    val = y * y2eta
    if y < yMax:
        return Vinf * rational_poly(val, a_v, b_v)
    else:
        val = yMax * y2eta
        return Vinf * rational_poly(val, a_v, b_v)

# Vectorized versions
y_vals = np.linspace(0, 75, 1000)
u_vals = np.vectorize(u)(y_vals)
v_vals = np.vectorize(v)(y_vals)

# Plotting
plt.figure(figsize=(10, 5))
aux=np.dstack((y_vals, u_vals[-1] - u_vals, v_vals[-1] - v_vals))
# Print full array
np.set_printoptions(threshold=np.inf)
print(aux)
plt.plot(u_vals, y_vals, label='u(y)', color='blue')
plt.plot(v_vals, y_vals, label='v(y)', color='red')
plt.xlabel('y')
plt.ylabel('Velocity')
plt.title('Velocity Profiles u(y) and v(y)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

