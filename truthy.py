

def sf(form, X, NOTX):
  t = ()
  for inner in form:
    t += tuple(_sf(inner, X, NOTX))
  return t


def _sf(form, X, NOTX):
  if isinstance(form, basestring):
    if form in X:
      pass
    elif form in NOTX:
      yield ()
    else:
      raise Exception(form)
  else:
    assert isinstance(form, tuple)
    yield sf(form, X, NOTX)


def parms(expression):
  names = [(name, (name,)) for name in collect_names(expression)]
  for terms in product(*names):
    yes, no = set(), set()
    for term in terms:
      if isinstance(term, basestring):
        yes.add(term)
      else:
        no.add(term[0])
    yield terms, yes, no


def find_counter_examples(form):
  for terms, yes, no in parms(form):
    if mark(sf(form, yes, no)):
      yield terms



f1 = ('d', ('b', 'f')), ('e', 'b'), ('f', 'c', ('e',)), (('c', 'd'))

##print
##print
##for ce in find_counter_examples(f1):
##  print ce


##print; print; print
##print 'FBA:', s(fba)
##print
##
##for terms, yes, no in parms(fba):
##  print terms
##  E = sf(fba, yes, no)
##  print s(E)
##  print mark(E)
##  print


print 'How to discover the truthiness of logical propositions:'
print

# Logical conjunction ^ 
and_l = nor
implies = lambda P, Q: (P, (Q,))

# [(P -> R) ^ (Q -> S)] -> [(P ^ Q) -> (R ^ S)]

f3 = and_l(implies('P', 'R'), implies('Q', 'S'))
f4 = implies(and_l('P', 'Q'), and_l('R', 'S'))
f5 = implies(f3, f4)

for counter_example in find_counter_examples(f5):
  print counter_example
  break
else:
  print True, s(f5)


# [B ^ (B -> C)] -> C
f6 = and_l('B', implies('B', 'C'))
f7 = implies(f6, 'C')

