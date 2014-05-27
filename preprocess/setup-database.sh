# Create empty tables from schema
psql -d $DBNAME < schema.sql

# Load lattice file
pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bdc /tmp/deepspeech-lattices.out

# Load transcripts
pypy load-transcript.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Btr /tmp/deepspeech-transcripts.out

# Load google 1gram
load_google_ngram.py /dfs/hulk/0/zifei/ocr/google-ngram/1gram/ google_1gram $DBNAME

# Data transform
psql -d $DBNAME -c "ANALYZE google_1gram;"

psql -d $DBNAME -c "
  SELECT * INTO google_1gram_reduced 
  FROM google_1gram
  WHERE count >= 1000;
"

# load google 2gram
load_google_ngram_2_reduced.sh /dfs/hulk/0/zifei/ocr/google-ngram/ngram_2_reduced.tsv $DBNAME
