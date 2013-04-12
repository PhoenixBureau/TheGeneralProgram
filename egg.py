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
