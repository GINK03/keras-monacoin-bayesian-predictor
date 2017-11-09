import keras
import sys
import gzip
import pickle
import json
import numpy as np
if '--make_pair' in sys.argv:
  f = open('monacoin.csv')
  key = next(f).split()

  ys, Xs = [], []
  for val in f:
    val = val.strip().split()
    obj = dict(zip(key, val))
    obj['price'] = float( obj['price'] )
    X = obj['snapped_at'] 
    y = float( obj['price'] )
    ys.append(y)
    Xs.append(X)
  open('tmp/make_pair.pkl', 'wb').write( gzip.compress( pickle.dumps( (ys, Xs) ) ) )
  
if '--key_vec' in sys.argv:
  ys, Xs = pickle.loads( gzip.decompress( open('tmp/make_pair.pkl', 'rb').read() ) )
  key_index = {}
  size = 0
  for x in Xs: 
    size = max([size, len(x)])
    for index, ch in enumerate(list(x)):
      key = '%s-%s'%(index, ch)
      if key_index.get(key) is None:
        key_index[key] = len(key_index)

  print( 'key lenght', len(key_index) )
  open('tmp/key_index.json', 'w').write( json.dumps([key_index, size], indent=2, ensure_ascii=False) )

if '--to_vec' in sys.argv:
  key_index, size = json.loads( open('tmp/key_index.json').read() )

  ys_, Xs = pickle.loads( gzip.decompress( open('tmp/make_pair.pkl', 'rb').read() ) )
  
  Xs_ = []
  for X in Xs:
    base = [ [0.0]*len(key_index) for i in range(size) ]
    for index, ch in enumerate(list(X)):
      key = '%s-%s'%(index, ch)
      cursol = key_index[key]
      base[index][cursol] = 1.0
    Xs_.append( base )
  Xs_ = np.array(Xs_)
  ys_ = np.array(ys_)
  open('tmp/data.pkl', 'wb').write( gzip.compress( pickle.dumps( (ys_, Xs_) ) ) )