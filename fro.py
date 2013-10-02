from itertools import product, imap, izip


class f(frozenset):

  def __repr__(self):
    return '(%s)' % ' '.join(map(repr, self))


a = f()
mark = lambda form: not form or not any(imap(mark, form))

nor = lambda *bits: f(bits)
or_ = lambda *bits: nor(f(bits))
and_ = lambda *bits: f(f((bit,)) for bit in bits)
nand = lambda *bits: f((and_(*bits),))
xor = lambda *bits: f((and_(*bits), f(bits)))


def implies(x, y):
  return f(f(f((x,)), y))


print xor(7, 8, 9, 7)


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

##  Python 2.7.3 (default, Apr 10 2013, 06:20:15) 
##  [GCC 4.6.3] on linux2
##  Type "copyright", "credits" or "license()" for more information.
##  >>> ================================ RESTART ================================
##  >>> 
##  ((8 9 7) ((7) (8) (9)))
##  >>> k = xor(1, 2, 3)
##  >>> k
##  (((2) (3) (1)) (1 2 3))
##  >>> k0 = or_(1, 2, 3)
##  >>> k0
##  ((1 2 3))
##  >>> k0 = nor(1, 2, 3)
##  >>> k0
##  (1 2 3)
##  >>> k0 in k
##  True
##  >>> insert(k, 32, k0)
##  (32 ((2) (3) (1)))
##  >>> k0 = and_(1, 2, 3)
##  >>> k0 in k
##  True
##  >>> insert(k, 32, k0)
##  (32 (1 2 3))
##  >>> k1 = nor(3)
##  >>> k!
##  SyntaxError: invalid syntax
##  >>> k1
##  (3)
##  >>> insert(k, 32, k0, k1)
##  ((1 2 3) (32 (2) (1)))
##  >>> insert(k, 32, k0, k1, 3)
##  ((1 2 3) ((2) (32) (1)))
##  >>> 
