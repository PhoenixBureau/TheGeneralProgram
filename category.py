from itertools import imap
from pprint import pprint as p


mark = lambda form: not form or not any(imap(mark, form))


nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(tuple((nor(bit) for bit in bits)))
xor = lambda *bits: nor(and_(*bits), nor(*bits))


C = set((1, 2, 3))
hom = {}

for item in C:
  hom[item, item] = lambda n: n

f0 = lambda n: n + 1

hom[1, 2] = set()
hom[1, 2].add(f0)

hom[2, 3] = set()
hom[2, 3].add(f0)
 

machine = {
  '100': '110',
  '110': '010',
  '111': '000',
  '000': '110',
  '011': '001',
  }


def future(m, state, time):
  for _ in range(time):
    state = m.get(state, state)
  return state



def reify(meaning, form):
  if isinstance(form, basestring):
    return walkstar(meaning, form)
  if isinstance(form, tuple):
    return tuple(reify(meaning, inner) for inner in form)
  return form


def walkstar(meaning, key):
  key = walk(meaning, key)
  if isinstance(key, tuple):
    return tuple(walkstar(meaning, inner) for inner in key)
  return key


def walk(meaning, key):
  while key in meaning:
    means = meaning[key]
    if means == key:
      break
    key = means
  return key





def FBA(a, b, Cin):
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, Cin)
  return nor(j, nor(y, Cin)), or_(j, h)


Sum, Cout = FBA('a', 'b', 'Cin')


def make_adder(width):
  sum_bits = []
  Cin = 'Cin'
  for i in range(width):
    machine = {
      'a': 'a' + str(i),
      'b': 'b' + str(i),
      'Cin': Cin,
      }
    sum_bits.append(reify(machine, Sum))
    Cin = reify(machine, Cout)
  return sum_bits, Cin

