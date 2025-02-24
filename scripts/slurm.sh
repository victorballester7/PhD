# Paths and solvers
INC_SOLVER=IncNavierStokesSolver
SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

# Calculate the total number of processors
NP=$SLURM_NTASKS
JOB_ID=$SLURM_JOB_ID
slurmjob="$SLURM_SUBMIT_DIR/slurm.job"
history_file="HistoryPoints.his"
history_file_backup="HistoryPoints.his.old"
datefile=$(date +"%Y-%m-%d_%H-%M-%S".txt)

function getTime {
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

    # Remove leading zeros from hours, minutes, and seconds; like 01 -> 1
    hours=$(echo $hours | sed 's/^0*//')
    minutes=$(echo $minutes | sed 's/^0*//')
    seconds=$(echo $seconds | sed 's/^0*//')

    # Convert days, hours, minutes, seconds to total seconds
    TIMEMAX=$((days * 86400 + hours * 3600 + minutes * 60 + seconds))

    # substract 30 seconds for safe termination
    TIMEMAX=$((TIMEMAX - 30))

}

function getFiles {
    # Identify the mesh file (first one matching mesh*.xml)
    mesh_file=$(ls mesh*.xml 2>/dev/null | head -n 1)

    # Identify the session file (any other .xml file that is not the mesh file)
    session_file=$(ls *.xml 2>/dev/null | grep -v "^$mesh_file$" | head -n 1)

    # Extract log and output file names from slurm.job
    log_file=$(grep "^#SBATCH --error=" "$slurmjob" | awk '{print $2}' | cut -d= -f2)
    output_file=$(grep "^#SBATCH --output=" "$slurmjob" | awk '{print $2}' | cut -d= -f2)
}


getTime

getFiles

# create a file with the date and time of the job submission
echo "" > $datefile

cp $history_file $history_file_backup

rm -f $output_file $log_file $history_file

# Run the job start script
python3 $SCRIPTS_DIR/jobStart.py $JOB_ID

mpirun --timeout $TIMEMAX -np $NP $INC_SOLVER -v $mesh_file $session_file > $output_file 2> $log_file

python3 $SCRIPTS_DIR/jobFinish.py $JOB_ID
