'''

  Every Bit Tells

Based on "Functional Pearl: Every Bit Counts"
by Dimitrios Vytiniotis & Andrew J. Kennedy
https://dl.acm.org/citation.cfm?id=1863548
'''
from operator import sub, add
from pprint import pprint


def encode(game, value, path=None):
  if path is None:
    path = []

  predicate, choices = game

  P = predicate(value) # Invert to index the branches.
                           # True takes left
                           # False takes right branch.
  path.append(int(P))

  it = choices[not P]

  if isinstance(it, tuple):
    return encode(it, value, path)

  if it == value:
    return path
  return []


def decode(game, path):
  for bit in path:
    _, choices = game
    game = choices[not bit]
  return game


def list_codes(game, path=None):
  if path is None:
    path = []
  if not isinstance(game, tuple):
    yield path, game
  else:
    f, (l, r) = game
    for P, leaf in list_codes(l, path[:] + [1]):
      yield P, leaf
    for P, leaf in list_codes(r, path[:] + [0]):
      yield P, leaf


def F(N, op=sub, arg=1):
  if not N: return N
  return (
    lambda n: n == N,
    (N, F(op(N, arg), op, arg))
    )


def O(n, m):
  if n == m:
    return n
  assert n < m, (n, m)
  midpoint = n + (m - n) / 2
  f = lambda number: number <= midpoint
  return f, (O(n, midpoint), O(midpoint + 1, m))


if __name__ == '__main__':
  o = O(0, 10)
  for p, g in list_codes(o):
    d = decode(o, p)
    print '%-2s -> %r = %s' % (g, p, d)
    assert d == g ,(d, g)

  print '-' * 70
  o = O(0, 15)
  for p, g in list_codes(o):
    d = decode(o, p)
    print '%-2s -> %r = %s' % (g, p, d)
    assert d == g ,(d, g)

  print '-' * 70
  o = O(33, 35)
  for p, g in list_codes(o):
    d = decode(o, p)
    print '%-2s -> %r = %s' % (g, p, d)
    assert d == g ,(d, g)


  print '-' * 70
  print '-' * 70



  V = F(3)
  for n in range(-2, 7):
    path = encode(V, n)
    print n, path, decode(V, path) if path else None
  print

  B = F(-3, add, 1)
  for n in range(-4, 2):
    path = encode(B, n)
    print n, path, decode(B, path) if path else None
  print
