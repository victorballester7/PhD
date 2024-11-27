#!/bin/bash
date=$(date +"%Y%m%d") # current date

# prompt a message if there are less or more than 1 argument
if [ "$#" -ne 1 ]; then
    echo "Incorrect arguments provided"
    echo "Usage: ./copyToNodes.sh <folderToCopyToNodes>. For example: ./syncNODES.sh src/ganlintutorial"
    exit 1
fi

folder=$1
NODE="typhoon" # the node actually does not play a role becuase the database are all linked so it's the same for all nodes: typhoon, hurricane, splitfire, blackfriars.
USER="vb824"

# working directory in supercomputer
dest="/home/${USER}/Desktop/PhD"

folder_prev_dir=$(dirname ${folder})

# get the path direftory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd ${DIR}/..

rsync -avz -e ssh ${folder} ${USER}@${NODE}.ae.ic.ac.uk:${dest}/${folder_prev_dir}

rsync -avz -e ssh ${DIR}/sendMessage.py ${USER}@${NODE}.ae.ic.ac.uk:${dest}/${folder}
rsync -avz -e ssh ${DIR}/run.sh ${USER}@${NODE}.ae.ic.ac.uk:${dest}/${folder}


# # create a tar file of that folder
# tar -cvzf ${date}.tar ${folder}

# # destination in nodes database
# scp ${date}.tar ${USER}@${NODE}.ae.ic.ac.uk:${dest} 

# # we enter in gauss and then in IDRIS
# # 'ssh -t ${USER}@${NODE}.ae.ic.ac.uk' prevents the loading of the .bash_profile, and so we avoid loading the modules each time
# ssh -t ${USER}@${NODE}.ae.ic.ac.uk /bin/sh << EOF
#   cd ${dest}
#   # remove current directories
#   # rm -Rf -- */
#   tar -xvzf ${date}.tar
#   rm ${date}.tar
# EOF

# scp ${DIR}/sendMessage.py ${USER}@${NODE}.ae.ic.ac.uk:${dest}/${folder}
# scp ${DIR}/run.sh ${USER}@${NODE}.ae.ic.ac.uk:${dest}/${folder}

# # remove the tar file
# rm ${date}.tar
