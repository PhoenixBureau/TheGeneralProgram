'''
Defines a machine using the GSB-LoF form.
'''

def wrap(form, i):
  '''

  * -> ((*))

  In order to handle the wrapping of nothing in-between the inner forms
  of the form we adopt the convention that even i (0, 2, 4, ...) will
  select the intersticies of the inner forms, while the odd i (1, 3, ...)
  will select the inner forms themselves.

  Therefore the valid indicies for a form g are: range(2 * len(g) + 1).
  Greater indicies will append wrap the nothing at the end of the form.

  If you wrap (0, 1, 2) with the following indicies you get these
  resultant forms:

    0 -> (((),), 0, 1, 2)
    1 -> (((0,),), 1, 2)
    2 -> (0, ((),), 1, 2)
    3 -> (0, ((1,),), 2)
    4 -> (0, 1, ((),), 2)
    5 -> (0, 1, ((2,),))
    6 -> (0, 1, 2, ((),))

  '''
  wrap_nothing = not i % 2
  i /= 2
  left = form[:i]
  if wrap_nothing:
    right = form[i:]
    t = ((),)
  else:
    right = form[i + 1:]
    t = ((form[i],),)
  return left + (t,) + right


def unwrap(form, i):
  '''

  ((*)) -> *

  Unwrap an inner form (including nothing) in form at index i.

  (Unlike the wrap() function which handles indices specially to permit
  one function to wrap both "present" forms and intersticial nothing,
  unwrap() uses just the normal index.


    0 -> (((),), 0, 1, 2) -> (0, 1, 2)
    0 -> (((0,),), 1, 2) -> (0, 1, 2)
    1 -> (0, ((),), 1, 2) -> (0, 1, 2)
    1 -> (0, ((1,),), 2) -> (0, 1, 2)
    2 -> (0, 1, ((),), 2) -> (0, 1, 2)
    2 -> (0, 1, ((2,),)) -> (0, 1, 2)
    3 -> (0, 1, 2, ((),)) -> (0, 1, 2)

  '''
  left, t, right = form[:i], form[i], form[i + 1:]
  return (left + right) if t == ((),) else (left + (_k(t),) + right)

# Helper function to "unwrap" a single wrapped form.
_k = lambda (((anything,),)): anything


def delete(form, i):
  '''
  OA -> O
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + form[i + 1:]


def undelete(form, i, anything):
  '''
  O -> OA
  '''
  assert form[i] == ()
  i += 1
  return form[:i] + (anything,) + form[i:]


def copy(form, i):
  '''
  A(B) -> A(AB)
  '''
  left, A, t, right = form[:i + 1], form[i], form[i + 1], form[i + 2:]
#  print 'copy', left, A, t, right
  return left + ((A,) + t,) + right


def uncopy(form, i):
  '''
  A(AB) -> A(B)
  '''
  left, A, t, right = form[:i], form[i], form[i + 1], form[i + 2:]
  assert t[0] == A
  return left + (t[1:],) + right


def apply_(form, program):
  if program and callable(program[0]):
    function, args = program[0], program[1:]
    return function(form, *args)
  for inner in program:
    form = apply_(form, inner)
  return form


if __name__ == '__main__':
  print '~' * 70
  print 'Wrap / UnWrap' ; print

  g = tuple(range(2))
  WG = []
  for n in range(2 * len(g) + 1):
    wg = wrap(g, n)
    WG.append(wg)
    print n, '->', wg

  print

  for n, wg in enumerate(WG):
    print n / 2, '->', wg, '->', unwrap(wg, n / 2)

  print
  print '~' * 70
  print 'Delete / UnDelete' ; print

  g = tuple(() for _ in range(3))
  for i in range(len(g)):
    print i, '->', g, '->',
    g = undelete(g, i, "Hey there!")
    print g, '->',
    g = delete(g, i)
    print g

  print
  print '~' * 70
  print 'Copy / UnCopy' ; print

  g = ((), 'A', ('B',), ())
  print g, '->',
  g = copy(g, 1)
  print g, '->',
  g = uncopy(g, 1)
  print g











