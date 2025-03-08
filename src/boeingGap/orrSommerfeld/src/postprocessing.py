import numpy as np
import matplotlib.pyplot as plt

def printEVSorted(EVvariable, maxEVs=10):
    idx = np.argsort(EVvariable.imag)
    EVvariable = EVvariable[idx]
    for i in range(min(maxEVs, len(EVvariable))):
        print(f"EV {i}: {EVvariable[-i - 1].real}    {EVvariable[-i - 1].imag}i")
    print("...")


def getMostUnstableEV(EVvariable, vv):
    i = np.argmax(EVvariable.imag)
    return EVvariable[i], vv[:, i]


def printSpectrum(EVvariable, EVlabel):
    plt.plot(EVvariable.real, EVvariable.imag, "ob", markersize=5)
    plt.xlabel(f"{EVlabel}_r")
    plt.ylabel(f"{EVlabel}_i")
    xmin = np.max(np.array([np.min(EVvariable.real), -10]))
    xmax = np.min(np.array([np.max(EVvariable.real), 10]))
    ymin = np.max(np.array([np.min(EVvariable.imag), -0.4]))
    ymax = np.min(np.array([np.max(EVvariable.imag), 1]))

    eps = 0.03

    plt.xlim([xmin, xmax])
    plt.ylim([ymin - eps, ymax + eps])
    # plt.xlim([-0.2, 1])
    # plt.ylim([-1, 0.1])
    plt.grid()
    plt.show()

def printEVector(y_cheb, vv):
    plt.plot(vv.real, y_cheb, label="real")
    plt.plot(vv.imag, y_cheb, label="imag")
    plt.xlabel("v")
    plt.ylabel("y")
    plt.legend()
    plt.show()


