./run.sh $2
echo "Evaluating DeepSpeech..."
./run-evaluation.sh
echo "Evaluating Baseline..."
./run-evaluation-baseline.sh
echo "Evaluating Oracle..."
./run-evaluation-oracle.sh
echo "Saving experiment result..."
./save-experiment.sh $1
