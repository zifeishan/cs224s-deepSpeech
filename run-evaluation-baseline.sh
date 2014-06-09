#! /bin/bash

#source "$APP_HOME/setup_database.sh"
export APP_HOME=`pwd`
# export DEEPDIVE_HOME=`cd ../..; pwd`
export DEEPDIVE_HOME=`cd $(dirname $0)/../..; pwd`

export EVAL_BASE=$APP_HOME/speech-data/output/
# source env.sh

echo "Exporting lattice data..."

psql --tuples-only -d $DBNAME -c "
select array_to_string(array_agg(word order by starts), ' ') || ' (' || speaker_id || '_' || sentenceid || ')' 
from  candidate_baseline c,
      lattice_meta m,
      lattices_holdout h
where c.lattice_id = m.lattice_id
  and c.lattice_id = h.lattice_id   -- part of holdout doc
GROUP BY c.lattice_id, speaker_id, sentenceid
order by c.lattice_id
;" > $EVAL_BASE/baseline-output.trn

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
# sclite -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/baseline-output.trn -i wsj
sclite -f 0 -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/baseline-output.trn -i rm >$EVAL_BASE/eval-result-baseline.txt
# sclite -r $EVAL_BASE/transcript.trn -h $EVAL_BASE/baseline-output.trn -i rm >$EVAL_BASE/eval-result-baseline.txt

grep 'SPKR' $EVAL_BASE/eval-result-baseline.txt
grep 'Sum/Avg' $EVAL_BASE/eval-result-baseline.txt

