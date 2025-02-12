# Paths and solvers
NEK_PATH=$HOME/nektar++
INC_SOLVER=$NEK_PATH/build/dist/bin/IncNavierStokesSolver 
COMP_SOLVER=$NEK_PATH/build/dist/bin/CompressibleFlowSolver 
SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

JOB_ID=$PBS_JOBID
pbsjob="$PBS_O_WORKDIR/pbspro.job"
history_file="HistoryPoints.his"
history_file_backup="HistoryPoints.his.old"

# Find the number of CPUs
NP=$(wc -l $PBS_NODEFILE | awk '{print $1}')

function getTime { 
    # get the time limit
    time_str=$(grep "^#PBS -l walltime=" "$pbsjob" | awk '{print $3}')
    if [[ "$time_str" =~ ([0-9]+):([0-9]+):([0-9]+) ]]; then
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
    # Identify the mesh file (first one matching mesh_*.xml)
    mesh_file=$(ls mesh_*.xml 2>/dev/null | head -n 1)

    # Identify the session file (any other .xml file that is not the mesh file)
    session_file=$(ls *.xml 2>/dev/null | grep -v "^$mesh_file$" | head -n 1)

    # Extract log and output file names from pbspro.job
    log_file=$(grep "^#PBS -e" "$pbsjob" | awk '{print $3}')
    output_file=$(grep "^#PBS -o" "$pbsjob" | awk '{print $3}')

}

cd $PBS_O_WORKDIR

getTime

getFiles

cp $history_file $history_file_backup

rm -f $output_file $log_file $history_file

# Load required modules
module load tools/eb-dev cmake/3.18.2 HDF5/1.10.7-gompi-2021a SCOTCH/6.1.0-gompi-2021a Boost/1.76.0-GCC-10.3.0 OpenBLAS/0.3.15-GCC-10.3.0 FlexiBLAS/3.0.4-GCC-10.3.0 FFTW/3.3.9-gompi-2021a ScaLAPACK/2.1.0-gompi-2021a-fb

# Run the job start script
python3 $SCRIPTS_DIR/jobStart.py $JOB_ID

mpirun --timeout $TIMEMAX -np $NP $INC_SOLVER -v $mesh_file $session_file > $output_file 2> $log_file

python3 $SCRIPTS_DIR/jobFinish.py $JOB_ID

