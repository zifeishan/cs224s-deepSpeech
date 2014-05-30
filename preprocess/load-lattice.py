#! /usr/bin/python
# Sample usage: <this> <html_path> <outbase>
# NEW: ignore existing files in output dir

import codecs

import sys, os

'''
Input (bdc): (start 0 end 1 word 2 confirm 3)
19960510_NPR_ATC#Ailene_Leblanc@0001.dc
1 2 <s> confirm=0
3 13 THE confirm=1
3 14 THE confirm=1
14 37 TWO confirm=1
15 36 TWO confirm=1
37 114 HELICOPTERS confirm=1
38 114 HELICOPTERS confirm=1

Input (bnc): (start 0 end 1 word 2 confirm 5)
19960510_NPR_ATC#Ailene_Leblanc@0001.nc
1 2 <s>  0 1 confirm=0
3 13 THE  1 2 confirm=1
3 14 THE  1 3 confirm=1
14 37 TWO  2 5 confirm=1

Input (bbase): (start 1 end -1 word 0 confirm -1)
# end output "0" if not specified
19960510_NPR_ATC#Ailene_Leblanc@0001.base
# baseline
<s> 2
THE 9
TWO 27
HELICOPTERS 77
'''

dbname = 'deepspeech'
path = ''
outfile = '/tmp/deepspeech-lattice.out'
if len(sys.argv) == 9:
  dbname = sys.argv[1]
  path = sys.argv[2]
  outfile = sys.argv[3]
  tablename = sys.argv[4]
  startcol, endcol, wordcol, confirmcol = [int(_) for _ in sys.argv[5:]]
else:
  print 'Usage:',sys.argv[0],'DBNAME LATTICE_FILE OUTPUT_FILE TABLENAME startcol endcol wordcol conformcol'
  print 'e.g. python %s dbname latticefile.Bdc latticefile.Bdc.out candidate_all' % sys.argv[0]
  sys.exit(1)

# if not os.path.exists(outfile):
#   os.makedirs(outfile)

# Parse input lattice
fin = open(path)

fout = open(outfile, 'w') 
fout.close()

num_lattices = 0
candidate_id = 0
while True:
  # Read a lattice
  this_lattice = []

  firstline = fin.readline()
  if firstline == '': break  # ends

  # before: 19960510_NPR_ATC#Ailene_Leblanc@0001.dc
  # after: '19960510_NPR_ATC#Ailene_Leblanc@0001', 'dc'
  tmpname = firstline.strip().rsplit('.', 1)
  assert len(tmpname) == 2

  this_lattice_name, source = tmpname
  # print 'Reading lattice file:', this_lattice_name
  assert '@' in this_lattice_name
  num_lattices += 1
  if num_lattices % 10000 == 0: print 'Reading %dth lattice.' % num_lattices

  while True:
    line = fin.readline()
    if line.startswith('#'): continue
    if line.strip() == '.': break
    
    parts = line.strip().split(' ')
    # assert(len(parts) == 4)
    
    # Read all fields
    start, word = parts[startcol], parts[wordcol]

    end = 0
    if endcol != -1: end = parts[endcol]

    confirm = 0
    if confirmcol != -1: 
      confirm = int(parts[confirmcol].split('=')[-1])

    candidate_id += 1
    this_lattice.append((start, end, word, confirm, candidate_id))

  fout = open(outfile, 'a') 
  for p in this_lattice:
    print >>fout, '\t'.join( [this_lattice_name, source] + [str(x) for x in p])
  fout.close()

os.system('''psql -c """DROP TABLE IF EXISTS err; CREATE TABLE err (cmdtime timestamp with time zone, relname text, filename text, linenum integer, bytenum integer, errmsg text, rawdata text, rawbytes bytea);""" '''+dbname)
os.system('''psql -c "TRUNCATE %s CASCADE;" %s''' % (tablename, dbname))

print 'Loading from', outfile
sqlcmd = '''sed \'s/\\\\/\\\\\\\\/g\' '''+outfile+''' | psql -c "COPY %s(lattice_id,source,starts,ends,word,confirm, candidate_id) FROM STDIN LOG ERRORS INTO err SEGMENT REJECT LIMIT 1000 ROWS;" %s'''  % (tablename, dbname)
print sqlcmd
os.system(sqlcmd)

os.system('''psql -c "ANALYZE %s;" %s''' % (tablename, dbname))
