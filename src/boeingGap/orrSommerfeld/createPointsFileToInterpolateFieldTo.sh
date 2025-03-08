#!/bin/bash

# Description
# 1. generate a .pts file with N points in a line. Initially it was set for fixed x and varying y to create N points spaced quadratically in y (more concentrated near ymin than near ymax). The output file is points.pts
# 2. This file is then sent to the nodes, which uses fieldconvert of a .fld file to interpolate the field to the points in the .pts file.
# 3. The output of fieldconvert is copied back to the local machine.

# Usage: ./createPointsFileToInterpolateFieldTo.sh

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

# Get user input
x=254
ymin=0
ymax=75
N=200
datadir="data"
output_file="${datadir}/points_x$x"


# For remote access
HOST="typhoon"
# HOST="hpc"
USER="vb824"
# DIR_REMOTE="~/Desktop/PhD/runs/boeingGap/baseflowRe1000_IncNS2D/dns/d4_w16.35"
DIR_REMOTE="/home/${USER}/Desktop/PhD/runs/boeingGap/evSolverRe1000_IncNS2D/d4_w16.35"
MESH_REMOTE="mesh_d4_w16.35_shearMesh.xml"
FLD_REMOTE="baseflow_shearMesh.fld"


function genPointsFile {
    echo -e "${YELLOW}Generating .pts file...${RESET}"

    # Create and write to the .pts file
    {
        echo '<?xml version="1.0" encoding="utf-8" ?>'
        echo '<NEKTAR>'
        echo '<POINTS DIM="2" FIELDS="">'

        for ((i = 0; i < N; i++)); do
            step=$(echo "scale=6; $i / ($N - 1)" | bc)
            y=$(echo "scale=6; $ymin + ($ymax - $ymin) * $step * $step" | bc)
            printf "%.6f %.6f\n" "$x" "$y"
        done

        echo '</POINTS>'
        echo '</NEKTAR>'
    } > "$output_file".pts

    echo -e "${GREEN}File '${output_file}'.pts generated successfully!${RESET}"

}

function interpolateData {
    echo -e "${CYAN}Interpolating field data to points...${RESET}"

    scp -r "${DIR_SCRIPT}/${output_file}.pts" "${USER}@${HOST}:${DIR_REMOTE}/$datadir"

    ssh "${USER}@${HOST}" /bin/bash << EOF
        source /etc/profile
        source ~/.bashrc  # Ensure modules are available
        cd "${DIR_REMOTE}"
        mkdir -p "${datadir}"
        module load nektar++
        rm -f ${datadir}/*.dat
        FieldConvert -m interppoints:fromxml="${MESH_REMOTE}":fromfld="${FLD_REMOTE}":topts="${output_file}".pts ${output_file}.dat
EOF
    
    scp "${USER}@${HOST}:${DIR_REMOTE}/${output_file}.dat" "${DIR_SCRIPT}/$datadir"
    echo -e "${GREEN}Field data interpolated to points successfully!${RESET}"
}

# Get the script's directory
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

genPointsFile

interpolateData

