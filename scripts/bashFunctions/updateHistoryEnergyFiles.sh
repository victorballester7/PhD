function updateHistoryEnergyFiles {
    filenameHis="HistoryPoints.his"
    filenameE="EnergyFile.mdl"


    if [[ -f "${filenameHis}.old" ]]; then
        grep -v '^#' "$filenameHis" >> "${filenameHis}.old"
        rm "$filenameHis"
    else
        mv "$filenameHis" "${filenameHis}.old"
    fi


    if [[ -f "${filenameE}.old" ]]; then
        grep -v '^#' "$filenameE" >> "${filenameE}.old"
        rm "$filenameE"
    else
        mv "$filenameE" "${filenameE}.old"
    fi
    
}

