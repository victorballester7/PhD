import os
import numpy as np
from pp.inputargs import parseArgs
from pp.fileManagement import extract_width_depth, readDataHistoryPoints
import matplotlib.pyplot as plt
from pp.noiseDetector import NoiseDetector
from scipy.fft import rfft, irfft, rfftfreq
from scipy.interpolate import make_interp_spline


def main():
    args = parseArgs()
    folders = args.folders

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, folder in enumerate(folders):
        width, depth = extract_width_depth(folder)
        codename = f"d{depth}_w{width}"
        points, data = readDataHistoryPoints(folder)
        print(points.shape, data.shape)

        # pointref = 24 if i == 0 else 3
        # numPointsYdir = 9 if i == 0 else 1
        pointref = 25
        point = 322
        # numPointsYdir = 1
        X = []
        nx = []
        data_p = data[point]
        data_pref = data[pointref]

        t, u, v, p = data_p.transpose()
        t_ref, u_ref, v_ref, p_ref = data_pref.transpose()

        # u analysis
        # def doStuff(t, var, t_ref, var_ref):
        #     detector_u = NoiseDetector(t, var)
        #     t_0_detected_u, results_u = detector_u.detect_t0_robust(methods=['variance'])

        #     detector_u_ref = NoiseDetector(t_ref, var_ref)
        #     t_0_detected_u_ref, results_u_ref = detector_u_ref.detect_t0_robust(methods=['variance'])
        #     t0= np.max([t_0_detected_u, t_0_detected_u_ref])

        #     t, var = detector_u.filter_data(t0)
        #     t_ref, var_ref = detector_u_ref.filter_data(t0)

        #     # fft
        #     fft_var = rfft(var)
        #     freqs = rfftfreq(len(var), t[1] - t[0])
        #     fft_var_ref = rfft(var_ref)
        #     freqs_ref = rfftfreq(len(var_ref), t_ref[1] - t_ref[0])
        #     modulus_var = np.abs(fft_var)
        #     modulus_var_ref = np.abs(fft_var_ref)

        #     sorted_indices = np.argsort(fft_var)[::-1]
        #     sorted_indices = sorted_indices[:20]
        #     sorted_freqs = freqs[sorted_indices]
        #     sorted_freqs_ref = freqs_ref[sorted_indices]
        #     sorted_modulus_var = modulus_var[sorted_indices]
        #     sorted_modulus_var_ref = modulus_var_ref[sorted_indices]
        #     for i in range(len(sorted_freqs)):
        #         print(f"Frequency: {sorted_freqs[i]}, Modulus: {sorted_modulus_var[i]}, Frequency Ref: {sorted_freqs_ref[i]}, Modulus Ref: {sorted_modulus_var_ref[i]}")

        #     # print(f"fft_var: {fft_var.shape} {fft_var}")
        #     # print(f"fft_var_ref: {fft_var_ref.shape} {fft_var_ref}")

        #     # print(f"freqs_var: {freqs.shape} {freqs}")
        #     # print(f"freqs_var_ref:  {freqs_ref.shape} {freqs_ref}")

        #     quotient = np.log(sorted_modulus_var / sorted_modulus_var_ref)

        #     # sort frequencies by highest quotient
        #     sorted_indices = np.argsort(quotient)[::-1]
        #     sorted_freqs = freqs[sorted_indices]
        #     sorted_quotient = quotient[sorted_indices]
        #     sorted_modulus_var_ref = sorted_modulus_var_ref[sorted_indices]
        #     # for i in range(len(sorted_freqs)):
        #     #     print(f"Frequency: {sorted_freqs[i]}, Quotient: {sorted_quotient[i]}, Mouldus Ref: {sorted_modulus_var_ref[i]}")
        #     print()

        # doStuff(t, u, t_ref, u_ref)
        # doStuff(t, v, t_ref, v_ref)

        pointsAfterGap = 100
        numPointsYdir = 9

        for point in range(pointsAfterGap, len(points) - numPointsYdir):
            x, y, z = points[point]
            if y > 0.26:
                continue
            Y = []
            X = []
            for i in range(numPointsYdir):
                x, y, z = points[point + i]
                t, u, v, p = data[point + i].transpose()
                detector_u = NoiseDetector(t, u)
                detector_v = NoiseDetector(t, v)

                t_0_detected, results = detector_u.detect_t0_robust(
                    methods=["variance"]
                )
                _, u = detector_u.filter_data(t_0_detected)
                _, v = detector_v.filter_data(t_0_detected)

                rms = np.sqrt(np.mean(u**2 + v**2))
                Y.append(y)
                X.append(rms)
            Y = np.array(Y)
            X = np.array(X)
            # normalize X
            X = X / np.max(X)
            
            # create a spline for smoothness
            spline = make_interp_spline(Y, X, k=3)
            Y_smooth = np.linspace(Y.min(), Y.max(), 300)
            X_smooth = spline(Y_smooth)


            X_smooth = x/1000 + X_smooth

            ax.plot(X_smooth, Y_smooth, label=f"x = {x:.2f}")

    plt.legend()
    plt.show()

        # Aref = []

        # for pref in range(pointref, pointref + numPointsYdir):
        #     t, u, v, p = data[pref].transpose()
        #     # detector_u = NoiseDetector(t, u)
        #     # detector_v = NoiseDetector(t, v)
        #     # t_0_detected, results = detector_u.detect_t0_robust(methods=['variance'])
        #     # _, u = detector_u.filter_data(t_0_detected)
        #     # _, v = detector_v.filter_data(t_0_detected)
        #     print(f"shape u: {u.shape}")
        #     print(f"u: {u}")
        #     rms = np.sqrt(np.mean(v**2))
        #     Aref.append(rms)
        #     print(f"Point {points[pref]}: Aref = {rms}")

        # Aref = np.array(Aref)
        # print(f"Aref: {Aref}")

        # count = 0
        # for point in range(pointref + numPointsYdir, len(points) - numPointsYdir + 1):
        #     x, y, z = points[point]
        #     count += 1
        #     if count > 1:
        #         if count == numPointsYdir:
        #             count = 0
        #         continue
        #     if count == numPointsYdir:
        #         count = 0

        #     X.append(x)
        #
        #     A = []
        #     for i in range(numPointsYdir):
        #         t, u, v, p = data[point + i].transpose()
        #         # detector_u = NoiseDetector(t, u)
        #         # detector_v = NoiseDetector(t, v)

        #         # t_0_detected, results = detector_u.detect_t0_robust(methods=['variance'])
        #         # _, u = detector_u.filter_data(t_0_detected)
        #         # _, v = detector_v.filter_data(t_0_detected)

        #         rms = np.sqrt(np.mean(v**2))
        #         A.append(rms)
        #         print(f"Point {points[point]}: Aref = {rms}")
        #     A = np.array(A)

        #     nx.append(np.log(A / Aref))

        # nx = np.array(nx)
        # X = np.array(X)
        # print(nx)
        # ax.plot(X, nx, label=range(numPointsYdir))
    # plt.grid()
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()
