import subprocess

path_gap = "~/hosts/hpc/PhD/runs/incNSboeingGapRe1000/directLinearSolver/blowingSuction/"

path_flat = "~/hosts/hpc/PhD/runs/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn/"


code_names = [
    "d4_w10",
    "d4_w15",
    "d3.75_w10",
    "d3.75_w15",
    "d3.5_w10",
    "d3.5_w15",
    "d3.25_w10",
    "d3.25_w15",
    "d3_w10",
    "d3_w15",
    "d2.75_w10",
    "d2.75_w15",
    "d2.5_w10",
    "d2.5_w15",
    "d2.5_w20",
    "d2.25_w10",
    "d2.25_w16",
    "d2.25_w20",
    "d2.25_w25",
    "d2.25_w31",
    "d2_w10",
    "d2_w16",
    "d2_w20",
    "d2_w24",
    "d2_w28",
    "d2_w32",
    "d2_w36",
    "d1.75_w10",
    "d1.75_w15",
    "d1.75_w20",
    "d1.75_w25",
    "d1.75_w30",
    "d1.75_w35",
    "d1.75_w40",
    "d1.75_w45",
    "d1.5_w10",
    "d1.5_w15",
    "d1.5_w20",
    "d1.5_w25",
    "d1.5_w30",
    "d1.5_w35",
    "d1.5_w40",
    "d1.5_w45",
    "d1.5_w50",
    "d1.25_w10",
    "d1.25_w15",
    "d1.25_w20",
    "d1.25_w25",
    "d1.25_w30",
    "d1.25_w35",
    "d1.25_w40",
    "d1.25_w45",
    "d1.25_w50",
    "d1.25_w60",
    "d1.25_w70",
    # "d1.25_w80",
    "d1_w10",
    "d1_w15",
    "d1_w20",
    "d1_w25",
    "d1_w30",
    "d1_w34",
    "d1_w38",
    "d1_w45",
    "d1_w50",
    "d1_w60",
    "d1_w70",
    "d0.75_w10",
    "d0.75_w20",
    "d0.75_w30",
    "d0.75_w40",
    "d0.75_w50",
    "d0.75_w60",
    "d0.75_w70",
    "d0.5_w10",
    "d0.5_w20",
    "d0.5_w30",
    "d0.5_w40",
    "d0.5_w50",
    "d0.5_w60",
    "d0.5_w70",
]

command = "python plotNfactor.py"

command += " " + path_flat

for code_name in code_names:
    folder_name = path_gap + code_name + "/wgn"
    command += " " + folder_name

command += " --use_DELTA_N"

print(command)
# result = subprocess.run(command, shell=True, capture_output=True, text=True)

# if result.returncode == 0:
#     print(result.stdout)
# else:
#     print("Error:", result.stderr)
#     exit(result.returncode)

