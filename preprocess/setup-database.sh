psql -d $DBNAME < schema.sql

pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bdc /tmp/deepspeech-lattices.out

# load-transcript.py

# load_google_ngram.py

# load_google_ngram_2_reduced.sh