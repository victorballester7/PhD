# Usage: ./run.sh <num_cores> <mesh_file> <session_file>

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <num_cores> <mesh_file> <session_file>"
    exit 1
fi

num_cores=$1
mesh_file=$2
session_file=$3

PYTHON=python3
# PYTHON=python


mpirun -np $num_cores IncNavierStokesSolver -v $mesh_file $session_file > output.txt 2> log.txt
python3 sendMessage.py .
