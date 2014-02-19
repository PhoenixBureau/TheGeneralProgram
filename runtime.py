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
m.R['a'] = o
print m
for n in range(100):
  m.cycle()
  print '%3i' % n, m

