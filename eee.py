from collections import defaultdict
from itertools import imap


mark = lambda form: not form or not any(imap(mark, form))


nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(and_(*bits))
xor = lambda *bits: nor(and_(*bits), nor(*bits))

s = lambda form: int(not mark(form))

names = 'nor or_ and_ nand xor'.split()
operations = dict(zip(names, (nor, or_, and_, nand, xor)))

truth_tables = defaultdict(dict)
B = (), ((),)
T = ((op, a, b) for op in operations for a in B for b in B)

for op, a, b in T:
  truth_tables[op][1-s(a), 1-s(b)] = 1-s(operations[op](a, b))

##for op, table in truth_tables.iteritems():
##  print '', op
##  print '-' * 6
##  for a, b in sorted(table):
##    print ' %i%i|%i' % (a, b, table[a, b])
##  print

v = lambda term: str(term).replace("'", '').replace(" ", '').replace(",", '')


def simple_computer(a, b, c):
  return nor(b, c), nor(c), nor(a, nor(c))


a, b, c = register = simple_computer(*'abc')


def reify(form, meaning={}):
  if isinstance(form, tuple):
    return tuple(reify(inner, meaning) for inner in form)
  return meaning.get(form, form)


def print_register(reg):
  T = [(a, b, c) for a in B for b in B for c in B]
  for bit_expression in reg:
    print v(bit_expression), '->'
    for a, b, c in T:
      meaning = {'a': a, 'b': b, 'c': c}
      print 1-s(a), 1-s(b), 1-s(c), '->', 1-s(reify(bit_expression, meaning))
  print '-' * 16



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
  T = [(a, b, c) for a in B for b in B for c in B][::-1]
  for a, b, c in T:
    print '=' * 16
    for gen in range(n):
      print 1-s(a), 1-s(b), 1-s(c), 'cycle:', gen
      a, b, c = simple_computer(a, b, c)

##
##  print_simple_computer(5)
##
##
##
##         100 -->\
##                 110 -> 010
##  111 -> 000 -->/
##
##  011 -> 001




##    ================
##    0 0 0 cycle: 0
##    1 1 0 cycle: 1
##    0 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
##    ================
##    0 0 1 cycle: 0
##    0 0 1 cycle: 1
##    0 0 1 cycle: 2
##    0 0 1 cycle: 3
##    0 0 1 cycle: 4
##    ================
##    0 1 0 cycle: 0
##    0 1 0 cycle: 1
##    0 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
##    ================
##    0 1 1 cycle: 0
##    0 0 1 cycle: 1
##    0 0 1 cycle: 2
##    0 0 1 cycle: 3
##    0 0 1 cycle: 4
##    ================
##    1 0 0 cycle: 0
##    1 1 0 cycle: 1
##    0 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
##    ================
##    1 0 1 cycle: 0
##    0 0 0 cycle: 1
##    1 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
##    ================
##    1 1 0 cycle: 0
##    0 1 0 cycle: 1
##    0 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
##    ================
##    1 1 1 cycle: 0
##    0 0 0 cycle: 1
##    1 1 0 cycle: 2
##    0 1 0 cycle: 3
##    0 1 0 cycle: 4
