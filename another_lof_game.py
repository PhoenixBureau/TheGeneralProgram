#!/usr/bin/env python

def a(value):
  return '1' + b(value) if value else '0'

def b(value):
  bits = a(value[0])
  if len(value) == 1:
    return '0' + bits
  return '1' + bits + a(value[1:])

if __name__ == '__main__':
  from itertools import combinations_with_replacement as combo, chain, permutations

  initial = (), ((),)
  K = set(initial)
  Found = K.copy()

  def permute(n, k=K):
    return set(chain(*(permutations(form) for form in set(combo(k, n)))))

  q, p = {}, {}

  def register(form, path):
    assert form not in p or p[form] == path
    q[path] = form
    p[form] = path

  for form in (
    (),
    ((),),
    (((),),),
##    ((), (),),
##    ((), (), (),),
##    ((), (), (), (),),
##    (((),),),
##    (((),), ()),
##    ((), ((),),),
##    (((),), ((),)),
##    (((),), ((),), ((),)),
##    (((),), ((),), ((),), ((),)),
##    ((((),),),),
    ):

    path = a(form)
    register(form, path)
    pr_form = ' '.join(map(str, form))
    print '%-28s -> %s' % (pr_form, path)
##    if path.endswith('0100'):
##      print '~>', path[:-4] + 'x'
##    else:
##      print

  print '_' * 70

  FORMs = sorted(p)
  for n in range(2, 5):
    for form in combo(FORMs, n):
      path = a(form)
      if form in p:
        assert p[form] == path, [form, path, p[form]]
        print 'found %s again' % (form,)
        continue

      register(form, path)
      print ' '.join(map(str, form))
      print path
