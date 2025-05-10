#!/bin/bash

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

# For remote access
# HOST="typhoon"
HOST="hpc"

# do not edit
USER="vb824"
if [ "$HOST" = "typhoon" ]; then
    DIR_REMOTE_PRE="/home/${USER}"
else
    DIR_REMOTE_PRE="/rds/general/user/${USER}/home"
fi

function readInput {
  # prompt a message if there are less than 2 arguments
  if [ "$#" -ne 2 ]; then 
    echo -e "${RED}Usage: $0 <depth> <width>${RESET}"
    echo -e "${YELLOW}For example: $0 4 16.5 ${RESET}"
    exit 1
  fi

  depth=$1
  width=$2
  codename="d${depth}_w${width}"
  localDIR_LS=$(pwd)
  localDIR_baseflow="${localDIR_LS}/../baseflow/dns"
  
  localDIRtmp="${localDIR_LS##*/Desktop/}"
  localDIRtmp="Desktop/${localDIRtmp/src/runs}"
  remoteDIR_LS="${DIR_REMOTE_PRE}/${localDIRtmp}"

  localDIRtmp="${localDIR_baseflow##*/Desktop/}"
  localDIRtmp="Desktop/${localDIRtmp/src/runs}"
  remoteDIR_baseflow="${DIR_REMOTE_PRE}/${localDIRtmp}"


  cd "$localDIR_baseflow/$codename" || exit 1

  getMeshSessionFiles
  
  echo -e "${CYAN}Session file: $session_file${RESET}"
  echo -e "${CYAN}Geo file: $geo_file${RESET}"
  echo -e "${CYAN}Folder: $codename${RESET}"
  echo -e "${CYAN}Local LS directory: $localDIR_LS${RESET}"
  echo -e "${CYAN}Local baseflow directory: $localDIR_baseflow${RESET}"
  echo -e "${CYAN}Remote LS directory: $remoteDIR_LS${RESET}"
  echo -e "${CYAN}Remote baseflow directory: $remoteDIR_baseflow${RESET}"
  echo ""

  # Check if the input files exist (mesh file and session file)
  if [[ ! -f "$session_file" ]]; then
    echo -e "${RED}Error opening the input files.${RESET}"
    exit 1
  fi
}

function createBaseflowFile {
  # Capture SSH output into local variables
  ssh "${USER}@${HOST}" /bin/bash << EOF
    cd "${remoteDIR_baseflow}/$codename" || exit 1

    # Extract last chk number
    chk_number=\$(grep 'Writing: "mesh_${codename}_.*\.chk"' output.txt | tail -n 1 | sed -n 's/.*mesh_${codename}_\\([0-9]\\+\\)\\.chk.*/\\1/p')

    mkdir -p "${remoteDIR_LS}/$codename"

    # Safely remove if baseflow.fld already exists (whether file or dir)
    rm -rf "${remoteDIR_LS}/${codename}/baseflow.fld"
    
    echo -e "${CYAN}Copying mesh_${codename}_\$chk_number.chk to ${remoteDIR_LS}/$codename/baseflow.fld${RESET}"
    cp -r mesh_${codename}_\$chk_number.chk ${remoteDIR_LS}/$codename/baseflow.fld
EOF
}


function modifyFile {
  cd "$localDIR_LS" || exit 1
  mkdir -p "$codename"
  cd "$codename" || exit 1
  cp "../$session_file" .
  cp "$localDIR_baseflow/$codename/$geo_file" .
  cp "$localDIR_baseflow/$codename/pbspro.job" .
  cp "$localDIR_baseflow/$codename/slurm.job" .

  # 3. Extract timestep
  timestep=$(awk '/<P> *TimeStep *=/ {
    for(i=1;i<=NF;i++) {
      if ($i ~ /^[0-9.]+$/) {
        print $i; exit
      }
    }
  }' "$localDIR_baseflow/$codename/$session_file")

  if [[ -z "$timestep" ]]; then
    echo "❌ Could not extract TimeStep from $session_file"
    return 1
  fi


  echo -e "${CYAN}TimeStep: $timestep${RESET}"

  # 5. Replace TimeStep line
  sed -i "s|<P> *TimeStep *= *[^<]*</P>|<P> TimeStep = ${timestep} </P>|" "$session_file"

  # run prepareRun.sh
  prepareRun.sh
  cd ..

  echo -e "${GREEN}Session file changed properly.${RESET}"

}

echo -e "${YELLOW} THIS SCRIPT SHOULD BE RUN FROM INSIDE THE LINEARSOLVER DIRECTORY (WHICH HAS TO CONTAIN A REFERENCE SESSION FILE, THE .GEO AND PBS FILES ARE TAKEN FROM THE BASEFLOW/DNS DIRERCTORY)\n ${RESET}"

source $SCRIPTS_DIR/bashFunctions/getMeshSessionFiles.sh

readInput "$@"

createBaseflowFile

modifyFile

