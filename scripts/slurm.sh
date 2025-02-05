#!/bin/bash 

if [ "$#" -ne 3 ]; then 
    echo "Usage: $0 <number of processors> <job ID> <pwd>"
    echo "Example: $0 4 454167 /path/to/working/directory"
    exit 1
fi

# Calculate the total number of processors
NP=$1
JOB_ID=$2
slurmjob="$3/slurm.job"

# Extract the time line
time_str=$(grep "^#SBATCH --time=" "$slurmjob" | awk '{print $2}')

# Split into days and HH:MM:SS
if [[ "$time_str" =~ ([0-9]+)-([0-9]+):([0-9]+):([0-9]+) ]]; then
    days="${BASH_REMATCH[1]}"
    hours="${BASH_REMATCH[2]}"
    minutes="${BASH_REMATCH[3]}"
    seconds="${BASH_REMATCH[4]}"
elif [[ "$time_str" =~ ([0-9]+):([0-9]+):([0-9]+) ]]; then
    days=0
    hours="${BASH_REMATCH[1]}"
    minutes="${BASH_REMATCH[2]}"
    seconds="${BASH_REMATCH[3]}"
else
    echo "Invalid time format"
    exit 1
fi

# Convert days, hours, minutes, seconds to total seconds
TIMEMAX=$((days * 86400 + hours * 3600 + minutes * 60 + seconds))

# substract 30 seconds for safe termination
TIMEMAX=$((TIMEMAX - 30))

# Identify the mesh file (first one matching mesh_*.xml)
mesh_file=$(ls mesh_*.xml 2>/dev/null | head -n 1)

# Identify the session file (any other .xml file that is not the mesh file)
session_file=$(ls *.xml 2>/dev/null | grep -v "^$mesh_file$" | head -n 1)

# Paths and solvers
INC_SOLVER=IncNavierStokesSolver
SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

# Run the job start script
python3 $SCRIPTS_DIR/jobStart.py $JOB_ID

rm -f output.txt log.txt

timeout $TIMEMAX mpirun -np $NP $INC_SOLVER -v $mesh_file $session_file > output.txt 2> log.txt

if [ $? -eq 124 ]; then
    python3 $SCRIPTS_DIR/jobFinish.py $JOB_ID 1
else
    python3 $SCRIPTS_DIR/jobFinish.py $JOB_ID 0
fi

