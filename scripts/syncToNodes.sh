# #!/bin/bash

# # Define local and remote paths
# LOCAL_DIR="$HOME/Phd"
# REMOTE_USER="your_username"   # Replace with your username on typhoon
# REMOTE_HOST="typhoon"
# REMOTE_DIR="~/desktop/PhD"

# # Sync docs and scripts directly
# rsync -avz --progress "$LOCAL_DIR/docs" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
# rsync -avz --progress "$LOCAL_DIR/scripts" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

# # Sync src folder as runs on remote
# rsync -avz --progress "$LOCAL_DIR/src" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/runs"

#!/bin/bash

# Define local and remote paths
LOCAL_DIR="$HOME/Desktop/PhD"
REMOTE_USER="vb824"  
REMOTE_DIR="~/Desktop/PhD"

# List of remote hosts
HOSTS=("typhoon" "hpc")
SYNC_DIRS=("${LOCAL_DIR}/docs" "${LOCAL_DIR}/scripts")

# I set the src directory separately as it is synced to the runs directory on the remote hosts (which does not exist locally)
SRC_DIR="${LOCAL_DIR}/src"
RUNS_DIR="${REMOTE_DIR}/runs"

# Loop through each host and sync the directories
for HOST in "${HOSTS[@]}"; do
    echo "Syncing with $HOST..."
    for DIR in "${SYNC_DIRS[@]}"; do
        rsync -avz --progress "$DIR" "$REMOTE_USER@$HOST:$REMOTE_DIR/"
    done
    rsync -avz --progress "$SRC_DIR/" "$REMOTE_USER@$HOST:$RUNS_DIR"
done

