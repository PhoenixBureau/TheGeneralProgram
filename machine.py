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


if __name__ == '__main__':
  g = tuple(range(3))
  WG = []
  for n in range(2 * len(g) + 1):
    wg = wrap(g, n)
    WG.append(wg)
    print n, '->', wg

  print

  for n, wg in enumerate(WG):
    print n / 2, '->', wg, '->', unwrap(wg, n / 2)

















