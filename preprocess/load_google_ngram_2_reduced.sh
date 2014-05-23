if [ $# != 2 ]; then
  echo "Usage: $0 tsv_path DBNAME"
  exit
fi

psql -c "
  DROP TABLE IF EXISTS ngram_2_reduced CASCADE;
  
  CREATE TABLE ngram_2_reduced(
    id bigint,
    gram text,
    count real
    ) DISTRIBUTED BY (gram);
" $2

psql -c "
COPY ngram_2_reduced FROM STDIN;
" $2 < $1
