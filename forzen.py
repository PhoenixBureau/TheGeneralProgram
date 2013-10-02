from itertools import imap, product, izip


class f(frozenset):

  def __repr__(self):
    return '(%s)' % ' '.join(map(repr, self))


mark = lambda form: not form or not any(imap(mark, form))

nor = lambda *bits: f(bits)
or_ = lambda *bits: nor(f(bits))
and_ = lambda *bits: f(f((bit,)) for bit in bits)
nand = lambda *bits: f((and_(*bits),))
xor = lambda *bits: f((and_(*bits), f(bits)))


def implies(x, y):
  return f(f(f((x,)), y))


def insert(form, replacement, *indicies):
  if not indicies:
    return replacement
  index, rest = indicies[0], indicies[1:]
  return f(
    inner
    if inner != index
    else insert(inner, replacement, *rest)
    for inner in form
    )


a = f()
b = nor(a)
c = nor(b)
j = xor(a, a, a, a)
k = xor(1, 2, 3)

B = a, b


def FBA(a, b, Cin):
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, Cin)
  return nor(j, nor(y, Cin)), or_(j, h)

fba = FBA('a', 'b', 'Cin')


def reify(meaning, form):
  if not isinstance(form, f):
    return meaning.get(form, form)
  return f(tuple(reify(meaning, inner) for inner in form))


def collect_names(form, names=None):
  if names is None:
    names = set()
  if not isinstance(form, f):
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
  for m, r in exhaust(form):
    no_yes[mark(r)].append((m, r))
  return no_yes


for m, o in exhaust(fba[0]):
  c = reify(m, fba[1])
  print int(not mark(o)), int(not mark(c)), m
##  print o
##  print c
  print


## This is how insert works.
##
##  >>> 
##  >>> a = f()
##  >>> j = xor(a, a, a, a)
##  >>> j
##  ((()) ((())))
##  >>> mark(j)
##  False
##  >>> insert(j, 23, a)
##  ((()) ((())))
##  >>> e = _
##  >>> e == j, e is j
##  (True, False)
##  >>> insert(j, 23, f((a,)))
##  (((())) 23)
##  >>> insert(j, 23, f((a,)), a)
##  ((23) ((())))
##  >>> insert(j, 23, f((a,)), a, a)
##  ((()) ((())))
##  >>> 
##
##  >>> ================================ RESTART ================================
##  >>> 
##  >>> a = f()
##  >>> j = xor(a, a, a, a)
##  >>> j
##  ((()) ((())))
##  >>> mark(j)
##  False
##  >>> insert(j, 23, a)
##  ((()) ((())))
##  >>> e = _
##  >>> e == j, e is j
##  (True, False)
##  >>> insert(j, 23, f((a,)))
##  (((())) 23)
##  >>> insert(j, 23, f((a,)), a)
##  ((23) ((())))
##  >>> insert(j, 23, f((a,)), a, a)
##  ((()) ((())))
##  >>> insert(j, 23, f((f((a,)),)), f((a,)), a)
##  ((()) ((23)))
##  >>> insert(j, 23, f((f((a,)),)), f((a,)))
##  ((23) (()))
##  >>> insert(j, 23, f((f((a,)),)))
##  ((()) 23)
##  >>> ================================ RESTART ================================
##  >>> 
##  >>> a
##  ()
##  >>> b
##  (())
##  >>> c
##  ((()))
##  >>> j
##  ((()) ((())))
##  >>> b in j
##  True
##  >>> c in j
##  True
##  >>> insert(j, 23, c)
##  ((()) 23)
##  >>> insert(j, 23, c, b)
##  ((23) (()))
##  >>> insert(j, 23, c, b, a)
##  ((()) ((23)))
##  >>> insert(j, 23, b)
##  (((())) 23)
##  >>> insert(j, 23, b, a)
##  ((23) ((())))


F = {}


def _f(form):
  return F.setdefault(form, form)



##from itertools import combinations
##
##def comb(A):
##  for n in xrange(1, len(A) + 1):
##    for c in combinations(A, n):
##      yield f(c)
##
##
##a = _f(f())
##b = _f(f([a]))
##
##
##for n in comb(list(F)):
##  print n
##  _f(n)
##for n in sorted(F):
##  print n
##
##print '*' * 23
##
##for n in comb(list(F)):
##  print n
##  _f(n)
##for n in sorted(F):
##  print n
##
