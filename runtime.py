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


for n in range(100):
  print '%3i' % n, m
  m.cycle()


##seen = {str(m)}
##n = 0
##while True:
##  print '%3i' % n, m
##  n += 1
##  m.cycle()
##  s = str(m)
##  if s in seen:
##    print 'looped.'
##    break
##  seen.add(s)
