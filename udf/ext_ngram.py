#! /usr/bin/python

import ddext
from ddext import SD
from ddext import plpy

# Import query:
'''
        SELECT    lattice_id,
                  ARRAY_AGG(starts ORDER BY starts, ends)  AS starts,
                  ARRAY_AGG(ends   ORDER BY starts, ends)  AS ends,
                  ARRAY_AGG(word   ORDER BY starts, ends)  AS words,
                  ARRAY_AGG(candidate_id ORDER BY starts, ends) AS candidate_ids,
                  2 as gram_len
        FROM      candidate
        GROUP BY  lattice_id;

'''

def init():
  ddext.input('lattice_id', 'text')
  ddext.input('starts', 'bigint[]')
  ddext.input('ends', 'bigint[]')
  ddext.input('arr_feature', 'text[]')
  ddext.input('candidate_ids', 'bigint[]')
  ddext.input('gram_len', 'bigint')

  ddext.returns('lattice_id', 'text')
  ddext.returns('candidate_id', 'bigint')
  ddext.returns('ngram', 'text')
  ddext.returns('skipping', 'boolean')

# TODO CANNOT "def raaaan"?!
def run(lattice_id, starts, ends, arr_feature, candidate_ids, gram_len):
  # Store functions
  if 'AddEdge' in SD:
    AddEdge = SD['AddEdge']
  else:
    # allow multiple same edges
    def AddEdge(edges, f, t):
      if f not in edges:
        edges[f] = []
      edges[f].append(t)
    SD['AddEdge'] = AddEdge


  if 'skipset' in SD:
    skipset = SD['skipset']
  else:
    skipset = set(['~SIL', '<s>', '</s>'])
    SD['skipset'] = skipset


  if 'DFS' in SD:
    DFS = SD['DFS']
  else:

    # Start with DFS(edges, id, 1)
    def DFS(lattice_id, edges, nowid, res_array, index_cid_sub, skipping=False):

      # Reaches N, finish generated a N-gram. 
      if len(res_array) == gram_len:
        feature_tmp = []
        for cwid in res_array:
          sub = index_cid_sub[cwid]
          # Deal with range problem
          if sub >= len(arr_feature):
            plpy.info('OUT OF RANGE:' + str(arr_feature[:10]))
          else:
            feature_tmp.append(arr_feature[sub])
        feature = ' '.join([f for f in feature_tmp])
        for cwid in res_array:
          # print lattice_id + '\t' + str(cwid) + '\t' + feature
          yield lattice_id, cwid, feature, skipping
        return
      
      if nowid not in edges: return
      
      for jid in edges[nowid]:
        next_word = arr_feature[index_cid_sub[jid]]
        
        if skipping: # already skipgram, don't generate nonskipgram.
          if next_word in skipset:
            # for item in DFS(lattice_id, edges, jid, res_array, index_cid_sub, skipping=True):
            #   yield item
            pass  # rule: can only skip once...
          else:
            res_array.append(jid)
            for item in DFS(lattice_id, edges, jid, res_array, index_cid_sub, skipping=True):
              yield item
            res_array.pop()
        else:  # not skipping
          if next_word in skipset: # branch into two!
            # Skipgram
            for item in DFS(lattice_id, edges, jid, res_array, index_cid_sub, skipping=True):
              yield item
            # Nonskipgram
            res_array.append(jid)
            for item in DFS(lattice_id, edges, jid, res_array, index_cid_sub, skipping=False):
              yield item
            res_array.pop()
          else:
            # nonskipgram
            res_array.append(jid)
            for item in DFS(lattice_id, edges, jid, res_array, index_cid_sub, skipping=False):
              yield item
            res_array.pop()


    SD['DFS'] = DFS

  ################## MAIN FUNCTION ####################

  N = len(candidate_ids)  # number of words
  if N == 0:
    plpy.info('Empty data:'+str(lattice_id))
    return

  # Build index for candidate_id
  index_cid_sub = {}
  for sub in range(N):
    cid = candidate_ids[sub]
    index_cid_sub[cid] = sub

  # Build index
  index_start_sub = {}
  for sub in range(N):
    start = starts[sub]
    if start not in index_start_sub: 
      index_start_sub[start] = []
    index_start_sub[start].append(sub)

  ######### 1. build directed graph

  # Note that input is sorted by (start, end)
  last_start = starts[0]
  last_end   = ends[0]
  last_candidate_id = -1
  
  edges = {}  # cand_word_id1 : [cand_word_id2]

  for i in range(N):
    start = starts[i]
    end = ends[i]
    if end + 1 in index_start_sub:
      for j in index_start_sub[end + 1]:
        AddEdge(edges, candidate_ids[i], candidate_ids[j])

  print edges
  ######## 2. DFS output candidates
  res_array = []
  for startid in sorted(edges.keys()):
    res_array.append(startid)
    for item in DFS(lattice_id, edges, startid, res_array, index_cid_sub):
      yield item
    res_array.pop()

### Testing
# TODO parse indents.. Cannot be in this part of comments :(
def test(lattice_id, starts, ends, words, cids, gramlen):
  for p in run(lattice_id, starts, ends, words, cids, gramlen):
    print p

if __name__ == '__main__':
  import time
  lattice_id = 'test_lattice'

  # starts = [1,     3,     5   ]
  # ends =   [4,     4,     6   ]
  # words =  ['not', 'at', 'all']
  # cids =   [1001,  1002,  1003]
  # transcript = ['not',  'at',  'all']
  # test(lattice_id, starts, ends, words, cids, 2)
  

  # starts = [1,     3,     6,    1,    4,     6    ]
  # ends =   [2,     5,     7,    3,    5,     7    ]
  # words =  ['not', 'tai', 'all','now','at','tao'  ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['not',  'at',  'all']
  # test(lattice_id, starts, ends, words, cids, 2)
  

  starts = [1,     3,     5,    1,    4,     6    ]
  ends =   [2,     4,     6,    3,    5,     7    ]
  words =  ['not', '~SIL', 'all','now','at','tao'  ]
  cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  transcript = ['not',  'at',  'all']
  test(lattice_id, starts, ends, words, cids, 2)


  # Weird yield issue...
