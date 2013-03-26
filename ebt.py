'''

  Every Bit Tells

Based on "Functional Pearl: Every Bit Counts"
by Dimitrios Vytiniotis & Andrew J. Kennedy
https://dl.acm.org/citation.cfm?id=1863548
'''
from operator import sub, add


a = lambda n: n == 0
b = lambda n: n == 1
c = lambda n: n == 2


G = (a, (0, 1))


def decode(game, value):
  predicate, choices = game
  it = choices[not predicate(value)]
  if isinstance(it, tuple):
    return decode(it, value)
  return it


def F(N, op=sub, arg=1):
  if not N: return N
  return (
    lambda n: n == N,
    (N, F(op(N, arg), op, arg))
    )


if __name__ == '__main__':
  V = F(3)
  for n in range(-2, 7): print decode(V, n),
  print

  B = F(-3, add, 1)
  for n in range(-4, 1): print decode(B, n),
  print
