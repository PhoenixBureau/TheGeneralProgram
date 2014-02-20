from random import choice
from string import ascii_lowercase
from egg import xor, and_, and_
from machine import Machine, _, o, view_program


def generate_program(alphabet, per_bit):
  return {
    letter: per_bit(i, letter, alphabet)
    for i, letter in enumerate(alphabet)
    }


def generate_xor_ring_program(alphabet):
  '''
  A simple program that XORs a bit with its next neighbor.
  
  '''
  def per_bit(i, letter, A):
    return xor(letter, A[(i + 1) % len(A)])
  return generate_program(alphabet, per_bit)

  ##    and_(letter, choice(alphabet)),


A = ascii_lowercase[:8]
program = generate_xor_ring_program(A)
print view_program(program)


m = Machine(A, program)
m.R[A[-1]] = o


n, looped_to, seen = m.find_cycle(noisy=True)


print 'at', n, 'looped to', looped_to
#print '\n'.join(seen)


##for n in range(100):
##  print '%3i' % n, m
##  m.cycle()
