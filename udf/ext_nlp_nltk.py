import ddext

def init():
  ddext.import_lib('nltk')

  ddext.input('lattice_id', 'text')
  ddext.input('candidate_id', 'bigint')
  ddext.input('word', 'text')

  ddext.returns('lattice_id', 'text')
  ddext.returns('candidate_id', 'bigint')
  ddext.returns('pos', 'text')

def run(lattice_id, candidate_id, word):
  if word in ['<s>', '</s>', '~SIL']:
    yield lattice_id, candidate_id, word
    return
  nltk.data.path = ['/dfs/rambo/0/zifei/nltk_data']
  poss = nltk.pos_tag([word])
  if len(poss) > 0:
    yield lattice_id, candidate_id, poss[0][1]