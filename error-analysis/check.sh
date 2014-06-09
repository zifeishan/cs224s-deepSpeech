DDOUT=../speech-data/output/dd-output.trn
TRANS=../speech-data/output/transcript.trn
head -n 100 $DDOUT | bash ./splitlines.sh >dd-output.txt
head -n 100 $TRANS | bash ./splitlines.sh >transcript.txt

vimdiff dd-output.txt transcript.txt