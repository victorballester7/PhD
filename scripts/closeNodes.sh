WHERETOMOUNT="~/hosts"

echo "Unmounting nodes..."
umount ${WHERETOMOUNT}/nodes
if [ $? -eq 0 ]; then
    echo "Nodes data unmounted successfully!"
else
    echo "Nodes data unmount failed!"
fi

echo "Unmounting cluster..."
umount ${WHERETOMOUNT}/hpc
if [ $? -eq 0 ]; then
    echo "Cluster data unmounted successfully!"
else
    echo "Cluster data unmount failed!"
fi

