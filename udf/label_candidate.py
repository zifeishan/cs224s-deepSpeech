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
          max(t.words) AS transcript
FROM      candidate  c, 
          transcript_array t
WHERE     t.lattice_id = c.lattice_id
GROUP BY  c.lattice_id;
'''

def init():
  ddext.input('lattice_id', 'text')
  ddext.input('starts', 'bigint[]')
  ddext.input('ends', 'bigint[]')
  ddext.input('candidates', 'text[]')
  ddext.input('candidate_ids', 'bigint[]')
  ddext.input('transcript', 'text[]')

  ddext.returns('lattice_id', 'text')
  ddext.returns('candidate_id', 'bigint')
  ddext.returns('is_true', 'boolean')

def run(lattice_id, starts, ends, candidates, candidate_ids, transcript):

  def ElemMatch(e1, e2):
    return e1 == e2

  # preDic: preDic[e] = [b,c,d] (b->e; c->e; d->e)
  def invertEdges(edges, index_cid_sub):
    preDic = {}
    for k in edges:
      for e in edges[k]:
        sub_e = index_cid_sub[e] 
        sub_k = index_cid_sub[k]
        preDic[sub_e].append(sub_k)
    return preDic

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
    if message != '': print message
    print 'F score:'
    print '\n'.join([str(_) for _ in f])
    print 'Path:'
    for p in path:
      for pairlist in p:
        print '[%20s]' % ', '.join([str('(%d,%d)' % pair) for pair in pairlist]),
      print ''
    raw_input()
    pass


  # check if edge exists
  # lattice_words: candidates (words in lattice)
  # trans_words: transcript words 
  def MatchTranscriptWithLattice(lattice_words, trans_words, edges, candidate_ids, index_cid_sub):
    # F: longest matching up to ith element from lattice_words and and jth from trans_words
    n1 = len(lattice_words)
    n2 = len(trans_words)
    if n1 == 0 or n2 == 0: 
      return 0, [], []
    # f = [[0] * (n2)] * (n1)  # Python array is weird....
    f = [[0.0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!  
    # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}
    # an "array" for each grid in matrix
    path = [[[] for _2 in range(n2)] for _ in range(n1)]

    indegree = {}

    #indegree stores cids
    for i in candidate_ids:
      indegree[i] = 0
    for k in edges:
      for e in edges[k]:
        if e not in indegree:
          indegree[e] = 0
        indegree[e] += 1

    zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] == 0]
    non_zero_indegree_index = [index_cid_sub[i] for i in indegree if indegree[i] != 0]

    # print 'Zero indegree indexes:',zero_indegree_index

    # Simpler init
    # Initialize zero-indegree with j=0
    for i_zero in zero_indegree_index:
      for j in range(n2):
        if ElemMatch(lattice_words[i_zero], trans_words[j]):
          f[i_zero][j] = 1.0
          path[i_zero][j].append((-1, -1)) # match
    
    # # Init
    # # Initialize zero-indegree with j=0
    # for i_zero in zero_indegree_index:
    #   if ElemMatch(lattice_words[i_zero], trans_words[0]):
    #     f[i_zero][0] = 1
    #     path[i_zero][0].append((-1, -1)) # match

    # # Update successors (redundant?)
    # ordered_cids = orderedLattice(candidate_ids, edges)
    # print 'Ordered Lattice:', ordered_cids
    # # raw_input()
    # for i_cid in ordered_cids:
    #   i = index_cid_sub[i_cid]
    #   # For each successor of i
    #   for i_succ_cid in edges[i_cid]:
    #     i_succ_index = index_cid_sub[i_succ_cid]

    #     if ElemMatch(lattice_words[i_succ_index], trans_words[0]):
    #       f[i_succ_index][0] = 1
    #       path[i_succ_index][0].append((i, -1))
    #     elif f[i][0] == 1:
    #       f[i_succ_index][0] = 1
    #       path[i_succ_index][0].append((i, 0))

    # # Update j with j-1
    # for j in range(1, n2):
    #   for i_zero in zero_indegree_index:
    #     if ElemMatch(lattice_words[i_zero], trans_words[j]):
    #       f[i_zero][j] = 1
    #       path[i_zero][j].append((-1, j-1))
    #     elif f[i_zero][j-1] == 1:
    #       f[i_zero][j] = 1
    #       path[i_zero][j].append((i_zero, j-1))
   
    PrintStatus(f, path, 'Initialization results:')

    # DP; max over predecessors
    # C[i,j] = max over all i'-> i (predecessor) {  f[i', j-1]+ 1{words[i] == transcript[j]}
    #     f[i',j]
    #     f[i,j-1]
    #   }
    ordered_cids = orderedLattice(candidate_ids, edges)

    # Update: treat sub/del/ins equally
    # for i_index in range(0, n1):
    for i_cid in ordered_cids:     # Must have topological order for DP
      for j in range(0, n2):
        # i_cid = candidate_ids[i_index]
        i_index = index_cid_sub[i_cid]

        # TODO edges stores cids; i_succ_index is cid!!! i_index is index
        for i_succ_cid in edges[i_cid]:
          i_succ_index = index_cid_sub[i_succ_cid]
          word_succ = lattice_words[i_succ_index]
          if i_succ_index < n1 and j+1 < n2 \
            and ElemMatch(word_succ, trans_words[j+1]):
              newscore = (f[i_index][j] * (j+1.) + 1.) / (j+2.)
              if f[i_succ_index][j+1] < newscore:
                f[i_succ_index][j+1] = newscore
                path[i_succ_index][j+1] = [(i_index,j)]    # Path stores index :P
              elif f[i_succ_index][j+1] == newscore:
                path[i_succ_index][j+1].append((i_index,j))

          # TODO consider insertion!! This is insertion!
          if i_succ_index < n1: # shift down (to successor)
            if f[i_succ_index][j] < f[i_index][j]:
              f[i_succ_index][j] = f[i_index][j]
              path[i_succ_index][j] = [(i_index, j)]
            elif f[i_succ_index][j] == f[i_index][j]: # another best path
              path[i_succ_index][j].append((i_index, j))

        if j + 1 < n2: # shift right (to next word in transcript)
          newscore = f[i_index][j] * (j+1.) / (j+2.)
          if f[i_index][j+1] < newscore:
            f[i_index][j+1] = newscore
            path[i_index][j+1] = [(i_index, j)]
          elif f[i_index][j+1] == f[i_index][j]: # another best path
            path[i_index][j+1].append((i_index, j))


    # Only match "diagonal" edges
    possible_opt_match_pairs = []  # can have cases like [(1,a) (2,a)] but have to be both optimal!
    visited = set()

    # Search from end to head for all viable best paths
    def LableMatchDFS(i, j):
      # print 'visiting ',i,j
      if (i, j) in visited:  # prevent multiple adds
        return
      visited.add((i, j))   # mark as visited
      if i >= 0 and j >= 0:  # Terminate at "-1"s
        for (pi, pj) in path[i][j]:
          # i,j is a valid match: if pi != i, pi must be pred of i
          if pi != i and pj != j:
            possible_opt_match_pairs.append((i, j))
          LableMatchDFS(pi, pj)     # continue searching

    # F matrix might look like this:
    # [1, 1, 1]
    # [1, 1, 1]
    # [1, 1, 2]
    # [0, 0, 0]
    # [0, 1, 1]
    # [1, 1, 1]
    # So we should check best end-nodes
    endnodes = [index_cid_sub[i] for i in edges if len(edges[i]) == 0]
    maxscore = 0.0
    besti = []
    for i in endnodes:
      if maxscore < f[i][n2 - 1]:
        maxscore = f[i][n2 - 1]
        besti = [i]
      elif maxscore == f[i][n2 - 1]:
        besti.append(i)

    for i in besti:
      LableMatchDFS(i, n2 - 1)  # find all best paths

    return maxscore, [x for x in reversed(possible_opt_match_pairs)], path, f


  # Build graph
  def AddEdge(edges, f, t):
    if f not in edges:
      edges[f] = []
    edges[f].append(t)

  # Return a set of all valid paths
  def DFS(lattice_id, edges, nowid, res_array, index_cid_sub, target_ids):
    # Reaches target, finish generating a path
    if nowid in target_ids:
      # yield a deep copy of the full path
      yield [_ for _ in res_array]
      return
    # Continue generating paths
    if nowid in edges:
      for j in edges[nowid]:
        res_array.append(j)
        # Nested yield
        for item in DFS(lattice_id, edges, j, res_array, index_cid_sub, target_ids):
          yield item
        res_array.pop()

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

  ############# 2. Return DP result

  # def run(lattice_id, starts, ends, candidates, candidate_ids, transcript):
  score, match_pairs, path_mat, f = MatchTranscriptWithLattice(candidates, transcript, \
    edges, candidate_ids, index_cid_sub)

  # DEBUG
  # print '================'
  # plpy.info('BEST SCORE: %f' % score)
  # print 'Match pairs:', match_pairs  # (latticeIndex, transcriptIndex)
  PrintStatus(f,path_mat)

  # Deduplication
  match_subs = set([p[0] for p in match_pairs])

  # a set of CIDs from the match
  match_cids = set([candidate_ids[i] for i in match_subs])

  true_cids = match_cids
  for cid in true_cids:
    yield lattice_id, cid, True

  false_cids = set(candidate_ids).difference(true_cids)
  for cid in false_cids:
    yield lattice_id, cid, False

  plpy.info('[%s]  SCORE: %f, matches: %d / %d' % (lattice_id, score, len(true_cids), len(candidate_ids)))


### Testing
# TODO parse indents.. Cannot be in this part of comments :(
def test(lattice_id, starts, ends, words, cids, transcript, expected_score, expected_cand):
  print 'Testing:', words, 'against', transcript
  # for p in run(lattice_id, starts, ends, words, cids, gramlen):
  #   print p
  true_num = 0
  for item in run(lattice_id, starts, ends, words, cids, transcript):
    print 'Returned item:',item
    if item[2]: true_num += 1
  print 'Expected score: %f. check manually.' % expected_score
  if expected_cand == true_num:
    print 'Passed.'
    return 0
  else:
    print 'FAILED: True candnum expected %d got %d' % (expected_cand, true_num)
    raw_input()
    return 1

if __name__ == '__main__':
  import time
  lattice_id = 'test_lattice'
  errors = 0

  # Assume ordered by starts then ends

  # starts = [1,     3,     5   ]
  # ends =   [2,     4,     6   ]
  # words =  ['not', 'at', 'all']
  # cids =   [1001,  1002,  1003]
  # transcript = ['not',  'at',  'all']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 3)
  

  # starts = [1,     3,     5   ]
  # ends =   [4,     4,     6   ]
  # words =  ['not', 'at', 'all']
  # cids =   [1001,  1002,  1003]
  # transcript = ['not',  'at',  'all']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 3)
  

  # starts = [1,     3,     6,    1,    4,     6    ]
  # ends =   [2,     5,     7,    3,    5,     7    ]
  # words =  ['not', 'tai', 'all','now','at','tao'  ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['not',  'at',  'all']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 3)
  # # Expected result: not (tai) all,  (now) at all
  

  # starts = [1,     3,     5,    1,    4,     6    ]
  # ends =   [2,     4,     6,    3,    5,     7    ]
  # words =  ['not', 'tai', 'all','now','at','tao'  ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['not',  'at',  'all']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 2)

  # # X grid in the middle
  # starts = [  1,   2,     2,    3,      3  ,  4    ]
  # ends =   [  1,   2,     2,    3,      3  ,  4    ]
  # words =  ['A',   'B', 'X',  'X',      'B', 'C'   ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['A','B','C']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 4)

  # starts = [  1,   2,     2,    3,      3  ,  4    ]
  # ends =   [  1,   2,     2,    3,      3  ,  4    ]
  # words =  ['A',   'B', 'C',  'C',      'B', 'D'   ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['A','B','C','D']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 4)

  # # Two single paths: ABXC, AXBC
  # starts = [  1,   2,     4,    2,      5  ,  7    ]
  # ends =   [  1,   3,     6,    4,      6  ,  7    ]
  # words =  ['A',   'B', 'X',  'X',      'B', 'C'   ]
  # cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  # transcript = ['A','B','C']
  # errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 4)

  # ABCD, ACBD
  starts = [  1,   2,     4,    2,      5  ,  7    ]
  ends =   [  1,   3,     6,    4,      6  ,  7    ]
  words =  ['A',   'B', 'C',  'C',      'B', 'D'   ]
  cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  transcript = ['A','B','C','D']
  errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 4)

  # ABCD, ACBD
  starts = [  1,   2,   2,   3,   4,   4,   5      ]
  ends =   [  1,   2,   2,   3,   4,   4,   5      ]
  words =  'A B D C C X E'.split(' ')
  cids =   [1001,  1002,  1003, 1004, 1005,  1006, 1007 ]
  transcript = ['A','B','C','D','E']
  # Should match anything but 3 and 6
  errors += test(lattice_id, starts, ends, words, cids, transcript, 4, 5)


  if errors == 0: print 'ALL TESTS PASSED!!'
  else: print 'FOUND %d ERRORS!!' % errors
