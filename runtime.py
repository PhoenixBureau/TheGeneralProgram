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


  ##    and_(letter, choice(alphabet)),


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


A = ascii_lowercase[:10]


program = xor_ring_program(A)
print view_program(program)
m = Machine(A, program)
m.R[A[-1]] = o
n, looped_to, seen = m.find_cycle(noisy=True)


print 'at', n, 'looped to', looped_to
#print '\n'.join(seen)


##for n in range(100):
##  print '%3i' % n, m
##  m.cycle()
