# -*- coding: utf-8 -*-
from itertools import product, imap, izip


B = ((),), ()


mark = lambda form: not form or not any(imap(mark, form))


reduce_ = lambda form: B[mark(form)]


nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(and_(bits))
xor = lambda *bits: nor(and_(*bits), nor(*bits))



def walk(meaning, name):
  while name in meaning and meaning[name] != name:
    name = meaning[name]
  if isinstance(name, tuple):
    return tuple(walk(meaning, inner) for inner in name)
  return name


def reify(meaning, form):
  if isinstance(form, basestring):
    return walk(meaning, form)
  if isinstance(form, tuple):
    return tuple(reify(meaning, inner) for inner in form)
  return form


def collect_names(form, names=None):
  if names is None:
    names = set()
  if isinstance(form, basestring):
    names.add(form)
  else:
    assert isinstance(form, tuple)
    for inner in form:
      collect_names(inner, names)
  return names


def all_meanings(form):
  names = collect_names(form)
  if not names:
    return
  for values in product(*([B] * len(names))):
    yield dict(izip(names, values))


def exhaust(form):
  for meaning in all_meanings(form):
    yield meaning, reify(meaning, form)


def goal_clause(terms):
  return nor(and_(*terms))


def solve(form):
  no_yes = [], []
  for m, r in exhaust(goal_clause(form)):
    no_yes[mark(r)].append((m, r))
  return no_yes
    

s = lambda term: (str(term)
                  .replace(' ', '')
                  .replace("','", ' ')
                  .replace("'", '')
                  .replace(',', '')
                  .replace('(())', '◎')
                  .replace('()', '○')
                  )


#        ( ¬a ∨ ¬b )      ≡        ¬( a ∧ b )
# or_(nor('a'), nor('b')) == nor(and_('a', 'b'))
#
# True
# In the circlang they are both: (((a)(b)))
# No love for De Morgan...  Sorry dude.
#
# c0 = or_(nor(nor('mortal')), nor('human'))

# c0 = nor(and_(nor('mortal'), 'human'))


print "All humans are mortal, a.k.a. mortal OR NOT human,"
print 'IF NOT mortal THEN NOT human (Sorry, "The Highlander".)'
print
print "E = nor('mortal'), 'human'"
print

E = nor('mortal'), 'human'

E = nor('mammal'), 'hairy', 'lactates', 'live-birth'


no, yes = solve(E)


print 'Look for acceptable solutions'
for m, r in yes:
  print s(r), '->', m
print


print 'Look for counter examples'
for m, r in no:
  print s(r), '->', m
print

##  ((◎(◎))) -> 1 {'human': ((),), 'mortal': ((),)}
##  ((○(◎))) -> 1 {'human': ((),), 'mortal': ()}
##  ((◎◎)) -> 0 
##  ((○◎)) -> 1 {'human': (), 'mortal': ()}
##
#    Non-human immortals;
#    Non-human mortals;
#    Human mortals;
#
#    but NO human immortals



##  for m, r in exhaust(and_(*'abcde')):
##    v = mark(r)
##    print s(r), '->', int(v), m if v else ''
