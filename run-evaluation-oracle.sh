#! /bin/bash

#source "$APP_HOME/setup_database.sh"
export APP_HOME=`pwd`
# export DEEPDIVE_HOME=`cd ../..; pwd`
export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`

export EVAL_BASE=$APP_HOME/speech-data/output/
# source env.sh

# if [ -f $DEEPDIVE_HOME/sbt/sbt ]; then
#   echo "DeepDive $DEEPDIVE_HOME"
# else
#   echo "[ERROR] Could not find sbt in $DEEPDIVE_HOME!"
#   exit 1
# fi

# cd $DEEPDIVE_HOME
# # $DEEPDIVE_HOME/sbt/sbt "run -c $APP_HOME/application.conf"
# deepdive -c $APP_HOME/evaluation.conf

# echo "deduplicating speaker meta..."
# psql -d $DBNAME -c "
# UPDATE lattice_meta m1 
# SET speaker_id = m1.speaker_id || '_0'
# FROM   lattice_meta m2 
# WHERE  m1.speaker_id != m2.speaker_id and lower(m1.speaker_id) =lower (m2.speaker_id)
# and m1.speaker_id < m2.speaker_id;
# "

echo "Exporting lattice data..."

psql --tuples-only -d $DBNAME -c "
select array_to_string(words, ' ') || ' (' || speaker_id || '_' || sentenceid || ')' 
from  output_oracle c,
      lattice_meta m,
      lattices_holdout h
where c.lattice_id = m.lattice_id
  and c.lattice_id = h.lattice_id   -- part of holdout doc
order by c.lattice_id
;" > $EVAL_BASE/oracle-output.trn

# psql --tuples-only -d $DBNAME -c "
# select array_to_string(words, ' ') || ' (' || speaker_id || '_' || sentenceid || ')' 
# from  transcript_array c,
#       lattices_holdout h,
#       lattice_meta m
# where c.lattice_id = m.lattice_id
# and   c.lattice_id = h.lattice_id   -- part of holdout doc
# order by c.lattice_id
# "  > $EVAL_BASE/transcript.trn

echo "Running evaluation script..."
# sclite -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/oracle-output.trn -i wsj
sclite -f 0 -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/oracle-output.trn -i rm >$EVAL_BASE/eval-result-oracle.txt
# sclite -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/oracle-output.trn -i rm >$EVAL_BASE/eval-result-oracle.txt

grep 'SPKR' $EVAL_BASE/eval-result-oracle.txt
grep 'Sum/Avg' $EVAL_BASE/eval-result-oracle.txt

