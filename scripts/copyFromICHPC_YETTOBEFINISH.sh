# # copy the files to IDRIS
date=$(date +"%Y%m%d") # current date

# prompt a message if there are less or more than 1 argument
if [ "$#" -ne 1 ]; then
    echo "Incorrect arguments provided"
    echo "Run the script from inside the directory you want to copy files to."
    echo "Usage: ./copyFromNodes.sh <folderToCopyFrom>. For example: ./syncNODES.sh src/gap/long_domain"
    exit 1
fi

folder=$1
NODE="typhoon" # the node actually does not play a role becuase the database are all linked so it's the same for all nodes: typhoon, hurricane, splitfire, blackfriars.
USER="vb824"

# working directory in supercomputer
dest="/home/${USER}/Desktop/nektarsim"

rsync -avz -e ssh ${USER}@${NODE}.ae.ic.ac.uk:"${dest}/${folder}" ../
