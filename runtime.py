from pprint import pprint as p_
from string import ascii_lowercase as alphabet
from egg import xor
from machine import Machine, _, o


program = {
  letter: xor(
    letter,
    alphabet[(i + 1) % len(alphabet)],
    )
  for i, letter in enumerate(alphabet)
  }
p_(program)
m = Machine(alphabet, program)
m.R['z'] = o
for n in range(100):
  print '%3i' % n, m
  m.cycle()
print m

