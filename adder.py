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
