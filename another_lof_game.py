#!/usr/bin/env python
'''

     _ -> 0           ( "Nothing". )
    () -> 100         ( Something with nothing next to it or inside it. )
  (A)B -> 1 B? BA : A ( I.e. path[1] indicates if term B exists, then
                        term B is encoded if it exists, then term A. )


'''


def a(value):
  return '1' + b(value) if value else '0'

def b(value):
  bits = a(value[0])
  if len(value) == 1:
    return '0' + bits
  return '1' + bits + a(value[1:])


def un_a(path):
  bit, path = path[0], path[1:]
  if bit == '0':
    return None, path
  return un_b(path)

def un_b(path):
  bit, path = path[0], path[1:]

  if bit == '0':
    # nothing for B, the rest of the path specifies A
    A, rest_of_path = un_a(path)
    if A is None:
      return (), rest_of_path
    return (A,), rest_of_path

  # A then B
  A, rest_of_path = un_a(path)
  B, rest_of_path = un_a(rest_of_path)
  assert not rest_of_path, repr(rest_of_path)

  print A, B
  if A is None:
    return ((),) + B, rest_of_path
  return (A, B), rest_of_path


def prp(path):
  LM = un_a(path)
  print LM
  print q[path], '<===>', LM[0], LM[0] == q[path]


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
#    print ('%-' + str(w) + 's -> %s') % (pr_form, path)

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

##  for form in P(initial.copy()):
##    initial.add(form)

  w = max(len(str(form)) for form in initial)
  for form in sorted(initial, key=lambda form: (len(str(a(form))), len(form))):
    register(form, w)

##    if path.endswith('0100'):
##      print '~>', path[:-4] + 'x'
##    else:
##      print

  print '_' * 70

path = list(q).pop()
print path
prp(path)

((), (((),),), ((((((((),),),),),),),))
((), ((((),),), (((((((),),),),),),) ))






