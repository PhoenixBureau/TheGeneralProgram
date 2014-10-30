# -*- coding: utf-8 -*-
from itertools import product, imap, izip
from operator import eq
from string import ascii_lowercase
from collections import defaultdict, Counter
from operator import add


Void, Mark = B = ((),), ()


mark = lambda form: not form or not any(imap(mark, form))
void = lambda form: any(not void(i) for i in form)


reduce_ = lambda form: B[mark(form)]


nor = lambda *bits: bits
or_ = lambda *bits: (bits,)
and_ = lambda *bits: tuple((bit,) for bit in bits)
nand = lambda *bits: (and_(*bits),)
xor = lambda *bits: (bits, and_(*bits))
nxor = lambda *bits: (xor(*bits),)

# Note the the above names for the basic logic functions work for the
#     True = () ; False = (()) interpretation.
# For the dual interpretation the names are "opposite".
# I.e.   a b <--> ((a)(b))  and/or  etc..

ifthen = lambda q, a, b: ((a, (q,)), (q, b))
flipflop = lambda q, r, s: ((s, q), r)


LEAF_TYPES = int, str, unicode
CONTAINER_TYPES = tuple, set, frozenset, list


def is_leaf(n): return isinstance(n, LEAF_TYPES)
def is_container(n): return isinstance(n, CONTAINER_TYPES)


VOIDS = {
  tuple: Void,
  frozenset: frozenset({frozenset()}),
  list: [[]],
  }


def leaf_check(F):
  return lambda form, *a, **b: form if is_leaf(form) else F(form, *a, **b)


def make_container_converter(T):
  '''
  Return a function that returns the result of recursively converting each
  of the containers in the form to the type T.
  '''
  cc = leaf_check(lambda form: T(map(cc, form)))
  return cc


frozenset_converter = make_container_converter(frozenset)
tuple_converter = make_container_converter(tuple)
list_converter = make_container_converter(list)


# Return the first item in a container, for sets and frozensets return
# any item.
first_of = lambda form: next(iter(form))


def can_unwrap(term):
  return (
    is_container(term)
    and len(term) == 1
    and is_container(first_of(term))
    )


def _unwrap(form):
  for term in form:
    if can_unwrap(term):
      for item in first_of(term):
        yield item
    else:
      yield term


# Remove all voids (()) and let ((*)) -> * in the first "depth" of a form.
unwrap = leaf_check(lambda form: type(form)(_unwrap(form)))


@leaf_check
def _B(form):
  for term in form:
    if not term: # term is a Mark.
      return VOIDS[type(form)]
  return form


@leaf_check
def Reduce(form):
  if len(form) == 1:
    inner = first_of(form)
    if is_container(inner) and len(inner) == 1:
      # form = ((foo)) = foo
      return Reduce(first_of(inner))
  T = type(form)
  return T(unwrap(_B(T(map(Reduce, form)))))


@leaf_check
def pervade(E, ex):
  '''
  Given a form E and a set of terms that are to be pervaded (excluded)
  from the form, return the result of Pervasion.  Note that this function
  will also collect and pervade literals as it goes along, so if you pass
  in an empty set for ex you'll get a (possibly) reduced form if there
  are any redundant literals in it.
  '''
  lits = leaves_of(E) - ex
  ex = ex | lits
  for i in E:
    if is_leaf(i): continue
    e = pervade(i, ex)
    if not e: return Void
    if e != Void: lits.add(e)
  return type(E)(lits)


def make_recursive_application(F, base=0, per=1, op=add):
  def w(form):
    if is_leaf(form): return base
    return op(per, F(map(w, form)))
  return w


count = make_recursive_application(sum)
depth = make_recursive_application(lambda s: max(s) if s else 0)
                                  # Built-in max() fails on empty s.

