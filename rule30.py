#!/usr/bin/env python
'''
Show off Wolfram's Rule 30 automaton.
'''

def rule30(a, b, c):
  return ((
    ((a,), b,    c  ),
    ( a,  (b,), (c,)),
    ( a,  (b,),  c  ),
    ( a,   b,   (c,)),
    ),)


if __name__ == '__main__':
  from itertools import izip_longest
  from egg import setcycle, _view

  WIDTH = 80
  CYCLES = WIDTH / 2

  P = {
    y: rule30(x, y, z) for x, y, z in zip(
      range(0, WIDTH),
      range(1, WIDTH + 1),
      range(2, WIDTH + 2),
      )
    }


  R = set()
  U = map(str, sorted(P))

  R.add(WIDTH / 2) # Set an initial signal "on".

  # Print column headers, the signal names done vertically.
  for n in map(''.join, izip_longest(*U, fillvalue='|')):
    print n

  for _ in range(CYCLES):
    print _view(R, P)
    R = setcycle(R, P)
  print _view(R, P)


##def ruleN(n):
##  assert 0 <= n < 256, repr(n)
##  for i, pattern in enumerate(PATTERNS):
##    if n & 2**i:
##      rules.append(pattern
##  def rule(a, b, c):
##    return (
##      ()()() -> __
##      ()()__ -> __
##      ()__() -> __
##      ()____ -> __
##      __()() -> __
##      __()__ -> __
##      ____() -> __
##      ______ -> __
##      )
