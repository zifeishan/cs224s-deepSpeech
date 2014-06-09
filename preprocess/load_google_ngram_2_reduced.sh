if [ $# != 2 ]; then
  echo "Usage: $0 tsv_path DBNAME"
  exit
fi

psql -c "
  DROP TABLE IF EXISTS google_2gram_reduced CASCADE;
  
  CREATE TABLE google_2gram_reduced(
    id bigint,
    gram text,
    count real
    ) DISTRIBUTED BY (gram);
" $2

psql -c "
COPY google_2gram_reduced FROM STDIN;
" $2 < $1

psql -c "
ANALYZE google_2gram_reduced;
" $2
