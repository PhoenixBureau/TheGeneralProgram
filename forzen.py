from itertools import imap


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
