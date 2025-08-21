#!/bin/bash

# Description
# 1. generate a .pts file with N points in a line for multiple x values
# 2. This file is then sent to the nodes, which uses fieldconvert of a .fld file to interpolate the field to the points in the .pts file.
# 3. The output of fieldconvert is copied back to the local machine.
# Usage: ./createPointsFileToInterpolateFieldTo.sh

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

constVar="x"
constValue=(-50 -25 0 20 40 60 80 100 150 200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000)
varValueMIN=0
varValueMAX=150
N=600

datadir="data"
HOST="hpc"
CASE="d4_w15"
DIR="incNSboeingGapRe1000/directLinearSolver/blowingSuction/${CASE}/wgnInsideDomainNektarAveraged"
# DIR="incNSboeingGapRe1000/directLinearSolver/blowingSuction/oldSetups/bs_withOmegaFromOrrSommerfeld/${CASE}/expBC_omega0.0465"
# DIR="flatSurfaceRe1000IncNS/directLinearSolver/blowingSuction/wgn"
MESH_REMOTE="mesh_${CASE}.xml"
CHKFILE="avg"
EXTENSION=".fld"

# automatic variables
USER="vb824"
DIR_REMOTE_PRE="/rds/general/user/${USER}/home"
DIR_REMOTE="${DIR_REMOTE_PRE}/Desktop/PhD/runs/${DIR}"
DIR_LOCAL="${HOME}/Desktop/PhD/src/${DIR}"
mkdir -p "${DIR_LOCAL}/${datadir}"

generate_pts_file_for_chkfile() {
    local chkfile="$1"
    local output_file="${datadir}/points${chkfile}_all_n${N}"
    local file_path="${DIR_LOCAL}/${output_file}.pts"

    {
        echo '<?xml version="1.0" encoding="utf-8" ?>'
        echo '<NEKTAR>'
        echo '<POINTS DIM="2" FIELDS="">'

        for varA in "${constValue[@]}"; do
            for ((i = 0; i < N; i++)); do
                step=$(echo "scale=6; $i / ($N - 1)" | bc)
                varB=$(echo "scale=6; $varValueMIN + ($varValueMAX - $varValueMIN) * $step * $step" | bc)
                if [ "$constVar" = "x" ]; then
                    x=$varA
                    y=$varB
                else
                    x=$varB
                    y=$varA
                fi
                printf "%.6f %.6f\n" "$x" "$y"
            done
            echo -e "${CYAN}Generated points for constValue=${varA}${RESET}" >&2
        done

        echo '</POINTS>'
        echo '</NEKTAR>'
    } > "$file_path"

    echo -e "${GREEN}Generated combined .pts file: ${output_file}.pts${RESET}"
}

# Create .pts file for first CHKFILE and then cp all the others to the rest CHKFILES
generate_pts_file_for_chkfile "$CHKFILE"

echo -e "${GREEN}All .pts files generated for case ${CASE}!${RESET}"


# Transfer all .pts files
rsync -avz --progress "${DIR_LOCAL}/" "${USER}@${HOST}:${DIR_REMOTE}/"

# Create array string for remote use
constValue_str=$(printf "%s " "${constValue[@]}")

# Do all interpolations remotely in one SSH session
ssh "${USER}@${HOST}" /bin/bash << EOF
    source /etc/profile
    source ~/.bashrc  # Ensure modules are available
    
    # Try to load nektar++ module, continue if it fails
    module load nektar++ || echo "Warning: Could not load nektar++ module, continuing anyway..."
    
    cd "${DIR_REMOTE}"
    
    # Convert string back to array
    constValue_array=(${constValue_str})
    
    FLD="mesh_${CASE}_${CHKFILE}${EXTENSION}"
    output_file="${datadir}/points${CHKFILE}_all_n${N}"
    echo "\${FLD}"
    echo "\${output_file}.pts"
    echo "Processing CHKFILE ${CHKFILE}..."
    FieldConvert -m interppoints:fromxml=${MESH_REMOTE}:fromfld=\${FLD}:topts=\${output_file}.pts \${output_file}.dat
    echo "Completed CHKFILE ${CHKFILE} (case: ${CASE})"
EOF

# Retrieve all .dat files
rsync -avz --progress "${USER}@${HOST}:${DIR_REMOTE}/${datadir}/" "${DIR_LOCAL}/${datadir}/"

echo -e "${GREEN}All interpolations completed and files retrieved for case ${CASE}!${RESET}"

