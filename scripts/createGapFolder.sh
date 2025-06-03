#!/bin/bash

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

function readInput {
  # prompt a message if there are less than 2 arguments
  if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo -e "${RED}Usage: $0 <depth> <width>${RESET}"
    echo -e "${RED}   or: $0 <depth> <width> <name_folder>${RESET}" 
    echo -e "${YELLOW}For example: $0 4 16.5 ${RESET}"
    echo -e "${YELLOW}         or: $0 4 16.5 d4_w16.5_custom${RESET}"
    exit 1
  fi

  depth=$1
  width=$2
  parent_dir=$(basename "$(dirname "$(realpath $session_file)")")
  codename="d${depth}_w${width}"
  folder_name=${codename}
  if [ "$#" -eq 3 ]; then
    folder_name=$3
  fi

  echo -e "${CYAN}Input file: $session_file${RESET}"
  echo -e "${CYAN}Geo file: $geo_file${RESET}"
  echo -e "${CYAN}Codename: $codename${RESET}"
  echo -e "${CYAN}Folder: $folder_name${RESET}"
  echo -e "${CYAN}Parent directory: $parent_dir${RESET}"
  echo ""

  # Check if the input files exist (mesh file and session file)
  if [[ ! -f "$geo_file" || ! -f "$session_file" ]]; then
    echo -e "${RED}Error opening the input files.${RESET}"
    exit 1
  fi
}

function generateFolders {
  pbspro_file="pbspro.job"
  slurm_file="slurm.job"
  mkdir -p "$folder_name"

  cp $session_file "$folder_name/$session_file"
  cp $pbspro_file "$folder_name/$pbspro_file"
  cp $slurm_file "$folder_name/$slurm_file"
  
  # update the depth and width in the new geo file
  sed -e "s/^D = .*deltaStar;/D = ${depth} * deltaStar;/" \
    -e "s/^W = .*deltaStar;/W = ${width} * deltaStar;/" "$geo_file" > "${folder_name}/mesh_${codename}.geo"

  cd "$folder_name"
  prepareRun.sh
  cd ..

  echo -e "${GREEN}All files have been generated.${RESET}"

}

source $SCRIPTS_DIR/bashFunctions/getMeshSessionFiles.sh

getMeshSessionFiles

readInput "$@"

generateFolders

