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


  print 'nor a, b ->', s(nor(a, b))
  print 'or a, b ->', s(or_(a, b))
  print 'and a, b ->', s(and_(a, b))
  print 'nand a, b ->', s(nand(a, b))
  print 'xor a, b ->', s(xor(a, b))



  # Half-Bit Adder: (((a)(b))(ab)):sum, ((a)(b)):carry
  print
  print 'Half-Bit Adder:'
  print 'Sum:', s(xor(a, b))
  print 'Carry:', s(and_(a, b))


  # Full Bit Adder
  # ((((((a)(b))(ab)))(Cin))((((a)(b))(ab))Cin)) : Sum
  # (((((((a)(b))(ab)))(Cin))((a)(b)))) : Cout

  def FBA(a, b, Cin):
    '''Full Bit Adder.'''
    k = xor(a, b)
    return xor(k, Cin), or_(and_(k, Cin), and_(a, b))


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


# Making a "wider" adder circuit is trivial:
#
  Sum0, Cout0 = FBA('a0', 'b0', 'Cin')
  Sum1, Cout1 = FBA('a1', 'b1', Cout0)
  Sum2, Cout2 = FBA('a2', 'b2', Cout1)
  Sum3, Cout3 = FBA('a3', 'b3', Cout2)


