from egg import nor, and_, or_, all_meanings, reify, reduce_, s


intify = lambda n: int(bool(n))


def FBA(a, b, Cin):
  h = and_(a, b)
  y = nor(h, nor(a, b))
  j = and_(y, Cin)
  return nor(j, nor(y, Cin)), or_(j, h)


fba = FBA('a0', 'b0', 'Cin')


print 'Full-Bit Adder works.'
print s(fba)
print

for meaning in all_meanings(fba):
  Sum, Cout = reify(meaning, fba)
  print '%i + %i + %i = %i %i' % tuple(map(intify, (
    meaning['a0'],
    meaning['b0'],
    meaning['Cin'],
    reduce_(Sum),
    reduce_(Cout),
    )))
print

sum0, cout = fba
sum1, cout = FBA('a1', 'b1', cout)

adder = sum0, sum1, cout
for meaning in all_meanings(adder):
  o0, o1, co = reify(meaning, adder)
  m = dict((k, intify(v)) for k, v in meaning.iteritems())
  s = '%(a1)s%(a0)s + %(b1)s%(b0)s + %(Cin)s' % m
  print s, '=', ('%i%i + %i' % tuple(
    intify(reduce_(form))
    for form in (o1, o0, co)
    ))
