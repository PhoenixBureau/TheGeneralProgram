from random import random


# Short form. (No pun intended.)
F = lambda form: form == () or not any(F(inner) for inner in form)


# Memo-ize for efficiency.
#
def memoize(f, memo):
  def mf(form):
    if form == (): return True
    try: return memo[form]
    except KeyError: m = memo[form] = f(form)
    return m
  return mf
D = {}
F = memoize(F, D)


def R(form):
  '''
  Reduce a form according to these rules:

    (()) -> nothing    "Cancel"
    ()() -> ()         "Repeat"

  '''
  f = iter(form)
  for inner in f:
    if inner == ((),):
      continue
    if inner == ():
      yield inner
      while inner == ():
        inner = f.next()
    yield inner
#    yield tuple(R(inner)) # Recursively reduce sub-expressions.


def P(form):
  '''
  Produce new forms by applying these rules:

    nothing -> (())
         () -> ()()

  '''
  for inner in form:
    if random() > 0.5:
      yield ((),)
    yield tuple(P(inner))
    if inner == () and random() > 0.5:
      yield inner
  if random() > 0.5:
    yield ((),)


for expected, form in (

  (False, ((),)),
  (False, ((), ())),
  (False, ((), (), ())),
  (False, ((), (), (), ())),
  (False, ((), ((), ()))),
  ( True, (((),),)),
  (False, (((),), ())),
  ( True, (((),), ((),))),
  ( True, (((),), ((),), ((),))),
  ( True, (((),), ((),), ((),), ((),))),
  ( True, (((),), ((),), ((),), ((),), ((),))),
  ( True, (((),), ((), ()), ((),), ((),))),
  ( True, (((),), ((), ((),)), ((),), ((),))),
  (False, (((),), (((),), ((),)), ((),), ((),))),
  (False, (((),), (((),),))),
  (False, (((),), (((),),), ((),), ((),))),
  ( True, (((), ((), ())), ((((),),), ((),)))),
  (False, ((((),),),)),
  (False, ((((),),), ((),))),
  (False, ((((),),), (((),),), (((),),))),
  ( True, (((((),),),),)),
  ( True, (((((),),),), ((((),),),), ((((),),),))),
  (False, ((((((),),),),),)),
  ( True, (((((((),),),),),),)),
  (False, ((((((((),),),),),),),)),

  ):
#  print '~' * 70
  result = F(form)
##  trans = ((), '--')[result]
##
##  r = ', '.join('%s' for _ in range(len(form))) % form
##
##  red = tuple(R(form))
##  j = ', '.join('%s' for _ in range(len(red))) % red
##
##  print '%-2s := %s -> %s' % (trans, r, j)
##  assert expected == result

##import pprint
##pprint.pprint(D)

##p = '' # Equivalent to ()
##while len(p) <= 3:
##  p = tuple(P(p))
##  print F(p), p
##
##print '~' * 70
##
##p = ((),)
##while len(p) <= 3:
##  p = tuple(P(p))
##  print F(p), p




