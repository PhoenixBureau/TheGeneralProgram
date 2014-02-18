from void import pretty, truth_table, reify, void


nor = lambda *bits: bits
or_ = lambda *bits: (bits,)
and_ = lambda *bits: tuple((bit,) for bit in bits)
nand = lambda *bits: (and_(*bits),)
xor = lambda x, y: (((x, (y,)), ((x,), y)),)

ifthen = lambda q, a, b: ((a, (q,)), (q, b))
flipflop = lambda q, r, s: ((s, q), r)


def mem_read(a, b, mem):
  M = dict(a=a, b=b)
  m = reify(mem, M)
  print pretty(m)
  return void(m)

def memory_location(q, bit):
  return flipflop(q, nor(bit), bit)


##wxyz = (a, b), (a, (b,)), ((a,), b), ((a,), (b,))
##ab = ((y, z),), ((x, z),)


a, b, c = 'abc'
w, x, y, z = 'wxyz'


mem_read((), (), xor(a, b))

##for form in (
##  nor(a, b, c),
##  or_(a, b, c),
##  and_(a, b, c),
##  nand(a, b, c),
##  xor(a, b),
##  ifthen(c, a, b),
##  flipflop(a, b, c),
##  ):
##  print pretty(form) ; print
##  truth_table(form) ; print ; print
