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

  # Returns: score, match_elements, path
  # Deduplication: matches_arr1 = set([p[0] for p in match_elements])
  def Match(arr1, arr2):
    # F: longest matching up to ith element from arr1 and and jth from arr2
    n1 = len(arr1)
    n2 = len(arr2)
    if n1 == 0 or n2 == 0: 
      return 0, [], []
    # f = [[0] * (n2)] * (n1)  # Python array is weird....
    f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!

    # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}

    # an "array" for each grid in matrix
    path = [[[] for _2 in range(n2)] for _ in range(n1)]

    # print f
    # Init
    if ElemMatch(arr1[0], arr2[0]):
      f[0][0] = 1
      path[0][0].append((-1, -1)) # match

    for i in range(1, n1):
      if ElemMatch(arr1[i], arr2[0]):
        f[i][0] = 1
        path[i][0].append((i-1, -1))
      elif f[i-1][0] == 1:  # todo multiple?
        f[i][0] = 1
        path[i][0].append((i-1, 0))

    for j in range(1, n2):
      if ElemMatch(arr1[0], arr2[j]):
        f[0][j] = 1
        path[0][j].append((-1, j-1))
      elif f[0][j-1] == 1:
        f[0][j] = 1
        path[0][j].append((0, j-1))

    # DP
    for i in range(0, n1):
      for j in range(0, n2):
        if i + 1 < n1 and j + 1 < n2 \
          and ElemMatch(arr1[i+1], arr2[j+1]):
            if f[i+1][j+1] < f[i][j] + 1:
              f[i+1][j+1] = f[i][j] + 1
              path[i+1][j+1] = [(i, j)]  # new list, truncate previous
            elif f[i+1][j+1] == f[i][j] + 1:
              path[i+1][j+1].append((i, j))  # append another best path

        if i + 1 < n1: # left shift
          if f[i+1][j] < f[i][j]:
            f[i+1][j] = f[i][j]
            path[i+1][j] = [(i, j)]
          elif f[i+1][j] == f[i][j]: # another best path
            path[i+1][j].append((i, j))

        if j + 1 < n2: # right shift
          if f[i][j+1] < f[i][j]:
            f[i][j+1] = f[i][j]
            path[i][j+1] = [(i, j)]
          elif f[i][j+1] == f[i][j]: # another best path
            path[i][j+1].append((i, j))

    # Only match "diagonal" edges
    possible_opt_match_pairs = []  # can have cases like [(1,a) (2,a)] but have to be both optimal!
    visited = set()
    def LableMatchDFS(i, j):
      if (i, j) in visited:  # prevent multiple adds
        return
      visited.add((i, j))   # mark as visited
      if i >= 0 and j >= 0:
        for (pi, pj) in path[i][j]:
          if pi == i - 1 and pj == j - 1: # i,j is a valid match
            possible_opt_match_pairs.append((i, j))
          LableMatchDFS(pi, pj)     # continue searching

    LableMatchDFS(n1-1, n2-1)

    return f[n1 - 1][n2 - 1], [x for x in reversed(possible_opt_match_pairs)], path
    # needs deduplication!

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
  indegree = [0 for i in range(N)]

  for i in range(N):
    start = starts[i]
    end = ends[i]
    if end + 1 in index_start_sub:
      for j in index_start_sub[end + 1]:
        AddEdge(edges, candidate_ids[i], candidate_ids[j])
        indegree[j] += 1


  ######## 2. DFS output candidates
  res_array = []

  end_ids = set([candidate_ids[i] for i in range(N) if candidate_ids[i] not in edges])
  start_ids = set([candidate_ids[i] for i in range(N) if indegree[i] == 0])

  # # DEBUG
  # print 'start nodes:',start_ids
  # print 'end targets:',end_ids
  # print 'edges:', edges
  # print 'indexes:', index_cid_sub

  # for startid in sorted(edges.keys()):

  pathnum = 0
  maxscore = 0
  bestpath_cids = set()
  for startid in start_ids:
    res_array.append(startid)
    for path in DFS(lattice_id, edges, startid, res_array, index_cid_sub, end_ids):
      pathnum += 1
      # "path" is candidate_ids in path
      path_words = [candidates[index_cid_sub[i]] for i in path]
      # 0, 1, 2...: subs for both "path" and "path_words"

      # # DEBUG
      # print path  
      # print path_words
      
      score, match_pairs, path_mat = Match(path_words, transcript)
      # Deduplication
      match_subs = set([p[0] for p in match_pairs])

      # a set of CIDs from the match
      match_cids = set([path[i] for i in match_subs])

      # # DEBUG
      # arr1 = path_words
      # arr2 = transcript
      # print 'A:',arr1
      # print 'B:',arr2
      # matches_arr1 = set([p[0] for p in match_pairs]) # Dedup
      # print 'Matched elements:', [arr1[i] for i in matches_arr1]
      # print '[%d]  %s' % (score, str(matches_arr1))
      # print 'Matches:', match_pairs
      # # print '\n'.join([str(x) for x in path])


      if score > maxscore:  # Update with this solution
        maxscore = score
        # print '  Updating score:', score
        bestpath_cids = match_cids
        # print '  best subs:', bestpath_cids
      elif score == maxscore:
        # print '  Merge subs from:', bestpath_cids
        bestpath_cids.update(match_cids)  # merge all possible cids into
        # print '  Merge subs to:', bestpath_cids

    res_array.pop()  # search for different starts

  # Obtain all results!
  # DEBUG
  # print 'Best score:', maxscore
  # print 'Matched cids', bestpath_cids

  # print 'Matched words', [candidates[index_cid_sub[cid]] for cid in bestpath_cids]

  true_cids = bestpath_cids
  for cid in true_cids:
    yield lattice_id, cid, True

  false_cids = set(candidate_ids).difference(true_cids)
  for cid in false_cids:
    yield lattice_id, cid, False

  plpy.info('%d paths, true labels: %d / %d' % (pathnum, len(true_cids), len(true_cids) + len(false_cids) ))


### Testing
# TODO parse indents.. Cannot be in this part of comments :(
def test(lattice_id, starts, ends, words, cids, transcript, expected_score, expected_cand):
  print 'Testing:', words, 'against', transcript
  # for p in run(lattice_id, starts, ends, words, cids, gramlen):
  #   print p
  true_num = 0
  for item in run(lattice_id, starts, ends, words, cids, transcript):
    print item
    if item[2]: true_num += 1
  print 'Expected score: %d. check manually.' % expected_score
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

  starts = [1,     3,     5   ]
  ends =   [4,     4,     6   ]
  words =  ['not', 'at', 'all']
  cids =   [1001,  1002,  1003]
  transcript = ['not',  'at',  'all']
  errors += test(lattice_id, starts, ends, words, cids, transcript, 3, 3)
  

  starts = [1,     3,     6,    1,    4,     6    ]
  ends =   [2,     5,     7,    3,    5,     7    ]
  words =  ['not', 'tai', 'all','now','at','tao'  ]
  cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  transcript = ['not',  'at',  'all']
  errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 3)
  # Expected result: not (tai) all,  (now) at all
  

  starts = [1,     3,     5,    1,    4,     6    ]
  ends =   [2,     4,     6,    3,    5,     7    ]
  words =  ['not', 'tai', 'all','now','at','tao'  ]
  cids =   [1001,  1002,  1003, 1004, 1005,  1006 ]
  transcript = ['not',  'at',  'all']
  errors += test(lattice_id, starts, ends, words, cids, transcript, 2, 2)

  if errors == 0: print 'ALL TESTS PASSED!!'
  else: print 'FOUND %d ERRORS!!' % errors
