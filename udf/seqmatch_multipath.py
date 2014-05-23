#! /usr/bin/python

import os, sys

def ElemMatch(e1, e2):
  return e1 == e2

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


  # for i in range(0, n1): 
  #   for j in range(0, n2):
  #     print '(%d,%d): %d\t' % (i,j,f[i][j]),

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

  # Single-path version
  # i, j = n1-1, n2-1
  # while i >= 0 and j >= 0:
  #   # (i, j) != (-1,-1):
  #   pi, pj = path[i][j]
  #   if pi == i - 1 and pj == j - 1:
  #     match_elements.append((i, j))
  #   i, j = pi, pj

  # return f[n1 - 1][n2 - 1], [x for x in reversed(match_elements)], path
  return f[n1 - 1][n2 - 1], [x for x in reversed(possible_opt_match_pairs)], path
  # needs deduplication!

def Test(arr1, arr2, expected_score, expected_match):
    score, match_elements, path = Match(arr1, arr2)
    print 'A:',arr1
    print 'B:',arr2
    matches_arr1 = set([p[0] for p in match_elements]) # Dedup
    print 'Matched elements:', [arr1[i] for i in matches_arr1]
    print '[%d]  %s' % (score, str(matches_arr1))
    if score != expected_score or len(matches_arr1) != expected_match:
      print 'ERROR! Expected: (%d, %d), Computed: (%d, %d)' % (expected_score, expected_match, score, len(matches_arr1))
      print 'Score:',score
      print 'Matches:', match_elements
      print '\n'.join([str(x) for x in path])
      raw_input()
      return 1      # fail
    else: return 0   # pass


if __name__ == "__main__": 
  if len(sys.argv) == 3:
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    arr1 = [l.strip() for l in open(f1).readlines()]
    arr2 = [l.strip() for l in open(f2).readlines()]
    score, matches = Match(arr1, arr2)
    print score
    print >>sys.stderr, matches  # test

  else:
    print 'Usage:',sys.argv[0],'<path1> <path2> (words split by \\n)'

    print 'Tetsing:'
    errors = 0
    arr1 = [0,1,3,2]
    arr2 = [5,1,2,3]
    errors += Test(arr1, arr2, 2, 3) # 1 2 3 matches (multipath)
    arr1 = 'I want to go to seattle'.split(' ')
    arr2 = 'I want go to seattle yay!'.split(' ')
    errors += Test(arr1, arr2, 5, 5)
    arr1 = 'I want to go to seattle'.split(' ')
    arr2 = 'I want to go to seattle yay!'.split(' ')
    errors += Test(arr1, arr2, 6, 6)
    arr1 = 'How I want go to seattle but...'.split(' ')
    arr2 = 'Why I want go to seattle yay!'.split(' ')
    errors += Test(arr1, arr2, 5, 5)
    arr1 = 'I want'.split(' ')
    arr2 = ''.split(' ')
    errors += Test(arr1, arr2, 0, 0)
    arr1 = 'c a'.split(' ')
    arr2 = 'a b'.split(' ')
    errors += Test(arr1, arr2, 1, 1)
    arr1 = [1,2,3]
    arr2 = [1,2,3]
    errors += Test(arr1, arr2, 3, 3)
    arr1 = [1]
    arr2 = [1]
    errors += Test(arr1, arr2, 1, 1)
    arr1 = []
    arr2 = [1]
    errors += Test(arr1, arr2, 0, 0)
    arr1 = 'I want to'.split(' ')
    arr2 = 'want I to'.split(' ')  # double path, break ties
    errors += Test(arr1, arr2, 2, 3)
    arr1 = 'I want to go back'.split(' ')
    arr2 = 'want I to back go'.split(' ')  # double path, break ties
    errors += Test(arr1, arr2, 3, 5)
    arr1 = 'A B C D E'.split(' ')
    arr2 = 'B C E A D'.split(' ')
    errors += Test(arr1, arr2, 3, 4)
    print 'NOTE: suppose to have BCDE matched'
    arr1 = 'A B C X Y Z'.split(' ')
    arr2 = 'A X B Y C Z'.split(' ')
    errors += Test(arr1, arr2, 4, 6) # XYZA / ABCZ
    if errors == 0: print 'ALL TESTS PASSED!!'
    else: print 'FOUND %d ERRORS!!' % errors

