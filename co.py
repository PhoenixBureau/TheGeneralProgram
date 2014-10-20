from egg import s
from perv import pervade


def bits_of(i, width):
  return [bool(i & 2**n) for n in range(width)]


def labels(tag, width):
  return [tag + str(n) for n in range(width)]


def claws(tags, n, width):
  '''
  Return a LoF form that is () iff the tagged signals "mean" n.

  I.e. claws('a', 3) -> ( (a0) (a1) a2 )

  Where a0 is the least significant bit of n, etc., and 1:() 0: (()).

  '''
  bits = zip(tags, bits_of(n, width))
  return tuple(
    (name,) if value else name
    for name, value in bits
    )


def comparison_clauses(bit_width, left, right):
  A, B = [], []
  for a in range(2**bit_width):
    for b in range(2**bit_width):
      if a == b:
        continue
      e = claws(left, a, bit_width) + claws(right, b, bit_width)
      if a > b:
        A.append(e)
      else: # a < b
        B.append(e)
  A = tuple(A),
  B = tuple(B),
  return A, B


def gen_m(A, B, bits):
  for a in range(2**bits):
    for b in range(2**bits):
      m = set()
      for bit in range(bits):
        N = 2**bit
        if a & N:
          m.add(A + str(bit))
        if b & N:
          m.add(B + str(bit))
      yield a, b, m


def _bits_in(i):
  return (
    bool(i & 2**n)
    for n in reversed(range(len(bin(i)) - 2))
    )


def z(a, b):
  for ga, gb in zip(_bits_in(a), _bits_in(b)):
    r = set()
    if ga: r.add('a0')
    if gb: r.add('b0')
    yield r


def co(bits, left, right, lo, hi):
  assert (len(left) ==
          len(right) ==
          len(lo) ==
          len(hi) ==
          bits
          )
  A, B = comparison_clauses(bits, left, right)
  P = {}
  for a, b, L, H in zip(left, right, lo, hi):
    P[L] = (((A,), b), (A, a))
    P[H] = (((B,), b), (B, a))
  return P


def latching_co(bits, left, right, lo, hi,
                low_latch, high_latch, reset):
  assert (len(left) ==
          len(right) ==
          len(lo) ==
          len(hi) ==
          bits
          )

  # The base comparisons..
  A, B = comparison_clauses(bits, left, right)

  # Modified such that the first to trip inhibits the other.
  Al = ((A,), low_latch)
  Bl = ((B,), high_latch)

  # Then latched into the external signals (to carry over the state from
  # cycle to cycle.)
  AA = ((high_latch, Al), reset)
  BB = ((low_latch, Bl), reset)

  P = {high_latch: AA, low_latch: BB}

  for a, b, L, H in zip(left, right, lo, hi):
    P[L] = (((AA,), b), (AA, a))
    P[H] = (((BB,), b), (BB, a))
  return P


if __name__ == '__main__':
  from sortingnetwork import solve, cycle

  bits = 2

  A = labels('a', bits)
  B = labels('b', bits)
  H = labels('H', bits)
  L = labels('L', bits)

  # Show off simple sortnet (no latching.)

  P = co(bits, A, B, L, H)

  for a, b, m in gen_m('a', 'b', bits):
    k = cycle(m, P)
    h = ('H2' in k) * 4 + ('H1' in k) * 2 + ('H0' in k) 
    l = ('L2' in k) * 4 + ('L1' in k) * 2 + ('L0' in k) 
    print '%s %s -> (%s <= %s) -> %s' % (a, b, l, h, h >= l)

##  for name, clause in P.items():
##    a = len(s(clause))
##    b = len(s(pervade(clause)))
##    print name, a, b, a - b
##    print

  print ; print

  # Show off latching sortnet.

  P = latching_co(bits, A, B, L, H, 'lo', 'hi', 'reset')

  D = set()
  for i, m in enumerate(z(

    0b1111000001000,
    0b1111001000000,

    )):

    print m, '->',

    if i == 7:
      D.add('reset')
    elif i == 8:
      D.remove('reset')

    m = m | D # Carry over the signals in D from previous cycle.

    D = cycle(m, P)

    print D

    D = D - {"a0", "b0"} # clear out the previous digits.
