#!/usr/bin/env python
from itertools import imap as lazy_apply
'''

"The Laws of Form" by G. Spencer-Brown.


In Python, let "a form" be any data-structure composed entirely of tuples.

We shall consider the absence of any form to be "the ground" and have the
Boolean value of True.

A "mark" is the empty tuple or any tuple without a mark, marks have the
Boolean value of False.

'''

mark = lambda form: not form or not any(lazy_apply(mark, form))


#  Reduce a form according to these rules:
#
#    (()) -> nothing    "Cancel"
#    ()() -> ()         "Repeat"
#

a = lambda form: tuple(inner for inner in form if inner != ((),))

b = lambda form: form if () not in form else (
  ((),) + tuple(inner for inner in form if inner)
  )

R = lambda form: tuple(a(b(R(inner) for inner in form)))



#  Produce new forms by applying these rules:
#
#    nothing -> (())
#         () -> ()()
#

z = lambda form: (((),),) + tuple(form)

y = lambda form: ((),) + form if () in form else form

P = lambda form: tuple(y(z(P(inner) for inner in form)))


# Generate random new forms.
from random import random

T = lambda form: z(form) if random() > 0.5 else y(form)
I = lambda: () if random() > 0.5 else ((),)


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
mark = memoize(mark, D)


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
  print '~' * 70
  result = mark(form)
  trans = ((), '--')[result]

  r = ', '.join('%s' for _ in range(len(form))) % form

  red = tuple(R(form))
  j = ', '.join('%s' for _ in range(len(red))) % red

  print '%-2s := %s -> %s' % (trans, r, j)
##  print '%-2s := %s' % (trans, r)
  assert expected == result

##  red = a(form)
##  print 'a', ', '.join('%s' for _ in range(len(red))) % red
##
##  red = b(form)
##  print 'b', ', '.join('%s' for _ in range(len(red))) % red


##import pprint
##pprint.pprint(D)

##p = '' # Equivalent to ()
##while len(p) <= 3:
##  p = tuple(P(p))
##  print mark(p), p
##
##print '~' * 70
##
##p = ((),)
##while len(p) <= 3:
##  p = tuple(P(p))
##  print mark(p), p
##

while True:
  form = T(T(T(T(T(T(T(I())))))))
  print '%-5s -> %s' % (mark(form), form)
