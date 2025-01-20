#!/bin/bash

# prompt a message if there are less than 4 arguments
if [ "$#" -lt 4 ]; then 
    echo "Usage: $0 <mesh_file> <general_session_file> <parameter_to_change> <values>"
    echo "For example: $0 mesh_finer.xml gap_pert_incNS.xml mode_num 1 2 3 4 5"
    exit 1
fi


# Input XML file and maximum mode number
mesh_file=$1
session_file=$2                 
parameter=$3
parameter_values="${@:4}" # all the values after the 3rd argument
parent_dir=$(basename "$(dirname "$(realpath gap_incNS.xml)")")

echo "Input file: $session_file"
echo "Mesh file: $mesh_file"
echo "Parameter to change: $parameter"
echo "Values: $parameter_values"
echo "Parent directory: $parent_dir"
echo ""

# Check if the input files exist (mesh file and session file)
if [[ ! -f "$mesh_file" || ! -f "$session_file" ]]; then
  echo "Error opening the input files."
  exit 1
fi

# check if there exists such a parameter in the session file
if grep -q "<p> ${parameter}[[:space:]]*=.*</p>" "$session_file"; then
  pCapital=0
elif grep -q "<P> ${parameter}[[:space:]]*=.*</P>" "$session_file"; then
  pCapital=1
else
  echo "Parameter $parameter not found in the session file."
  exit 1
fi


# Loop over the range of mode numbers
for p in $parameter_values; do
  # Create directory for the current p
  dir_name="${parameter}${p}"
  mkdir -p "$dir_name"
  cp "$mesh_file" "${dir_name}/${mesh_file}"
  
  # Copy the input file and modify it
  output_file="${dir_name}/${session_file}"
  
  if [ $pCapital -eq 1 ]; then
    sed "s/<P> ${parameter}[[:space:]]*=.*<\/P>/<P> ${parameter} = ${p} <\/P>/g" "$session_file" > "$output_file"
  else
    sed "s/<p> ${parameter}[[:space:]]*=.*<\/p>/<p> ${parameter} = ${p} <\/p>/g" "$session_file" > "$output_file"
  fi
  
  #!/bin/bash

  # Check if there are any .job files in the current directory
  if ls *.job 1> /dev/null 2>&1; then
    for job_file in *.job; do
      cp "$job_file" "${dir_name}/${job_file}"
      sed -i "s/^#PBS -N .*/#PBS -N ${parent_dir}_${dir_name}/" "${dir_name}/${job_file}"
    done
  else
    echo "No .job files found in the current directory."
  fi

  
  echo "Generated file for ${parameter} $p in $dir_name"
done

echo "All files have been generated."

