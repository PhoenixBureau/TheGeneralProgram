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


def unwrap(form):
  '''
  Remove all (()) and let ((*)) -> * in a form. Generator.
  '''
  for term in form:
    if term == ((),):
      continue
    if isinstance(term, tuple) and len(term) == 1 and isinstance(term[0], tuple):
      # Flatten out one "layer" of "wrapping".
      for item in term[0]:
        yield item
    else:
      yield term


_A = lambda form: (form
                   if isinstance(form, basestring)
                   else tuple(unwrap(form)))


_B = lambda form: (form
                   if isinstance(form, basestring)
                   else ((),) if () in form else form)


def Reduce(form):
  if isinstance(form, basestring):
    return form
  if (len(form) == 1
      and isinstance(form[0], tuple)
      and len(form[0]) == 1):
    return Reduce(form[0][0])
  return tuple(_A(_B(tuple(map(Reduce, form)))))


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
