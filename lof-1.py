

def f(form, indent=0):
  '''
  Long-winded.
  '''
  if form is ():
    print indent * 2 * ' ', '(), I am Mark!'
    return True

  # A mark that lies inside this tuple marks it as a non-mark
  print indent * 2 * ' ', '( non-empty, checking insides', form, hex(id(form))
  if any(f(inner, indent + 1) for inner in form):
    print indent * 2 * ' ', '), found mark inside', hex(id(form)), '<- unmarked'
    return False

  print indent * 2 * ' ', '), found unmarked inside', hex(id(form)), '<- marked'
  return True


# Short form. (No pun intended.)
F = lambda form: form is () or not any(F(inner) for inner in form)


def memoize(memo={}):
  def memoize_(f):
    def mf(form, *ignored):
      if form is ():
        return True
      if form in memo:
        print 'cache hit for', form, hex(id(form))
        return memo[form]
      m = memo[form] = f(form)
      return m
    return mf
  return memoize_


D = {}
f = memoize(D)(f)
#F = memoize(D)(F)


for form in (

  (), # True

  ((),), # False

  (((),),), # True

  (((),), ()), # False

  (((),), ((),)), # True

  (((),), (((),),)), # False

  (((((),),),),),
  ((((((),),),),),),
  (((((((),),),),),),),
  ((((((((),),),),),),),),

  ((), ()),

  ((), (), ()),

  ((), (), (), ()),

  (((),), ()),

  (((),), ((),)),
  (((),), ((),), ((),)),
  (((),), ((),), ((),), ((),)),
  (((),), ((),), ((),), ((),), ((),)),

  (((),), ((), ()), ((),), ((),)),
  (((),), (((),),), ((),), ((),)),

  ((((),),), (((),),), (((),),)),

  (((((),),),), ((((),),),), ((((),),),)),

  (((), ((), ())), ((((),),), ((),),),),

  ):
  print '=' * 70
  print '%5s %-5s := %s' % (f(form), F(form), form)
  print ; print ; print

import pprint
pprint.pprint(D)
