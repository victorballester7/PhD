import subprocess
import numpy as np
from pathlib import Path

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
    "d1.25_w80",
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

path_gap = "~/hosts/hpc/PhD/runs/incNSboeingGapRe1000/directLinearSolver/blowingSuction/"

path_flat = "~/hosts/hpc/PhD/runs/flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn/"



def editFile(pathFile: Path, replacement_line, line_startswith) -> None:
    # Read the file and replace the specified line
    with open(pathFile, "r") as file:
        lines = file.readlines()

    with open(pathFile, "w") as file:
        for line in lines:
            linechanged = False
            # loop in the i,j in (replacement_line, line_startswith)
            for rep_line, line_start in zip(replacement_line, line_startswith):
                if line.strip().startswith(line_start):
                    # take the last part of the line (starting with # ) and add it to rep_line
                    rep_line = rep_line + " #" + line.split("#")[-1]
                    file.write(rep_line)
                    linechanged = True
                    break
            if not linechanged:
                file.write(line)

def main():
    path_script = "~/hosts/hpc/PhD/scrip/createPointsOfSectionDomain.sh"
    path_script = Path(path_script)

    for code_name in code_names:
        path_gap_code = path_gap + code_name + "/wgn"
        # see how many files are named of the form "mesh_$code_name_*.chk" inside path_gap_code

        num_chkfiles = ...

        line_startswith = np.array([
            "CASE=", 
            "CHKFILE_FINAL=",
        ])
        replacement_line = np.array([
            f"CASE=\"{code_name}\"",
            f"CHKFILE_FINAL={num_chkfiles}",
        ])
        
        

        editFile(Path(path_script), replacement_line, line_startswith)

        # execute script

# result = subprocess.run(command, shell=True, capture_output=True, text=True)

# if result.returncode == 0:
#     print(result.stdout)
# else:
#     print("Error:", result.stderr)
#     exit(result.returncode)
if __name__ == "__main__":
    main()
