#!/usr/bin/env python
'''

     _ -> 0           ( "Nothing". )
    () -> 100         ( Something with nothing next to it or inside it. )
  (A)B -> 1 B? BA : A ( I.e. path[1] indicates if term B exists, then
                        term B is encoded if it exists, then term A. )

'''
from omgebt import encode, decode, _s


if __name__ == '__main__':
  from itertools import product

  def patterns(forms, n=2):
    return product(*([forms] * n))

  def P(f, n=2, m=4):
    if n == m:
      return
    for p in patterns(f, n):
      yield p
    for pp in P(f, n+1, m):
      yield pp

  q, p = {}, {}

  def register(form, w=28):
    path = encode(*form)
    assert form not in p or p[form] == path
    q[path] = form
    p[form] = path
    pr_form = _s(form, True)
    print ('%-s -> %s') % (pr_form, path)

  t = ()
  initial = t,
  initial = set(initial)
  for _ in range(7):
    t = t,
    initial.add(t)
  print sorted(initial)
  print '-' * 70

  for form in P(initial.copy()):
    initial.add(form)

  w = max(len(str(form)) for form in initial)
  for form in sorted(initial, key=lambda form: (len(str(encode(*form))), len(form))):
    register(form, w)

  print '_' * 70