# The above is a refactoring of the two functions below:
#
##  def depth(form):
##    if is_leaf(form): return 0
##    return 1 + MAX(imap(depth, form))
##
##
##  def count(form):
##    if is_leaf(form): return 0
##    return 1 + sum(imap(count, form))


def sort_key(form):
  '''
  Leaf terms sort before containers and then by lexographic (whatever python does)
  containers sort after leaves and then by depth, then by count.
  '''
  if is_leaf(form): return 0, form
  return 1, depth(form), count(form)


@leaf_check
def normalize(form):
  return type(form)(sorted(map(normalize, form), key=sort_key))


def reify(meaning, form):
  if is_leaf(form): return meaning.get(form, form)
  return type(form)(reify(meaning, inner) for inner in form)


leaves_of = lambda E: set(i for i in E if is_leaf(i))


def yield_leaves(form):
  if is_leaf(form):
    yield form
  else:
    for inner in form:
      for leaf in yield_leaves(inner):
        yield leaf


def collect_names(form):
  return set(yield_leaves(form))


def collect_names_histogram(form, names=None):
  return Counter(yield_leaves(form))


def names_by_frequency(form):
  c = collect_names_histogram(form)
  return sorted(c, key=lambda k: (-c[k], k))


def all_meanings(form):
  names = collect_names(form)
  if not names: return
  universe = [B] * len(names)
  for values in product(*universe):
    yield dict(izip(names, values))
    # Note that even though names is a set we can iterate over it several
    # times and expect the order to remain stable because we are not
    # altering the set in the meantime.  If this worries you feel free to
    # convert names to a (possibly sorted) list or something...


def exhaust(form):
  '''
  For all possible mappings from the variables in form to the domain B
  yield the mapping and the reification of the form with that mapping.
  '''
  for meaning in all_meanings(form): yield meaning, reify(meaning, form)


marks_of_meaning = lambda m: {n for n, e in m if mark(e)}
voids_of_meaning = lambda m: {n for n, e in m if void(e)}


def setsolve(form, marks):
  '''
  Given a form and a set of names that are Marks assume all other names
  in the form are Void and reduce to basic value (Mark or Void.)
  '''
  for inner in form:
    if is_leaf(inner):
      if inner in marks: return Void
      # else assume inner is Void and omit it.
    elif not setsolve(inner, marks): # Mark
      return Void
  return Mark


def setcycle(R, P):
  # To calculate the new R first collect all the signals in R that are
  # marks but that are not mentioned in the current P (and so cannot be
  # set to Void by it) then add the marks generated by solving P's
  # expressions with the marks in R.
  return R.difference(P).union(
    signal
    for signal, expression in P.iteritems()
    if not setsolve(expression, R)
    )


def solve(form):
  '''
  Return two lists containing the mappings from the variables in form to
  the domain B, one of which is the satisfying mappings and the other is
  the unsatisfying mappings.

  (If a form has no satisfying mappings then it is "unsatisfiable"; if it
  has no unsatisfying mappings it is a Tautology.)
  '''
  solutions = [], []
  for meaning, expression in exhaust(form):
    solutions[void(expression)].append(meaning)
  return solutions


def name_normalize(form, symbols=ascii_lowercase):
  '''
  Return the form with variable names remapped to those in symbols.
  '''
  names = collect_names(form)
  if len(names) > len(symbols): raise Exception('Not enough symbols')
  return reify(dict(izip(sorted(names), symbols)), form)


def name_normalize_by_frequency(form, symbols=ascii_lowercase):
  names = names_by_frequency(form)
  if len(names) > len(symbols): raise Exception('Not enough symbols')
  return reify(dict(izip(names, symbols)), form)


def standard_form(x, form):
  '''
  Return the "Standard Form" of form in the variable x.
  '''
  Ex = reify({x: ((),)}, form) # Replace x with Void.
  E_x_ = reify({x: ()}, form) # Replace x with Mark.
  return (x, Ex), ((x,), E_x_)


