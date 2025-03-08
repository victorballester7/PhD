#!/bin/bash

# Description: This script interpolates a field file (of the form .fld .chk, entered as an argument) that has been computed using an old mesh, to a new mesh. So it outputs the a field .fld file for the new mesh.

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

# function getOldMeshFile {
#     # Identify the mesh file (first one matching mesh*.xml and does not contain "old")
#     old_mesh_file=$(ls mesh*.xml 2>/dev/null | grep -v "^$mesh_file" | grep -v "^$session_file" | head -n 1)
# }

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 field_file.fld old_mesh_file.xml"
    echo "Example: $0 field_file.fld ../d4_w16.35/mesh_d4_w16.35.xml"
    exit 1
fi

field_file=$1
old_mesh_file=$2
new_field_file="initialCond.fld"

# Get the script's directory
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $DIR_SCRIPT/bashFunctions/getMeshSessionFiles.sh

getMeshSessionFiles > /dev/null

echo -e "${CYAN}Old mesh file: $old_mesh_file${RESET}"
echo -e "${CYAN}Interpolating field file: $field_file${RESET}"
echo -e "${CYAN}New mesh file: $mesh_file${RESET}"
echo -e "${CYAN}interpolated field file: $new_field_file${RESET}"

# Interpolate the field file

FieldConvert -m interpfield:fromxml=${old_mesh_file}:fromfld=${field_file} ${mesh_file} ${new_field_file}

