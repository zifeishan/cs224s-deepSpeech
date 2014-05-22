psql -d $DBNAME < schema.sql

pypy load-lattice.py $DBNAME ~/zifei/LDC2011T06/data/Train/train.Bdc /tmp/deepspeech-lattices.out
