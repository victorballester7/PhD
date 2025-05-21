# Paths and solvers
NEK_PATH=$HOME/nektar++
INC_SOLVER=$NEK_PATH/build/dist/bin/IncNavierStokesSolver 
COMP_SOLVER=$NEK_PATH/build/dist/bin/CompressibleFlowSolver 
SCRIPTS_DIR=$HOME/Desktop/PhD/scripts

JOB_ID=$PBS_JOBID
pbsjob="$PBS_O_WORKDIR/pbspro.job"
datefile=$(date +"%Y%m%d_%H%M%S".date)

# Find the number of CPUs
NP=$(wc -l $PBS_NODEFILE | awk '{print $1}')

source $SCRIPTS_DIR/bashFunctions/computeTimeMax.sh
source $SCRIPTS_DIR/bashFunctions/getMeshSessionFiles.sh
source $SCRIPTS_DIR/bashFunctions/uploadDateFile.sh
source $SCRIPTS_DIR/bashFunctions/updateHistoryEnergyFiles.sh
source $SCRIPTS_DIR/bashFunctions/runIncNS.sh

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
}

function getOutputFiles {
    # Extract log and output file names from pbspro.job
    log_file=$(grep "^#PBS -e" "$pbsjob" | awk '{print $3}')
    output_file=$(grep "^#PBS -o" "$pbsjob" | awk '{print $3}')

}

function setup {
    getTime
    computeTimeMax
    getMeshSessionFiles
    getOutputFiles
    uploadDateFile
    updateHistoryEnergyFiles

    rm -f $output_file $log_file

    # Load required modules
    # module load tools/eb-dev cmake/3.18.2 HDF5/1.10.7-gompi-2021a SCOTCH/6.1.0-gompi-2021a Boost/1.76.0-GCC-10.3.0 OpenBLAS/0.3.15-GCC-10.3.0 FlexiBLAS/3.0.4-GCC-10.3.0 FFTW/3.3.9-gompi-2021a ScaLAPACK/2.1.0-gompi-2021a-fb
    module load tools/eb-dev CMake/3.24.3-GCCcore-11.3.0 HDF5/1.13.1-gompi-2022a SCOTCH/7.0.1-gompi-2022a Boost/1.79.0-GCC-11.3.0 OpenBLAS/0.3.20-GCC-11.3.0 FlexiBLAS/3.2.0-GCC-11.3.0 FFTW/3.3.10-GCC-11.3.0 ScaLAPACK/2.2.0-gompi-2022a-fb arpack-ng/3.8.0-foss-2022a 
}

cd $PBS_O_WORKDIR

setup
runIncNS

