DATE=`ls -t ../../out/ | head -n 1`
mkdir -p experiments/${DATE}-$1
cp -r ../../out/${DATE}/calibration experiments/${DATE}-$1/calibration  # comment in $1
cp -r application.conf experiments/${DATE}-$1/configuration.conf
psql -d $DBNAME -c "select * 
from dd_inference_result_variables_mapped_weights 
order by weight desc" > experiments/${DATE}-$1/weights.txt