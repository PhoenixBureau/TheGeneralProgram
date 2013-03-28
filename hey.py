from itertools import product

initial = (), ((),)
K = set(initial)
Found = K.copy()

def patterns(forms, n=2):
  return product(*([forms] * n))

def P(f, n=2, m=4):
  if n == m:
    return
  for p in patterns(f, n):
    assert not p in K
    yield p
  for pp in P(K, n+1, m):
    yield pp

for form in P(K.copy()):
  print form
  K.add(form)

##for f in sorted(K):
##  print f
