#!/bin/bash

# Input XML file and maximum mode number
session_file="gap_pert_incNS.xml"  # Replace with your actual input file
mesh_file="mesh_finer.xml"         # Replace with your actual mesh file
mode_max=5                         # Replace with your desired maximum mode number

# Check if the input file exists
if [[ ! -f $session_file ]]; then
  echo "Error: Input file '$session_file' does not exist."
  exit 1
fi

# get the path direftory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


# Loop over the range of mode numbers
for mode in $(seq 1 $mode_max); do
  # Create directory for the current mode
  dir_name="mode${mode}"
  mkdir -p "$dir_name"
  cp "$mesh_file" "${dir_name}/${mesh_file}"
  
  cp "${DIR}/sendMessage.py" "${dir_name}/"
  cp "${DIR}/run.sh" "${dir_name}/"
  cp "pbspro.job" "${dir_name}/"


  # Copy the input file and modify it
  output_file="${dir_name}/${session_file}"
  sed "s/<p> mode_num[[:space:]]*=.*<\/p>/<p> mode_num = ${mode} <\/p>/g" "$session_file" > "$output_file"

  echo "Generated file for mode $mode in $dir_name"
done

echo "All files have been generated."

