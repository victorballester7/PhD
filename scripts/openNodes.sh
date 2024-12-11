NODE="typhoon" # the node actually does not play a role becuase the database are all linked so it's the same for all nodes: typhoon, hurricane, splitfire, blackfriars.
CLUSTER="hpc"
USER="vb824"

FOLDERTOMOUNT="Desktop/PhD"
WHERETOMOUNT="$HOME/hosts"


echo "Mounting nodes..."
mkdir -p ${WHERETOMOUNT}/nodes
sshfs -o allow_other -o kernel_cache -o auto_cache -o reconnect -o compression=no -o cache_timeout=600 -o ServerAliveInterval=15 ${USER}@${NODE}:/home/${USER}/${FOLDERTOMOUNT} ${WHERETOMOUNT}/nodes
if [ $? -eq 0 ]; then
    echo "Nodes data mounted successfully!"
else
    echo "Nodes data mount failed!"
fi

echo "Mounting cluster..."
mkdir -p ${WHERETOMOUNT}/hpc
sshfs -o allow_other -o kernel_cache -o auto_cache -o reconnect -o compression=no -o cache_timeout=600 -o ServerAliveInterval=15 ${USER}@${CLUSTER}:/rds/general/user/${USER}/home/${FOLDERTOMOUNT} ${WHERETOMOUNT}/hpc
if [ $? -eq 0 ]; then
    echo "Cluster data mounted successfully!"
else
    echo "Cluster data mount failed!"
fi
