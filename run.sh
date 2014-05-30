#! /bin/bash

#source "$APP_HOME/setup_database.sh"
export APP_HOME=`pwd`
# export DEEPDIVE_HOME=`cd ../..; pwd`
export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`

export SAMPLE_SIZE=1000

if [ $# = 1 ]; then          # Export Sample size from command line
  echo "Set sample size to: $1"
  export SAMPLE_SIZE=$1
fi

# source env.sh

if [ -f $DEEPDIVE_HOME/sbt/sbt ]; then
  echo "DeepDive $DEEPDIVE_HOME"
else
  echo "[ERROR] Could not find sbt in $DEEPDIVE_HOME!"
  exit 1
fi

cd $DEEPDIVE_HOME
# $DEEPDIVE_HOME/sbt/sbt "run -c $APP_HOME/application.conf"
deepdive -c $APP_HOME/application.conf

# # remove the results file for evaluation
# rm $EL_RESULTS_FILE
# touch $EL_RESULTS_FILE

# # after inference is done, populate the results file
# source "$APP_HOME/populate_results.sh"

# # run the EL evaluation script
# perl $APP_HOME/evaluation/entity-linking/kbpenteval.pl $APP_HOME/evaluation/entity-linking/el_2010_eval_answers.tsv $APP_HOME/evaluation/entity-linking/results/out.tsv

# # run the RE evaluation script
# source $APP_HOME/evaluation/slotfilling/evaluate.sh 2010

## Evaluation
# psql -d $DBNAME < $APP_HOME/evaluation/evaluation.sql