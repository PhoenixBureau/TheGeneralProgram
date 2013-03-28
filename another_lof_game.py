#!/usr/bin/env python

def a(value):
  return '1' + b(value) if value else '0'

def b(value):
  bits = a(value[0])
  if len(value) == 1:
    return '0' + bits
  return '1' + bits + a(value[1:])

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
    path = a(form)
    assert form not in p or p[form] == path
    q[path] = form
    p[form] = path
    pr_form = ' '.join(map(str, form))
    print ('%-' + str(w) + 's -> %s') % (pr_form, path)

  initial = (), ((),)
  initial = set(initial)

  for form in P(initial.copy()):
    initial.add(form)

  for form in P(initial.copy()):
    initial.add(form)

  w = max(len(str(form)) for form in initial)
  for form in sorted(initial):
    register(form, w)

##    if path.endswith('0100'):
##      print '~>', path[:-4] + 'x'
##    else:
##      print

#  print '_' * 70
