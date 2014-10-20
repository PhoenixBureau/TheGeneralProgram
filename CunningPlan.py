from itertools import izip_longest
from pprint import pformat
from egg import Reduce
from void import pretty, truth_table, reify, void


nor = lambda *bits: bits
or_ = lambda *bits: (bits,)
and_ = lambda *bits: tuple((bit,) for bit in bits)
nand = lambda *bits: (and_(*bits),)
xor = lambda x, y: (((x, (y,)), ((x,), y)),)

ifthen = lambda q, a, b: ((a, (q,)), (q, b))
flipflop = lambda q, r, s: ((s, q), r)


def cascade(qs, ms, x):
  for q, m in zip(qs, ms):
    x = ifthen(q, m, x)
  return Reduce(x)


def ram(length, width):
  r = {}
  for rank in range(length):
    prefix = 'mem:%s.' % (rank,)
    for i in range(width):
      m = prefix + str(i)
      r[m] = m
  return r


def selector(power_of_two, prefix='sel:'):
  names = [prefix + str(n) for n in range(power_of_two)]
  clauses = [
    tuple(
      name if i & 2**n else (name,)
      for n, name in enumerate(names)
      )
    for i in range(2**power_of_two)
    ]
  return names, clauses


a, b, c = 'abc'
w, x, y, z = 'wxyz'
q, i, rw, select = 'qirs'


sel, clauses = selector(3)
memory = ram(1, 8)


def acc(pairs, load):
  return {
    'a:%i' % (n,): ifthen(load, true, false)
    for n, (true, false) in enumerate(pairs)
    }


P = {

  b: cascade(clauses, sorted(memory), b),

  'sel:0': 'sel:0', # (xor(b, 'sel:0',),),
  'sel:1': 'sel:1', # xor('sel:0', 'sel:1'),
  'sel:2': 'sel:2', # xor('sel:1', 'sel:2'),

  'mem:0.0': xor('mem:0.0', 'mem:0.1'),
  'mem:0.1': xor('mem:0.1', 'mem:0.2'),
  'mem:0.2': xor('mem:0.2', 'mem:0.3'),
  'mem:0.3': xor('mem:0.3', 'mem:0.4'),
  'mem:0.4': xor('mem:0.4', 'mem:0.5'),
  'mem:0.5': xor('mem:0.5', 'mem:0.6'),
  'mem:0.6': xor('mem:0.6', 'mem:0.7'),
  'mem:0.7': xor('mem:0.7', 'mem:0.0'),

  'load': 'mem:0.5',

  }

J = {}
J.update(memory)
J.update(acc(zip(sorted(memory), b * len(memory)), 'load'))
J.update((s, s) for s in sel)
J.update(P)

R = dict.fromkeys(J, ((),))
R['sel:0'] = R['sel:2'] = ()
R['mem:0.7'] = ()
R['load'] = R['sel:1'] = ((),)


_view = lambda r: ''.join(
  '_O'[not r[n]]
  for n in sorted(r)
  )

def _p(*a, **b):
  print pformat(*a, **b)


def cyc(r, p):
##  _p(r); print '=' * 10
  print _view(R)
  return {
    name: Reduce(reify(p[name], r))
    for name in p
    }

#_p(J); print '_' * 10; print

_p(J)
print '=' * 10
print
for n in map(''.join, izip_longest(*sorted(J), fillvalue='|')):
  print n

for _ in range(12):
  R = cyc(R, J)

##_p(R); print '=' * 10
print _view(R)



##E = J[b]
##from egg import fstan
##F = fstan(E)
##for c in F:
##  print pretty(c)



##
##def mem_read(a, b, mem):
##  M = dict(a=a, b=b)
##  m = reify(mem, M)
##  print pretty(m)
##  return void(m)
##
##def memory_location(q, bit):
##  return flipflop(q, nor(bit), bit)
##
##
####wxyz = (a, b), (a, (b,)), ((a,), b), ((a,), (b,))
####ab = ((y, z),), ((x, z),)
##
##
##mem_read((), (), xor(a, b))
##
####for form in (
####  nor(a, b, c),
####  or_(a, b, c),
####  and_(a, b, c),
####  nand(a, b, c),
####  xor(a, b),
####  ifthen(c, a, b),
####  flipflop(a, b, c),
####  ):
####  print pretty(form) ; print
####  truth_table(form) ; print ; print
##
##
##def memory_cell(q, i, rw, select):
##  nrw = nor(rw)
##  r = nand(i, nrw, select)
##  s = nand(nor(i), nrw, select)
##  q = flipflop(q, nor(r), nor(s))
##  return q, Reduce(and_(rw, q, select))
##
##
##Q, m = memory_cell(q, i, rw, select)
##
##P = {
##  q: Q,
##  'm': m,
##  }
##
##
