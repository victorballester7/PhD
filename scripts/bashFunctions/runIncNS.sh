function runIncNS {
    # execute python script if job is cancelled
    # trapCancel

    # Run the job start script
    python3 $SCRIPTS_DIR/jobStart.py $JOB_ID

    mpirun --timeout $TIMEMAX -np $NP $INC_SOLVER -v $mesh_file $session_file > $output_file 2> $log_file

    python3 $SCRIPTS_DIR/jobFinish.py $JOB_ID
}
