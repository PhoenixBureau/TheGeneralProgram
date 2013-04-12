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
  names = sorted(collect_names(form))
  if not names:
    return
  for values in product(*([B] * len(names))):
    yield dict(izip(names, values))


def exhaust(form):
  for meaning in all_meanings(form):
    yield meaning, reify(meaning, form)


s = lambda term: (str(term)
                  .replace(' ', '')
                  .replace("','", ' ')
                  .replace("'", '')
                  .replace(',', '')
                  .replace('(())', '◎')
                  .replace('()', '○')
                  )



# "All humans are mortal a.k.a. mortal OR NOT human
# IF NOT mortal THEN NOT human (Sorry, "The Highlander".)
#
c0 = or_('mortal', nor('human'))

for m, r in exhaust(c0):
  v = mark(r)
  print s(r), '->', int(v), m if v else ''
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
