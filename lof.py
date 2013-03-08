
# Short form. (No pun intended.)
F = lambda form: form == () or not any(F(inner) for inner in form)


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
F = memoize(F, D)


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
  result = F(form)
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
##  print F(p), p
##
##print '~' * 70
##
##p = ((),)
##while len(p) <= 3:
##  p = tuple(P(p))
##  print F(p), p
##

while True:
  form = T(T(T(T(T(T(T(I())))))))
  print '%-5s -> %s' % (F(form), form)
