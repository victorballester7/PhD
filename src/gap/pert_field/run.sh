# Usage: ./run.sh <num_cores> <mesh_file> <session_file>

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <num_cores> <num_cores_fourier> <mesh_file> <session_file>"
    exit 1
fi

num_cores=$1
num_cores_fourier=$2
mesh_file=$3
session_file=$4

PYTHON=python3
# PYTHON=python


mpirun -np $num_cores IncNavierStokesSolver --npz $num_cores_fourier -v $mesh_file $session_file > output.txt 2> log.txt
python3 sendMessage.py .
