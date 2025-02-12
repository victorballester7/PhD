#!/bin/bash

# Description: This script converts the output (checkpoint) files (*.chk or *.fld) to .vtu format 
# in order to visualize the results in Paraview or similar.

# Usage: Run from the directory where the .chk or .fld files are stored:
# $directory_of_scripts/fieldconvert.sh 01 02 03  # Converts mesh_01.chk, mesh_02.chk, mesh_03.chk

# Colors
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
CYAN='\e[36m'
NC='\e[0m' # No Color

# Directory to search (change '.' to the target directory if needed)
directory=$(pwd)

overwrite_all=false  # flag to overwrite all files

mesh_file=$(ls mesh_*.xml 2>/dev/null | head -n 1)
session_file=$(ls *.xml 2>/dev/null | grep -v "^$mesh_file$" | head -n 1)

if [ "$#" -gt 0 ]; then
  files=()
  options=()

  # if the first argument is '-m', then read the second argument and store it to later pass it to FieldConvert
  if [ "$1" = "-m" ]; then
      options+=("$1" "$2")
      shift 2
  fi

  for arg in "$@"; do
    if [[ "$arg" =~ ^[0-9]+$ ]]; then
        # we remove extension from mesh_file and add the argument (number) to it + .chk
      files+=( $(echo "${mesh_file}" | sed "s/\.[^.]*$//")_"$arg".chk )
    else
      files+=("$arg")
    fi
  done
else
  files=($(find "${directory}" -maxdepth 1 -type d \( -name "*.chk" -o -name "*.fld" \) | sort))
fi


if [ ${#files[@]} -eq 0 ]; then
    echo -e "${RED}No .chk or .fld files found in the directory.${NC}"
    exit 1
fi

for file in "${files[@]}"; do
    if [ ! -d "${file}" ]; then
        echo -e "${YELLOW}File ${file} does not exist. Skipping...${NC}"
        continue
    fi

    name=$(basename $(basename "${file}" .chk) .fld)
    output_file="${name}.vtu"

    if [ -f "${output_file}" ]; then
        if [ "$overwrite_all" = false ]; then
            while true; do
                echo -ne "${YELLOW}File ${output_file} already exists. Do you want to overwrite it? (y/n/A): ${NC}"
                read -r choice
                choice=${choice:-A}  # if the user presses enter, the default option is 'A'
                case "$choice" in
                    y|Y) break ;;  # overwrite
                    n|N) echo -e "${GREEN}Omitting ${output_file}.${NC}"; continue 2;;
                    a|A) overwrite_all=true; break ;;  # overwrite all
                    *) echo -e "${RED}Invalid option. Introduce 'y' (yes), 'n' (no) o 'a' (all).${NC}" ;;
                esac
            done
        fi
    fi

    echo -e "${GREEN}Converting ${file} to ${output_file}...${NC}"
    FieldConvert -f ${options[@]} "$mesh_file" "$session_file" "${file}" "${output_file}"
done

echo -e "${CYAN}Conversion completed.${NC}"

