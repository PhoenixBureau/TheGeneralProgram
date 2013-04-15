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


def assoc(meaning, key, value):
  d = meaning.copy()
  d[key] = value
  return d


def unify(u, v, s):
  """
  Find substitution so that u == v while satisfying s

  >>> unify((1, x), (1, 2), {})
  {x: 2}

  """
  u = walk(s, u)
  v = walk(s, v)
  if u == v:
    return s
  if isinstance(u, basestring):
    return assoc(s, u, v)
  if isinstance(v, basestring):
    return assoc(s, v, u)
  if isinstance(u, tuple) and isinstance(v, tuple):
    if len(u) != len(v):
      return False
    for uu, vv in zip(u, v):  # avoiding recursion
      s = unify(uu, vv, s)
      if s == False: # (instead of a Substitution object.)
        break
    return s
  return False


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


def check(goal, rules):
  for rule in rules:
    s = unify(rule[0], goal, {})
    if s != False: # as opposed to an empty dict.
      # Proc head matches.
      return s, rule[1:]


def grind(out, goals, rules):
  S = {}
  while goals:
    goal = goals.pop(0)
    s, rule_body = check(goal, rules)
    if rule_body:
      goals.extend(rule_body)
      goals = [reify(s, goal) for goal in goals]
    S.update(s)
  return reify(S, out)


if __name__ == '__main__':
  a = 'append', (), 'x', 'x'

  p = 'append', ('cons', 'x', 'y'), 'z', ('cons', 'x', 'u')
  u = 'append',        'y',         'z',        'u'

  g = 'append', ('cons', 'a', ()), ('cons', 'b', ()), 'v'


  Rules = [(a,), (p, u)]
  goals = [g]


  print grind('v', [g], Rules)

##  a = 'a', 'b', 'c'
##  b = 'b', 'c', 'd'
##  c = 'c', 'e', 'd'
##  rules = [a, b, c]
##  goals = ['a']
