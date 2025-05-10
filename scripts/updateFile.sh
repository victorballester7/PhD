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
  localDIR=$(pwd)

  localDIRtmp="${localDIR##*/Desktop/}"
  localDIRtmp="Desktop/${localDIRtmp/src/runs}"
  remoteDIR="${DIR_REMOTE_PRE}/${localDIRtmp}"


  echo -e "${CYAN}Session file: $session_file${RESET}"
  echo -e "${CYAN}Folder: $codename${RESET}"
  echo -e "${CYAN}Local directory: $localDIR${RESET}"
  echo -e "${CYAN}Remote directory: $remoteDIR${RESET}"
  echo ""

  # Check if the input files exist (mesh file and session file)
  if [[ ! -f "$session_file" ]]; then
    echo -e "${RED}Error opening the input files.${RESET}"
    exit 1
  fi
}

function comment_descommentOutIC {
# Paso 1: Comentar todas las secciones InitialConditions
# (por seguridad, para evitar que haya más de una activa)
#!/bin/bash
tmpfile="$(mktemp)"
#!/bin/bash

# Check if the first <F VAR=...> line is commented
awk '
/<F VAR=/ {
    if ($0 ~ /<!--/) {
        # Line contains <!--, assume it is commented
        exit 0
    } else {
        # Line is not commented
        exit 1
    }
}
' "$session_file"

if [ $? -eq 0 ]; then
  echo -e "${YELLOW}Commenting the blasius IC and uncommenting the IC with mesh file.${RESET}"
    awk '
      BEGIN { 
        found_commented = 0; 
        found_uncommented = 0; 
      }
    {
      if (!found_commented && $0 ~ /^\s*<!--\s*<FUNCTION NAME="InitialConditions">/) {
        found_commented = 1;
        for (i=0; i<3; i++) {
          sub(/^\s*<!--\s*/, "", $0);
          sub(/\s*-->$/, "", $0);
          print;
          if (i<2) {
            getline;
          }
      }
  }
  else if (found_commented && !found_uncommented && $0 ~ /^\s*<FUNCTION NAME="InitialConditions">/) {
    found_uncommented = 1;
    print "<!-- " $0 " -->";
    for (i=0; i<20; i++) {
      getline;
      print " <!-- " $0 " -->";
    }
  }
  else {
    print;
  }
  }
  ' "$session_file" > "$tmpfile" && mv "$tmpfile" "$session_file"
fi

}

function getTimeStepAndChkFile {
  # Capture SSH output into local variables
  read -r chk_number cfl1 cfl2 cfl3 cfl4 <<< "$(ssh "${USER}@${HOST}" /bin/bash << EOF
    cd "${remoteDIR}/$codename" || exit 1

    # Extract last chk number
    chk_number=\$(grep 'Writing: "mesh_${codename}_.*\.chk"' output.txt | tail -n 1 | sed -n 's/.*mesh_${codename}_\\([0-9]\\+\\)\\.chk.*/\\1/p')

    # Extract last 4 CFL values
    mapfile -t cfls < <(grep 'CFL:' output.txt | tail -n 4 | awk '{print \$2}')

    echo "\$chk_number \${cfls[0]} \${cfls[1]} \${cfls[2]} \${cfls[3]}"
EOF
)"

  # Store CFLs in an array
  cfls=("$cfl1" "$cfl2" "$cfl3" "$cfl4")

  # Print results
  echo -e "${CYAN}Last chk file number: $chk_number${RESET}"
  echo -e "${CYAN}Last 4 CFL values:${RESET}"
  for i in "${!cfls[@]}"; do
    echo -e "${CYAN}CFL[-$((4 - i))]: ${cfls[$i]}${RESET}"
  done
}


function modifyFile {
  cd "$codename" || exit 1

  new_chk_file="mesh_${codename}_${chk_number}.chk"

  update_just_restart_file=true
  while true; do
    echo -e "${YELLOW}Would you like to update ONLY the restart file, or change as well the number of modes to 8-9 (which changes timestep as well) and remove SVV? (Y (only restart file)/n (change everything)) (default = y)${RESET}"
    read -n 1 -r choice
    echo ""
    choice=${choice:-Y} # Default to 'Y' if no input is given

    case $choice in
        y|Y)
            update_just_restart_file=true
            break
            ;;
        n|N)
            update_just_restart_file=false
            break
            ;;
        *)
        echo -e "${RED}Invalid option. Introduce 'y' (to change the restart file only), 'n' (to change everything).${RESET}"
        ;;
    esac
  done

  echo -e "${YELLOW}Update JUST the restart file: $update_just_restart_file${RESET}"

  # 1. Replace chk file name
  # sed -i "s|<F VAR=\"u,v,p\" FILE=\"mesh_${codename}_.*\.chk\" />|<F VAR=\"u,v,p\" FILE=\"${new_chk_file}\" />|" "$session_file"
  comment_descommentOutIC

  sed -i "s/\(FILE=\"\)[^\"]*\(\".*\)/\1${new_chk_file}\2/" "$session_file"



  # Use proper syntax for boolean logic
  if [[ "$update_just_restart_file" == "true" ]] || \
     (grep -q 'NUMMODES="9"' "$session_file" && grep -q 'NUMMODES="8"' "$session_file"); then
    mult="1"
  else
    mult="0.5625"
  fi

  # 2. Replace NUMMODES
  if [[ "$update_just_restart_file" != "true" ]]; then
    sed -i 's/NUMMODES="7"/NUMMODES="9"/' "$session_file"
    sed -i 's/NUMMODES="6"/NUMMODES="8"/' "$session_file"
  fi


  # 3. Extract timestep
  old_timestep=$(awk '/<P> *TimeStep *=/ {
    for(i=1;i<=NF;i++) {
      if ($i ~ /^[0-9.]+$/) {
        print $i; exit
      }
    }
  }' "$session_file")

  if [[ -z "$old_timestep" ]]; then
    echo -e "${RED}Could not extract TimeStep from $session_file.${RESET}"
    return 1
  fi

  # 4. Compute new timestep
  newCFL="0.29"
  new_timestep=$(echo "$old_timestep * $mult * $newCFL / ${cfls[0]}" | bc -l)

  echo -e "${CYAN}Old TimeStep: $old_timestep${RESET}"
  echo -e "${CYAN}New TimeStep: $new_timestep${RESET}"

  # 5. Replace TimeStep line
  sed -i "s|<P> *TimeStep *= *${old_timestep} *<\/P>|<P> TimeStep = ${new_timestep} </P>|" "$session_file"

  # 6. Delete the line containing SpectralVanishingViscosity
  if [[ "$update_just_restart_file" != "true" ]]; then
    sed -i '/SpectralVanishingViscosity/d' "$session_file"
  fi
  
  echo -e "${GREEN}Session file changed properly.${RESET}"

}

source $SCRIPTS_DIR/bashFunctions/getMeshSessionFiles.sh

getMeshSessionFiles

readInput "$@"

getTimeStepAndChkFile

modifyFile
