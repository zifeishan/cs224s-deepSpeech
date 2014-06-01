# # Create empty tables from schema
# psql -d $DBNAME < schema.sql
# if [ "$?" != "0" ]; then echo "[10] FAILED!"; exit 1; fi

# # Load lattice file
# pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bdc /tmp/deepspeech-lattices.out candidate_all 0 1 2 3
# if [ "$?" != "0" ]; then echo "[20] FAILED!"; exit 1; fi

# # Load transcripts
# pypy load-transcript.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Btr /tmp/deepspeech-transcripts.out
# if [ "$?" != "0" ]; then echo "[30] FAILED!"; exit 1; fi

# # Load google 1gram
# load_google_ngram.py /dfs/hulk/0/zifei/ocr/google-ngram/1gram/ google_1gram $DBNAME
# if [ "$?" != "0" ]; then echo "[40] FAILED!"; exit 1; fi

# # Data transform
# psql -d $DBNAME -c "ANALYZE google_1gram;"
# if [ "$?" != "0" ]; then echo "[50] FAILED!"; exit 1; fi

# psql -d $DBNAME -c "
#   SELECT * INTO google_1gram_reduced 
#   FROM google_1gram
#   WHERE count >= 1000;
# "
# if [ "$?" != "0" ]; then echo "[60] FAILED!"; exit 1; fi

# # load google 2gram
# load_google_ngram_2_reduced.sh /dfs/hulk/0/zifei/ocr/google-ngram/ngram_2_reduced.tsv $DBNAME
# if [ "$?" != "0" ]; then echo "[70] FAILED!"; exit 1; fi

# Load Baseline lattice file
# pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bbase /tmp/deepspeech-lattices-base.out candidate_baseline 1 -1 0 -1
# if [ "$?" != "0" ]; then echo "[80] FAILED!"; exit 1; fi

# # Load lattice file
# pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bnc /tmp/deepspeech-lattices-oracle.out candidate_oracle 0 1 2 5
# if [ "$?" != "0" ]; then echo "[90] FAILED!"; exit 1; fi

export WEBNGRAMDIR=/afs/cs/group/infolab/datasets/snap-private/web1T5gram/data/

bash load_google_ngram_from_gz.sh $WEBNGRAMDIR/3gms/ $DBNAME web3gram
if [ "$?" != "0" ]; then echo "[100] FAILED!"; exit 1; fi

bash load_google_ngram_from_gz.sh $WEBNGRAMDIR/4gms/ $DBNAME web4gram
if [ "$?" != "0" ]; then echo "[110] FAILED!"; exit 1; fi

bash load_google_ngram_from_gz.sh $WEBNGRAMDIR/5gms/ $DBNAME web5gram
if [ "$?" != "0" ]; then echo "[120] FAILED!"; exit 1; fi 
