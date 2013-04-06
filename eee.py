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

for op, table in truth_tables.iteritems():
  print '', op
  print '-' * 6
  for a, b in sorted(table):
    print ' %i%i|%i' % (a, b, table[a, b])
  print
