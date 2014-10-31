from pprint import pprint as _p

Domain = ((),), ()

def selector(power_of_two, prefix='sel:'):
  names = [prefix + str(n) for n in range(power_of_two)]
  clauses = [
    tuple(
      names[n] if i & 2**n else (names[n],)
      for n in range(power_of_two)
      )
    for i in range(2**power_of_two)
    ]
  return names, clauses


_p(selector(3))













##def foo(power_of_two, prefix='sel:'):
##  names, clauses = [], []
##  for i in range(2**power_of_two):
##    name = prefix + str(i)
##    names.append(name)
##    e = [
##      Domain[bool(i & 2**n)]
##      for n in range(power_of_two)
##      ]
##    clauses.append(e)
##  return zip(names, clauses)
##
