NODE="typhoon" # the node actually does not play a role becuase the database are all linked so it's the same for all nodes: typhoon, hurricane, splitfire, blackfriars.
USER="vb824"

sshfs -o allow_other -o kernel_cache -o auto_cache -o reconnect -o compression=no -o cache_timeout=600 -o ServerAliveInterval=15 ${USER}@${NODE}.ae.ic.ac.uk:/home/${USER}/Desktop/ ~/Desktop/PhD/nodes/Desktop/
if [ $? -eq 0 ]; then
    echo "Nodes data HOME mounted successfully!"
else
    echo "Nodes data HOME mount failed!"
fi