def fstan(form):
  '''
  Return the result of making the Standard Form of the form for each
  variable in the form.

  This isn't quite right.  It should result in clauses representing each
  satisfying set of values for the variables in the form, but I got the
  geometry wrong and instead it does something similar but not the same...
  '''
  for name in collect_names(form):
    form = Reduce(standard_form(name, form))
  return form


def reduce_string_bricken_bit_engine(s):
  '''
  Return the Mark|Void value of a string of balanced '(' ')' pairs.
  '''
  # FIXME: use and index instead of s = s[n:] inefficient!
  c = 0
  while s and s != '()':
    while s.startswith('(())'): s = s[4:]
    while s.startswith('()()'): s = s[2:]
    while s.startswith('))'):
      s = s[2:]
      c -= 2
    if s.startswith(')'):
      c -= 1
      s = '()' + occlude(s[1:])
    else: # s.startswith('(')
      s = s[1:]
      c +=1
    if c < 0:
      raise Exception('Mal-formed form')
  return s


def occlude(s):
  '''
  Given a string that consists of a prefix of balanced parentheses
  followed by a closing ')' (and optionally more chars) or the empty
  string, return the string without the prefix.

  This function is a helper for removing "occluded" terms following a
  Mark value in a string LoF expression.
  '''
  c = 0
  for i, ch in enumerate(s):
    c += (1, -1)[ch == ')']
    if c < 0: return s[i:]
  return ''


def reduce_string(s):
  '''
  Return the Mark|Void value of a string of balanced '(' ')' pairs.

  (I suspect this will be faster than reduce_string_bricken_bit_engine()
  but only due to being written in Python.  This version uses built-in
  str.replace() which should be faster than chewing through the string in
  a Python loop like reduce_string_bricken_bit_engine() does.)
  '''
  while True:
    n = len(s)
    s = s.replace('(())', '').replace('()()', '()')
    if len(s) == n: # No further reduction.
      break
  if s and s != '()':
    raise Exception('Mal-formed form')
  return s


def INS(E):
  '''
  Return the result of attempting Bricken's "Set Insertion" to reduce E.
  '''
  a = set()
  for into in E:
    put = frozenset(E).difference({into})
    i = ins(into, put)
    if not i: return Void
    if i != Void: a.add(i)
  return type(E)(a)


@leaf_check
def ins(into, put):
  '''
  Calculate the effect of "virtual" insertion of the terms in put into
  the into form.

  The terms will be (possibly) reduced by pervasion of the literals in
  the into form, and if any of the terms should be reduced to the Mark
  then the value of the into form is Void, and 
  '''
  lits = leaves_of(into)
  if lits:
    put = pervade(put, lits)
    if not put: return into # all the put terms went to Void
    if put == Void: return Void # A Mark was found
  for inner in into:
    if inner in lits: continue
    inner = ins(inner, put)
    if not inner: return Void
    if inner != Void: lits.add(inner)
  return type(into)(lits)


def dpll(E, partial=None, unit=True):
  if partial is None: partial = {}
  if unit:
    partial = partial.copy() # so we can backtrack later..
    E = assign_unit_clauses(E, partial)
  if not E: return partial
  if Mark in E: return
  v = next_symbol_of(E)
  partial[v] = Mark
  res = dpll(pervade(E, {v}), partial, unit)
  if res is not None: return res
  partial[v] = Void
  return dpll(markit(E, v), partial, unit)


def assign_unit_clauses(E, partial):
  on, off, E = find_units(E)
  while on or off:
    while on:
      if on & off: return Void
      term = first_of(on)
      partial[term] = Mark
      ON, OFF, E = find_units(markit(E, term))
      on |= ON
      on.remove(term)
      off |= OFF
    while off:
      if on & off: return Void
      term = first_of(off)
      partial[term] = Void
      ON, OFF, E = find_units(pervade(E, {term}))
      off |= OFF
      off.remove(term)
      on |= ON
  return E


