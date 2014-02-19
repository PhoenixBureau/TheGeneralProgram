from string import ascii_lowercase as alphabet
from egg import xor, and_, and_
from machine import Machine, _, o, view_program


program = {
  letter: xor(
    letter,
    alphabet[(i + 1) % len(alphabet)],
    )
  for i, letter in enumerate(alphabet)
  }
print view_program(program)


m = Machine(alphabet, program)
m.R['z'] = o


n, looped_to, seen = m.find_cycle(noisy=True)


print 'at', n, 'looped to', looped_to
print '\n'.join(seen)


##for n in range(100):
##  print '%3i' % n, m
##  m.cycle()
