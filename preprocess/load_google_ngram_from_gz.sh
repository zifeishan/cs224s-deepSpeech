# e.g. bash load_google_ngram_from_gz.sh /afs/cs/group/infolab/datasets/snap-private/web1T5gram/data/4gms/ deepspeech google_4gram

if [ $# != 3 ]; then
  echo "Usage: $0 gz_folder DBNAME table_name FILTER_COUNT"
  echo "e.g. $0 /afs/cs/group/infolab/datasets/snap-private/web1T5gram/data/3gms/ deepspeech google_3gram"
  exit
fi
INPUT=$1
DBNAME=$2

psql -c "
  DROP TABLE IF EXISTS $3 CASCADE;
  
  CREATE TABLE $3(
    gram text,
    count real
    ) DISTRIBUTED BY (gram);
" $DBNAME

psql -c "
DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);
" $DBNAME

# Sample
# find $INPUT -name "*0000.gz" -print0 | xargs -0 -L 1 -P 1 zcat $0 | awk -F "\t" '{if ($2 >= 10000) print $0}' | sed 's/\\/\\\\/g' | psql -c "COPY $3 FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 100000 ROWS;" -d $DBNAME
find $INPUT -name "*.gz" -print0 | xargs -0 -L 1 -P 1 zcat $0 | awk -F "\t" '{if ($2 >= 10000) print $0}' | sed 's/\\/\\\\/g' | psql -c "COPY $3 FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 100000 ROWS;" -d $DBNAME

psql -c "
ANALYZE $3;
" $DBNAME
