# -*- coding: utf-8 -*-
from itertools import product, imap, izip
from operator import eq
from string import ascii_lowercase
from collections import defaultdict


B = ((),), ()


mark = lambda form: not form or not any(imap(mark, form))
void = lambda form: any(not void(i) for i in form)


reduce_ = lambda form: B[mark(form)]


nor = lambda *bits: bits
or_ = lambda *bits: (bits,)
and_ = lambda *bits: tuple((bit,) for bit in bits)
nand = lambda *bits: (and_(*bits),)
xor = lambda *bits: (bits, and_(*bits))
nxor = lambda *bits: (xor(*bits),)


ifthen = lambda q, a, b: ((a, (q,)), (q, b))
flipflop = lambda q, r, s: ((s, q), r)


def implies(x, y):
  return nor(nor((x,), y))


# Forms with names.  (Tuples and strings.)


Records = depths, counts, names = {}, {}, {}


def unwrap(form):
  '''
  Remove all (()) and let ((*)) -> * in a form. Generator.
  '''
  for term in form:

    if term == ((),):
      continue

    if (isinstance(term, tuple)
        and len(term) == 1
        and isinstance(term[0], tuple)
        ):
      # Flatten out one "layer" of "wrapping".
      for item in term[0]:
        yield item
      continue

    yield term


_A = lambda form: (form if isinstance(form, basestring)
                   else tuple(unwrap(form)))


_B = lambda form: (form if isinstance(form, basestring)
                   else ((),) if () in form else form)


def Reduce(form):
  if isinstance(form, basestring):
    return form
  if (len(form) == 1
      and isinstance(form[0], tuple)
      and len(form[0]) == 1):
    return Reduce(form[0][0])
  return tuple(_A(_B(tuple(map(Reduce, form)))))


def depth(form):
  if isinstance(form, basestring):
    return 0
  return 1 + (max(depth(inner) for inner in form) if form else 0)


def count(form):
  if isinstance(form, basestring):
    return 0
  return 1 + sum(count(inner) for inner in form)


def sort_key(form):
  if isinstance(form, basestring):
    return 0, form
  return 1, depth(form), count(form)


def normalize(form):
  if isinstance(form, basestring):
    return form
  return tuple(sorted((normalize(inner) for inner in form), key=sort_key))


def walk(meaning, name, seen=None):
  if seen is None:
    seen = set()
  while name in meaning and meaning[name] != name:
    name = meaning[name]
    if name in seen:
      break
    seen.add(name)
  if isinstance(name, tuple):
    return tuple(walk(meaning, inner) for inner in name)
  return name


def reify(meaning, form):
  if isinstance(form, basestring):
    try:
      return walk(meaning, form)
    except RuntimeError:
      return form
  if isinstance(form, tuple):
    return tuple(reify(meaning, inner) for inner in form)
  return form


def assoc(meaning, key, value):
  d = meaning.copy()
  d[key] = value
  return d


def collect_names(form, names=None):
  if names is None:
    names = set()
  if isinstance(form, basestring):
    names.add(form)
  else:
    for inner in form:
      collect_names(inner, names)
  return names


def collect_names_histogram(form, names=None):
  if names is None:
    names = defaultdict(int)
  if isinstance(form, basestring):
    names[form] += 1
  else:
    for inner in form:
      collect_names_histogram(inner, names)
  return names


def names_by_frequency(form):
  c = collect_names_histogram(form)
  return sorted(c, key=lambda k: (-c[k], k))


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
  for m, r in exhaust(form):
    no_yes[mark(r)].append((m, r))
  return no_yes


def unify(u, v, s, eq=eq):
  """
  Find substitution so that u == v while satisfying s

  >>> unify((1, x), (1, 2), {})
  {x: 2}

  """
  u = walk(s, u)
  v = walk(s, v)
  if eq(u, v):
    return s
  if isinstance(u, basestring):
    return assoc(s, u, v)
  if isinstance(v, basestring):
    return assoc(s, v, u)
  if isinstance(u, tuple) and isinstance(v, tuple):
    if len(u) != len(v):
      return False
    for uu, vv in zip(u, v):  # avoiding recursion
      s = unify(uu, vv, s, eq)
      if s == False: # (instead of a Substitution object.)
        break
    return s
  return False


def name_normalize(form, symbols=ascii_lowercase):
  names = collect_names(form)
  meaning = dict(izip(sorted(names), symbols))
  return reify(meaning, form)


def name_normalize_by_frequency(form, symbols=ascii_lowercase):
  names = names_by_frequency(form)
  meaning = dict(izip(names, symbols))
  return reify(meaning, form)


def standard_form(x, form):
  Ex = reify({x: ((),)}, form)
  E_x_ = reify({x: ()}, form)
  return (x, Ex), ((x,), E_x_)


def fstan(form):
  for name in collect_names(form):
    form = Reduce(standard_form(name, form))
  return form


def record(form):
  form = normalize(Reduce(form))
#  form = name_normalize(form)
  if form in depths:
    return form, depths[form], counts[form], names[form]
  d = depths[form] = depth(form)
  c = counts[form] = count(form)
  n = names[form] = collect_names(form)
  return form, d, c, n


def cycle(register, program):
  '''
  Run one cycle of the program on the register.
  '''
  next_values = register.copy()
  for bit in register:
    next_value = reify(register, program.get(bit, bit))
    next_values[bit] = reduce_(next_value)
  register.update(next_values)


def view_register(r):
  '''
  Return a string representation of a register for insight.
  '''
  values = (r[bit] for bit in sorted(r))
  return ''.join(('-', 'O')[not v] for v in values)


def run_n_cycles(r, p, n=10, view=True):
  for i in range(n):
    if view:
      print view_register(r), i
    cycle(r, p)


def detect_cycle(r, p, view=True):
  seen = {}
  i = 0
  v = view_register(r)

  while v not in seen:
    if view:
      print
    seen[v] = i

    cycle(r, p)

    v = view_register(r)
    if view:
      print v, i,

    i += 1

  if view:
    print seen[v] - 1


s = lambda term: (str(term)
                  .replace(' ', '')
                  .replace("','", ' ')
                  .replace("'", '')
                  .replace(',', '')
                  .replace('(())', '◎')
                  .replace('()', '○')
                  )
