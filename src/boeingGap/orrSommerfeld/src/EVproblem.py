import numpy as np
import scipy.linalg as scla
import dmsuite

def Real2Cheb(a, b, f):
    return 2. / (b - a) * f - (b + a) * 1. / (b - a)

def Cheb2Real(a, b, f):
    return (b - a) / 2. * f + (b + a) / 2.

def adjustCoordinates(y_cheb, D, D2, D4, a, b):
    y_cheb = Cheb2Real(a, b, y_cheb)
    jac = 2. / (b - a)
    D = D * jac
    D2 = D2 * jac**2
    D4 = D4 * jac**4
    return y_cheb, D, D2, D4

def interpolateCheb(y, y_cheb, U, U_yy):
    # a = y[0]
    # b = y[-1]
    # y_toCheb = Real2Cheb(a, b, y)
    # U_toCheb = Real2Cheb(a, b, U)
    # U_yy_toCheb = Real2Cheb(a, b, U_yy)
    U = np.interp(y_cheb, y, U)
    U_yy = np.interp(y_cheb, y, U_yy)
    return U, U_yy

def getChebMatrices(N):
    y_cheb, D = dmsuite.chebdif(N, 1)
    D = D[0, :, :]
    D2 = D @ D
    D4 = D2 @ D2
    return y_cheb, D, D2, D4

def getOSMatrices(N, Re, alpha, D, D2, D4, U, U_yy):
    id = np.identity(N)

    # Orr-Sommerfeld eigenvalue problem:
    # L * v = omega * (M * v)
    L = (D4 - 2 * D2 * alpha**2 + id * alpha**4) / Re + 1j * alpha * (
        np.diag(U_yy) - np.diag(U) @ (D2 - id * alpha**2)
    )
    M = -1j * (D2 - id * alpha**2)

    # Apply boundary conditions:
    # v_tilde(0) = 0
    # v_tilde(N) = 0
    # v_tilde_diff(0) = 0
    # v_tilde_diff(N) = 0

    # move the eigenvalues of the BC to Q
    Q = -9999j
    # two homogeneous Dirichlet conditions
    L[0, :] = Q * id[0, :]
    M[0, :] = id[0, :]
    L[-1, :] = Q * id[-1, :]
    M[-1, :] = id[-1, :]

    # two homogeneous Neumann conditions
    L[1, :] = Q * D[0, :]
    M[1, :] = D[0, :]
    L[-2, :] = Q * D[-1, :]
    M[-2, :] = D[-1, :]
    return L, M


def solveEVproblem(L, M, alpha):
    omega, vv = scla.eig(L, M)
    c = omega / alpha
    return omega, c, vv

