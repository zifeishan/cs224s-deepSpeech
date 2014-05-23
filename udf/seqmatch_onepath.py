#! /usr/bin/python

import os, sys

def ElemMatch(e1, e2):
  return e1 == e2

def Match(arr1, arr2):
  # F: longest matching up to ith element from arr1 and and jth from arr2
  n1 = len(arr1)
  n2 = len(arr2)
  if n1 == 0 or n2 == 0: return 0
  # f = [[0] * (n2)] * (n1)  # Python array is weird....
  f = [[0] * n2 for _ in range(n1)] # This is correct way, do not give a shallow copy!!

  # f = { i:{j : 0 for j in range(0, n2)} for i in range(0, n1)}

  path = [[(-1,-1) for _2 in range(n2)] for _ in range(n1)]

  # print f
  # Init
  path[0][0] = (-9, -9) # no match
  if ElemMatch(arr1[0], arr2[0]):
    f[0][0] = 1
    path[0][0] = (-1, -1) # match

  for i in range(1, n1):
    if ElemMatch(arr1[i], arr2[0]):
      f[i][0] = 1
      path[i][0] = (i-1, -1)
    elif f[i-1][0] == 1:  # todo multiple?
      f[i][0] = 1
      path[i][0] = (i-1, 0)

  for j in range(1, n2):
    if ElemMatch(arr1[0], arr2[j]):
      f[0][j] = 1
      path[0][j] = (-1, j-1)
    elif f[0][j-1] == 1:
      f[0][j] = 1
      path[0][j] = (0, j-1)

  # DP
  for i in range(0, n1):
    for j in range(0, n2):
      if i + 1 < n1 and j + 1 < n2 \
        and ElemMatch(arr1[i+1], arr2[j+1]) \
        and f[i+1][j+1] < f[i][j] + 1:
        f[i+1][j+1] = f[i][j] + 1
        path[i+1][j+1] = (i, j)

      if i + 1 < n1 and f[i+1][j] < f[i][j]: # left shift
        f[i+1][j] = f[i][j]
        path[i+1][j] = (i, j)

      if j + 1 < n2 and f[i][j+1] < f[i][j]: # right shift
        f[i][j+1] = f[i][j]
        path[i][j+1] = (i, j)

  # for i in range(0, n1): 
  #   for j in range(0, n2):
  #     print '(%d,%d): %d\t' % (i,j,f[i][j]),

  # Only match "diagonal" edges
  match_elements = []
  i, j = n1-1, n2-1
  while i >= 0 and j >= 0:
    # (i, j) != (-1,-1):
    pi, pj = path[i][j]
    if pi == i - 1 and pj == j - 1:
      match_elements.append((i, j))
    i, j = pi, pj

  return f[n1 - 1][n2 - 1], [x for x in reversed(match_elements)], path




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
    arr1 = [0,1,3,2]
    arr2 = [5,1,2,3]
    # arr1 = 'I want to go to seattle'.split(' ')
    # arr2 = 'I want go to seattle yay!'.split(' ')
    # arr1 = 'c a'.split(' ')
    # arr2 = 'a b'.split(' ')
    # arr1 = [1,2,3]
    # arr2 = [1,2,3]
    arr1 = 'I want to'.split(' ')
    arr2 = 'want I to'.split(' ')  # double path, break ties
    score, match_elements, path = Match(arr1, arr2)
    print arr1
    print arr2
    print 'Score:',score
    print 'Matches:', match_elements
    print 'Matched elements:', [arr1[i[0]] for i in match_elements]
    print '\n'.join([str(x) for x in path])
    # print 'path:','../data/journal-test-output3-distinct/JOURNAL_14255.cand_word'

    # # tess = [l.strip().split('\t')[-1] for l in open('../data/journals-test-output/JOURNAL_102371.cand').readlines()]
    # # lines = [l.strip() for l in open('../data/test-supervision/JOURNAL_102371.seq').readlines()]
    # tess = [l.strip().split('\t')[5] for l in open('../data/journal-test-output3-distinct/JOURNAL_14255.cand_word').readlines()]
    # lines = [l.strip() for l in open('../data/test-evaluation/JOURNAL_14255.seq').readlines()]
    # print 'Matching 1000 words:'
    # print Match(tess[:1000], lines[:1000])
    # print 'Matching all words:', len(tess), len(lines)
    # print Match(tess, lines)
    # # # sys.exit(1)


