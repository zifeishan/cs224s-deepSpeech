#! /usr/bin/python

import ddext
from ddext import SD
from ddext import plpy

# Import query:
"""
  SELECT distinct lattice_id 
  FROM transcript_array;
"""

# Output schema
'''
CREATE TABLE lattice_meta (
    lattice_id    TEXT,     -- which lattice (document) it belongs
    speaker_id    TEXT,     -- speaker's identifier
    sentenceid    TEXT      -- which sentence for this speaker
    )  DISTRIBUTED BY (lattice_id);
'''

def init():
  ddext.import_lib('re')
  ddext.input('lattice_id', 'text')

  ddext.returns('lattice_id', 'text')
  ddext.returns('speaker_id', 'text')
  ddext.returns('sentenceid', 'text')

def run(lattice_id):
  parts = lattice_id.split('@')
  assert len(parts) == 2
  speaker_id = re.sub('_|-', '', parts[0])
  sentenceid = parts[1]
  yield lattice_id, speaker_id, sentenceid