@leaf_check
def next_symbol_of(E):
  for it in E: return next_symbol_of(it)
  raise Exception("no more symbols")


def find_units(E):
  '''
  Return two sets and a possibly-reduced E.  The literals in the first
  set must be Void and those in the second must be set Mark to have the
  entire expression become Void.
  '''
  on, off, poly = set(), set(), set()
  for clause in E:
    if len(clause) != 1:
      poly.add(clause)
      continue
    (n,) = clause # Unwrap one layer of containment.
    if is_leaf(n):
      on.add(n)
    elif len(n) == 1:
      (n,) = n
      off.add(n)
  return on, off, type(E)(poly)


@leaf_check
def markit(E, m):
  a = set()
  for inner in E:
    if inner == m: return Void
    inner = markit(inner, m)
    if not inner: return Void
    if inner != Void: a.add(inner)
  return type(E)(a)


##@leaf_check
##def occlude_pervade(E, marks, voids):
##  '''
##  Given a form E and a set of Marks and a set of Voids, return the
##  reduced form.
##  '''
##  a = []
##  marks, voids = marks.copy(), voids.copy()
##  for inner in E:
##
##    if inner in marks: return Void
##    if inner in voids: continue
##
##    if is_leaf(inner):
##      voids.add(inner)
##    elif len(inner) == 1:
##      term = first_of(inner)
##      if is_leaf(term):
##        if term in voids: # inner is Mark
##          return Void
##        if term in marks: # inner is Void
##          continue
##        marks.add(term)
##
##    inner = occlude_pervade(inner, marks, voids)
##
##    if not inner: return Void
##    if inner != Void: a.append(inner)
##
##  return type(E)(a)


def paren_gen(left, right=0, ans='', rank=0, variables=None):
  '''
  Generate the well-formed expressions of n=left parentheses pairs.

  Pass in an optional variables iterable to have named variables appear
  in the expression.
  '''
  if not rank: rank = left
  if variables is None: variables = ['' for n in range(rank)]

  if not (left or right):
    yield ans
    return

  if left > 0:
    for i in paren_gen(
      left - 1,
      right + 1,
      ans + '(' + variables[rank - left],
      rank,
      variables,
      ):
      yield i

  if right > 0:
    for i in paren_gen(
      left,
      right - 1,
      ans + ')',
      rank,
      variables,
      ):
      yield i


s = lambda term: (str(normalize(tuple_converter(term)))
                  .replace(' ', '')
                  .replace("','", ' ')
                  .replace("'", '')
                  .replace(',', '')
                  .replace('(())', '◎')
                  .replace('()', '○')
                  )


def _view(r, u):
  return ''.join('.O'[n in r] for n in u)


if __name__ == '__main__':
  from pprint import pformat

  a, b, c, d = 'abcd'
  U = a, b, c, d
  D = {n: n for n in U}
  V = [n + ',' for n in U]
  M = list(all_meanings(U))
  R = set(U)
  P = {
    a: (( (a, (b,)), ((a,), b) ),),
    b: ((a, c),),
    c: (a,),
    }

  for E in paren_gen(5, variables=V+[V[0]]):
    print E
    e = frozenset_converter(eval(E.replace(')', '),')))
    S0 = map(sorted, solve(e))
    S1 = [], []

    for m in M:
      ms = marks_of_meaning(m.items())
      S1[bool(setsolve(e, ms))].append(m)

    S1 = map(sorted, S1)
    if S0 != S1:
      print E
      break
  else:
    print 'solutions match!'

##
##      e = e.replace(')', '),')
##      print
##      print e
##  ##    F = fstan(E)
##
##      for m in M:
##        E = eval(e, {}, m)
##        print s(E), void(E)
##
##  ##    print s(F)
##      print '-' * 20
##
##  ##  print 
##  ##  print e.replace('(', '(a')
##  ##  print '-' * 20

