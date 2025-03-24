# create a file with the date and time of the job submission
function uploadDateFile {
    rm -f *.date
    echo "" > $datefile
}
