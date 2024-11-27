# # copy the files to IDRIS
date=$(date +"%Y%m%d") # current date

# prompt a message if there are less or more than 1 argument
if [ "$#" -ne 1 ]; then
    echo "Incorrect arguments provided"
    echo "Usage: ./copyToNodes.sh <folderToCopyToNodes>. For example: ./copyToICHPC.sh src/ganlintutorial"
    exit 1
fi

folder=$1
HPC="login.hpc" # the node actually does not play a role becuase the database are all linked so it's the same for all nodes: typhoon, hurricane, splitfire, blackfriars.
USER="vb824"

# working directory in supercomputer
dest="~/Desktop/nektarsim"

folder_prev_dir=$(dirname ${folder})

# get the path direftory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd ${DIR}/..

rsync -avz -e ssh ${folder} ${DIR}/sendMessage.py ${DIR}/run.sh ${USER}@${HPC}.imperial.ac.uk:${dest}/${folder_prev_dir}

rsync -avz -e ssh ${DIR}/sendMessage.py ${DIR}/run.sh ${USER}@${HPC}.imperial.ac.uk:${dest}/${folder}
rsync -avz -e ssh ${USER}@${HPC}.imperial.ac.uk:${dest}/${folder}


# # create a tar file of that folder
# tar -cvzf ${date}.tar ${folder}

# # destination in nodes database
# scp ${date}.tar ${USER}@${HPC}.ae.ic.ac.uk:${dest} 

# # we enter in gauss and then in IDRIS
# # 'ssh -t ${USER}@${HPC}.ae.ic.ac.uk' prevents the loading of the .bash_profile, and so we avoid loading the modules each time
# ssh -t ${USER}@${HPC}.ae.ic.ac.uk /bin/sh << EOF
#   cd ${dest}
#   # remove current directories
#   # rm -Rf -- */
#   tar -xvzf ${date}.tar
#   rm ${date}.tar
# EOF

# scp ${DIR}/sendMessage.py ${USER}@${HPC}.ae.ic.ac.uk:${dest}/${folder}
# scp ${DIR}/run.sh ${USER}@${HPC}.ae.ic.ac.uk:${dest}/${folder}

# # remove the tar file
# rm ${date}.tar
