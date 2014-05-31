#! /usr/bin/python

import ddext
from ddext import SD
from ddext import plpy

# Import query:
'''
SELECT    c.lattice_id AS lattice_id,
          ARRAY_AGG(c.starts ORDER BY starts, ends)  AS starts,
          ARRAY_AGG(c.ends   ORDER BY starts, ends)  AS ends,
          ARRAY_AGG(c.word   ORDER BY starts, ends)  AS candidates,
          ARRAY_AGG(c.candidate_id ORDER BY starts, ends) AS candidate_ids,
          ARRAY_AGG(c.expectation ORDER BY starts, ends) AS expectations
FROM      candidate_is_true_inference  c
GROUP BY  c.lattice_id;
'''

def init():
  ddext.input('lattice_id', 'text')
  ddext.input('starts', 'bigint[]')
  ddext.input('ends', 'bigint[]')
  ddext.input('candidates', 'text[]')
  ddext.input('candidate_ids', 'bigint[]')
  ddext.input('expectations', 'float[]')

  ddext.returns('lattice_id', 'text')
  ddext.returns('words', 'text[]')

def run(lattice_id, starts, ends, candidates, candidate_ids, transcript):

  def orderedLattice(cids, edges):
    # generate a topological ordered words
    lattice_ordered = []  
    visited = set()
    indegree = {}
    for i in cids:
      indegree[i] = 0
    for k in edges:
      for e in edges[k]:
        if e not in indegree:
          indegree[e] = 0
        indegree[e] += 1
    # print indegree
    for e in indegree:
      if indegree[e] == 0:
        visited.add(e)
    # print visited
    while len(visited) > 0:
      n = visited.pop()  
      lattice_ordered.append(n)
      if n in edges:
        for e in edges[n]:
          indegree[e] -= 1
          if indegree[e] == 0:
            visited.add(e)
    return lattice_ordered

  # DEBUG function
  def PrintStatus(f, path, message=''): 
    # if message != '': print message
    # print 'F score:'
    # print '\n'.join([str(_) for _ in f])
    # print 'Path:'
    # for p in path:
    #   for pairlist in p:
    #     print '[%20s]' % ', '.join([str('(%d,%d)' % pair) for pair in pairlist]),
    #   print ''
    # raw_input()
    pass


  # Only return 1 path that has highest score. 
  # Break ties by ID order. (small wins)
  def FindBestPath(lattice_words, edges, candidate_ids, index_cid_sub, expectations, start_subs):
    # F: longest matching up to ith element from lattice_words and and jth from trans_words
    n1 = len(lattice_words)
    if n1 == 0: 
      return 0, []

    f = [-10000000.0 for _ in range(n1)]    # f[sub] ->score
    path = [-1 for _ in range(n1)]  # stores index: f[sub] -> lastsub

    # init f of startnodes to be 0
    for i in start_subs: f[i] = 0.0

    ordered_cids = orderedLattice(candidate_ids, edges)

    for i_cid in ordered_cids:
      i = index_cid_sub[i_cid]
      f[i] += expectations[i]     # increase itself
      for j_cid in edges[i_cid]:  # i -> j
        j = index_cid_sub[j_cid]
        if f[j] < f[i]:
          f[j] = f[i]
          path[j] = i


    # Only match "diagonal" edges
    possible_opt_match_pairs = []  # can have cases like [(1,a) (2,a)] but have to be both optimal!
    visited = set()

    # F matrix might look like this:
    # [1, 1, 1]
    # [1, 1, 1]
    # [1, 1, 2]
    # [0, 0, 0]
    # [0, 1, 1]
    # [1, 1, 1]
    # So we just pick one best end-nodes (simplified for "1" best path)
    endnodes = [index_cid_sub[i] for i in edges if len(edges[i]) == 0]
    maxscore = 0
    besti = -1
    for i in endnodes:
      if maxscore < f[i]:
        maxscore = f[i]
        besti = i
      # elif maxscore == f[i][n2 - 1]:
      #   besti.append(i)

    i = besti
    bestpath = []
    while i != -1:
      bestpath.append(i)
      i = path[i]

    # indexes are sorted by "start,end ".
    return maxscore, [lattice_words[i] for i in sorted(bestpath)]

    # return maxscore, [x for x in reversed(possible_opt_match_pairs)], path, f


  # Build graph
  def AddEdge(edges, f, t):
    if f not in edges:
      edges[f] = []
    edges[f].append(t)

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
  for cid in index_cid_sub: edges[cid] = []
  
  indegree = [0 for i in range(N)]

  for i in range(N):
    start = starts[i]
    end = ends[i]
    if end + 1 in index_start_sub:
      for j in index_start_sub[end + 1]:
        AddEdge(edges, candidate_ids[i], candidate_ids[j])
        indegree[j] += 1

  start_subs = [i for i in range(len(indegree)) if indegree[i] == 0]

  ############# 2. Return DP result

  # If expectation array is empty, fill it with 1 (for oracle)
  exp = [ e - 0.5 for e in expectations]
  if len(expectations) == 0: exp = [0.5 for _ in range(len(candidates))]
  score, words = FindBestPath(candidates, \
    edges, candidate_ids, index_cid_sub, exp, start_subs)

  # plpy.info('[%s]  SCORE: %d, Words: %s...' % (lattice_id, score, (' '.join(words))[:30]))
  yield lattice_id, words


