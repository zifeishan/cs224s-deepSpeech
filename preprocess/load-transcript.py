#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

import codecs

import sys, os

'''
Input:
19960510_NPR_ATC#Ailene_Leblanc@0001.dc
1 2 <s> confirm=0
3 13 THE confirm=1
3 14 THE confirm=1
14 37 TWO confirm=1
15 36 TWO confirm=1
37 114 HELICOPTERS confirm=1
38 114 HELICOPTERS confirm=1
'''

dbname = 'deepspeech'
path = ''
outfile = '/tmp/deepspeech-transcript.out'
if len(sys.argv) == 4:
  dbname = sys.argv[1]
  path = sys.argv[2]
  outfile = sys.argv[3]
else:
  print 'Usage:',sys.argv[0],'DBNAME TR_FILE OUTPUT_FILE'
  print 'e.g. python %s deepspeech /dfs/madmax/0/zifei/LDC2011T06/data/Train/train.Btr /tmp/deepspeech-transcript.out' % sys.argv[0]
  sys.exit(1)

# if not os.path.exists(outfile):
#   os.makedirs(outfile)

# Parse input transcript
fin = open(path)

fout = open(outfile, 'w') 
fout.close()

num_transcripts = 0
candidate_id = 0
while True:
  # Read a transcript
  this_transcript = []

  firstline = fin.readline()
  if firstline == '': break  # ends

  # before: 19960510_NPR_ATC#Ailene_Leblanc@0001.dc
  # after: '19960510_NPR_ATC#Ailene_Leblanc@0001', 'dc'
  tmpname = firstline.strip().rsplit('.', 1)
  assert len(tmpname) == 2

  this_lattice_name, source = tmpname
  # print 'Reading transcript file:', this_lattice_name
  assert '@' in this_lattice_name
  num_transcripts += 1
  if num_transcripts % 10000 == 0: print 'Reading %dth lattice transcript.' % num_transcripts

  while True:
    line = fin.readline()
    if line.strip() == '.': break
    
    words = line.strip().split(' ')
    for i in range(len(words)):
      this_transcript.append((i, words[i]))

  fout = open(outfile, 'a') 
  for p in this_transcript:
    print >>fout, '\t'.join( [this_lattice_name] + [str(x) for x in p])
  fout.close()

os.system('''psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname)
os.system('''psql -c "TRUNCATE transcript CASCADE;" '''+dbname)

print 'Loading from', outfile
sqlcmd = '''sed \'s/\\\\/\\\\\\\\/g\' '''+outfile+''' | psql -c "COPY transcript FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" '''+ dbname
print sqlcmd
os.system(sqlcmd)

os.system('''psql -c "ANALYZE transcript;" '''+dbname)

sqlcmd = '''INSERT INTO transcript_array
  SELECT  lattice_id, 
          ARRAY_AGG(word ORDER BY wordid) AS words
  FROM    transcript
  GROUP BY lattice_id;
''' + dbname

os.system(sqlcmd)
os.system('''psql -c "ANALYZE transcript_array;" '''+dbname)
