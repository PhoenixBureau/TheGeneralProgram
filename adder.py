from itertools import imap

mark = lambda form: not form or not any(imap(mark, form))

nor = lambda *bits: bits
or_ = lambda *bits: nor(bits)
and_ = lambda *bits: tuple(nor(bit) for bit in bits)
nand = lambda *bits: nor(tuple((nor(bit) for bit in bits)))
xor = lambda *bits: nor(and_(*bits), nor(*bits))



if __name__ == '__main__':

  s = lambda term: str(term).replace("'", '').replace(" ", '').replace(",", '')

  a, b = 'ab'

  # Full Bit Adder
  # ((((((a)(b))(ab)))(Cin))((((a)(b))(ab))Cin)) : Sum
  # (((((((a)(b))(ab)))(Cin))((a)(b)))) : Cout

  def FBA1(a, b, Cin):
    '''Full Bit Adder.'''
    k = xor(a, b)
    return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


  def FBA(a, b, Cin):
    '''Full Bit Adder, factored.'''
    h = and_(a, b)
    y = nor(h, nor(a, b))
    j = and_(y, Cin)
    return nor(j, nor(y, Cin)), or_(j, h)


  Sum, Cout = FBA(a, b, 'Cin')
  print
  print 'Full-Bit Adder:'
  print 'Sum:', s(Sum)
  print 'Carry:', s(Cout)
  print


  print ' a  b Cin  Sum Cout'
  B = (), ((),)
  for a in B:
    for b in B:
      for Cin in B:
        Sum, Cout = FBA(a, b, Cin)
        print map(lambda n: int(bool(n)), (a, b, Cin)), '->',
        print int(not mark(Sum)), int(not mark(Cout))

  print; print

  N = lambda bits: sum(2**n for n, bit in enumerate(bits) if bool(bit))

  print 'a   b  Cin sum carry'
  for a1 in B:
    for b1 in B:
      for Cin in B:
        for a0 in B:
          for b0 in B:
            Sum0, Cout0 = FBA(a0, b0, Cin)
            Sum1, Cout1 = FBA(a1, b1, Cout0)

            print N((b0, b1)), '+', N((a0, a1)), '+', int(not mark(Cin)),
            print'=', N((int(not mark(Sum0)), int(not mark(Sum1)))), '+', 4 * int(not mark(Cout1))

##            print map(lambda n: int(bool(n)), (a0, b0, Cin, a1, b1)), '->',
####            print int(not mark(Sum0)), int(not mark(Sum1)), int(not mark(Cout0)), int(not mark(Cout1))
##            print int(not mark(Sum0)), int(not mark(Sum1)), int(not mark(Cout1))
##            print