# ### Testing
# # TODO parse indents.. Cannot be in this part of comments :(
# def test(lattice_id, starts, ends, words, cids, expectations, expected_score, expected_cand):
#   print 'Testing:', words, 'against', expectations
#   # for p in run(lattice_id, starts, ends, words, cids, gramlen):
#   #   print p
#   true_num = 0
#   for item in run(lattice_id, starts, ends, words, cids, expectations):
#     print 'Returned item:',item
#     if item[2]: true_num += 1
#   print 'Expected score: %d. check manually.' % expected_score
#   if expected_cand == true_num:
#     print 'Passed.'
#     return 0
#   else:
#     print 'FAILED: True candnum expected %d got %d' % (expected_cand, true_num)
#     raw_input()
#     return 1

# if __name__ == '__main__':
#   import time
#   lattice_id = 'test_lattice'
#   errors = 0

#   # Assume ordered by starts then ends

#   starts = [1,     3,     5   ]
#   ends =   [2,     4,     6   ]
#   words =  ['not', 'at', 'all']
#   cids =   [1001,  1002,  1003]
#   transcript = ['not',  'at',  'all']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 3)
  

#   starts = [1,     3,     5   ]
#   ends =   [4,     4,     6   ]
#   words =  ['not', 'at', 'all']
#   cids =   [1001,  1002,  1003]
#   transcript = ['not',  'at',  'all']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 3)
  

#   starts = [1,     3,     6,    1,    4,     6    ]
#   ends =   [2,     5,     7,    3,    5,     7    ]
#   words =  ['not', 'tai', 'all','now','at','tao'  ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['not',  'at',  'all']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 3)
#   # Expected result: not (tai) all,  (now) at all
  

#   starts = [1,     3,     5,    1,    4,     6    ]
#   ends =   [2,     4,     6,    3,    5,     7    ]
#   words =  ['not', 'tai', 'all','now','at','tao'  ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['not',  'at',  'all']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 2)

#   # X grid in the middle
#   starts = [  1,   2,     2,    3,      3  ,  4    ]
#   ends =   [  1,   2,     2,    3,      3  ,  4    ]
#   words =  ['A',   'B', 'X',  'X',      'B', 'C'   ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['A','B','C']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 4)

#   starts = [  1,   2,     2,    3,      3  ,  4    ]
#   ends =   [  1,   2,     2,    3,      3  ,  4    ]
#   words =  ['A',   'B', 'C',  'C',      'B', 'D'   ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['A','B','C','D']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 4)

#   # Two single paths: ABXC, AXBC
#   starts = [  1,   2,     4,    2,      5  ,  7    ]
#   ends =   [  1,   3,     6,    4,      6  ,  7    ]
#   words =  ['A',   'B', 'X',  'X',      'B', 'C'   ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['A','B','C']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 4)

#   # ABCD, ACBD
#   starts = [  1,   2,     4,    2,      5  ,  7    ]
#   ends =   [  1,   3,     6,    4,      6  ,  7    ]
#   words =  ['A',   'B', 'C',  'C',      'B', 'D'   ]
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
#   transcript = ['A','B','C','D']
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 4)

#   # ABCD, ACBD
#   starts = [  1,   2,   2,   3,   4,   4,   5      ]
#   ends =   [  1,   2,   2,   3,   4,   4,   5      ]
#   words =  'A B D C C X E'.split(' ')
#   cids =   [1001,  1002,  1003, 1004, 1005,  1006, 1007 ]
#   transcript = ['A','B','C','D','E']
#   # Should match anything but 3 and 6
#   errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 5)


#   if errors == 0: print 'ALL TESTS PASSED!!'
#   else: print 'FOUND %d ERRORS!!' % errors
