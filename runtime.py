from functools import wraps
from random import choice
from string import ascii_lowercase
from egg import xor, and_, and_
from machine import Machine, _, o, view_program


def generate_program(alphabet, per_bit):
  return {
    letter: per_bit(i, letter, alphabet)
    for i, letter in enumerate(alphabet)
    }


def enprogramate(per_bit): # Brutal decorator abuse ensues.
  @wraps(per_bit)
  def gen_prog(alphabet):
    return generate_program(alphabet, per_bit)
  return gen_prog


@enprogramate
def xor_ring_program(i, letter, alphabet):
  '''
  A simple program that XORs a bit with its next neighbor.
  Circular.  Makes Sierpinsk Gasket.  (Try with alphabets
  with various lengths, i.e. not powers of two.)
  '''
  return xor(letter, alphabet[(i + 1) % len(alphabet)])


@enprogramate
def and_rand_program(i, letter, alphabet):
  return and_(letter, choice(alphabet)),


# Run the xor ring pattern in the top N bits.
N = 16
A = ascii_lowercase[:N]
program = xor_ring_program(A)


# bit x is the AND of the lower three xor ring bits.
program['x'] = and_(*A[N - 3:N])


print view_program(program)


# Build a machine with all the bits..
m = Machine(ascii_lowercase, program)


# Initialize the lowest bit in the xor ring.
m.R[A[-1]] = o


# Find (visibly) the cycle.
n, looped_to, seen = m.find_cycle(noisy=True)


print 'at', n, 'looped to', looped_to
#print '\n'.join(seen)


##for n in range(100):
##  print '%3i' % n, m
##  m.cycle()
