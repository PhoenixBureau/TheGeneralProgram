from collections import defaultdict
from egg import *


names = 'nor or_ and_ nand xor'.split()
operations = dict(zip(names, (nor, or_, and_, nand, xor)))


def simple_computer(a, b, c):
  return nor(b, c), nor(c), nor(a, nor(c))


a, b, c = register = simple_computer(*'abc')


def print_register(reg):
  T = product(B, B, B)
  for bit_expression in reg:
    for a, b, c in T:
      meaning = {'a': a, 'b': b, 'c': c}
      print s(a), s(b), s(c), '->', s(Reduce(reify(meaning, bit_expression)))
  print '-' * 16


def print_register(reg):
  for bit_expression in reg:
    fb = fstan(bit_expression)
    print s(bit_expression)
    print s(fb)
    print ' '.join(sorted(collect_names(bit_expression)))
    for meaning, r in exhaust(bit_expression):
      rfb = reify(meaning, fb)
      for name, expression in view_meaning(meaning):
        print expression,
      print '->', s(Reduce(r)), s(Reduce(rfb))
    print '-' * 16
  print '=' * 16


def view_meaning(m):
  for name in sorted(m):
    yield name, s(m[name])


print_register(register)
register = simple_computer(*register)
print_register(register)
register = simple_computer(*register)
print_register(register)
register = simple_computer(*register)
print_register(register)
register = simple_computer(*register)
print_register(register)


def print_simple_computer(n=4):
  T = list(product(B, B, B))[::-1]
  for a, b, c in T:
    print '=' * 16
    for gen in range(n):
      print s(a), s(b), s(c), 'cycle:', gen
      a, b, c = simple_computer(a, b, c)
      aa, bb, cc = map(Reduce, (a, b, c))
      print s(aa), s(bb), s(cc), 'cycle:', gen
