echo "Usage: $0 EXP_NAME SAMPLE_SIZE"
./run.sh $2
./run-evaluation.sh
./save-experiment.sh $1

