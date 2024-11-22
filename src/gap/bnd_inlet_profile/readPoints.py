# THIS SCRIPT JUST CONVERTS THE POINTS FROM A SIMULATION OF GANLIN FROM A FIXED SWEPT ANGLE TO A CUSTOM ONE.

# The value m (in his thesis), which attains for the power law u_e(x)=U_oo * (x-x_0)^m, outside the boudnary layer, is m = 0.

# Change the value of the variable swept_new and the script will return a .xml file to use directly for nektar fieldconvert.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Read points from text file


def read_points(path : str):
    df = pd.read_csv(path, header= None,sep=r"\s+")
    return df.to_numpy()

m = 300
# plot 0-1 and 0-2
def plot_points(L):
    l=len(L)
    print(l)
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    # plot with aspect ratio 1 in the axes
    ax.plot(L[:m,0],L[:m,1], 'r')
    ax.plot(L[:m,0],L[:m,3], 'b')
    plt.show()

L=read_points("points.txt")

swept_old=60
swept_new=30

swept_old_rad=swept_old*np.pi/180
swept_new_rad=swept_new*np.pi/180

L[:,1]=L[:,1]*np.cos(swept_new_rad)/np.cos(swept_old_rad)
L[:,3]=L[:,3]*np.sin(swept_new_rad)/np.sin(swept_old_rad)

plot_points(L)

# fit curves with taylor series expansion of power laws until p=8
pmax=8
x=L[:,0]
u=L[:,1]
w=L[:,3]

# fit u
A=np.zeros((len(x),pmax))
for i in range(pmax):
    A[:,i]=x**i
coeffs_u=np.linalg.lstsq(A,u,rcond=None)[0]

# fit w
A=np.zeros((len(x),pmax))
for i in range(pmax):
    A[:,i]=x**i
coeffs_w=np.linalg.lstsq(A,w,rcond=None)[0]

# plot the fits
x_fit=np.linspace(0,1,100)
u_fit=np.zeros(100)
w_fit=np.zeros(100)
for i in range(pmax):
    u_fit+=coeffs_u[i]*x_fit**i
    w_fit+=coeffs_w[i]*x_fit**i

fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
# plot with aspect ratio 1 in the axes
m = 300
ax.plot(L[:m,0],L[:m,1], 'r')
ax.plot(L[:m,0],L[:m,3], 'b')
ax.plot(x_fit,u_fit, 'r--')
ax.plot(x_fit,w_fit, 'b--')
plt.show()



# # Output file path
# file_path = "bnd_inflow_sweep" + str(swept_new) + ".pts"

# # Writing the file
# with open(file_path, "w") as file:
#     # Write header
#     file.write('<?xml version="1.0" encoding="utf-8"?>\n')
#     file.write('<NEKTAR>\n')
#     file.write('  <POINTS DIM="1" FIELDS="u,v,w,p">\n\n')

#     # Write data
#     for row in L:
#         file.write("    " + "  ".join(f"{value:.8e}" for value in row) + "\n")
#     
#     # Write footer
#     file.write('\n  </POINTS>\n')
#     file.write('</NEKTAR>\n')

# print(f"File '{file_path}' has been created.")


