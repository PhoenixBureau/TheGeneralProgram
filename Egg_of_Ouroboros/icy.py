import unittest


class K(frozenset):

  def __str__(self):
    return '(%s)' % ' '.join(sorted(map(str, self)))

  __repr__ = __str__


Mark = K()
Void = K({Mark})


nor = lambda *bits: K(bits)
or_ = lambda *bits: K((K(bits),))
and_ = lambda *bits: K(nor(bit) for bit in bits)
nand = lambda *bits: nor(and_(*bits))
xor = lambda *bits: nor(nor(*bits), and_(*bits))
nxor = lambda *bits: nor(xor(*bits))


def unwrap(form):
  if not isinstance(form, K) or not form or form == Void:
    return form

  f = set()
  for i in form:
    u_(f, unwrap(i))

  if len(f) == 1:
    inner, = f
    if isinstance(inner, K) and len(inner) == 1:
      # {(foo)}
      inner, = inner
      return inner

  return Void if Mark in f else K(f)


def u_(f, form):
  if not isinstance(form, K):
    f.add(form)
    return

  if len(form) == 1:
    inner, = form
    if isinstance(inner, K):
      for term in inner:
        u_(f, term)
    else:
      f.add(form)

  elif form != Void:
    f.add(form)


def clean(form, exclude=None):
  '''
  Given a form and a set of terms that are to be pervaded (excluded)
  from the form, return the result of Pervasion.  Note that this function
  will also collect and pervade literals as it goes along.
  '''
  if not isinstance(form, K) or form == Mark or form == Void:
    return form

  if exclude is None:
    exclude = set()

  new_stuff = form - exclude
  exclude = exclude | new_stuff

  f = set()
  for i in new_stuff:
    if not isinstance(i, K):
      f.add(i)
      continue

    e = clean(i, exclude)

    if e == Mark:
      return Void
    if e != Void:
      f.add(e)

  return K(f)


def reify(meaning, form):
  if not isinstance(form, K):
    return meaning.get(form, form)
  return K(reify(meaning, inner) for inner in form)


def standard_form(x, form):
  '''
  Return the "Standard Form" of form in the variable x.
  '''
  # Inefficient.  Builds up structure to throw it away.
  Ex = reify({x: Void}, form) # Replace x with Void.
  E_x_ = reify({x: Mark}, form) # Replace x with Mark.
  E = nor(nor(x, Ex), nor(nor(x), E_x_))
  return unwrap(E)


class CleaningTest(unittest.TestCase):

  def testB2(self):
    '''
    ((a b) a)
    ((  b) a)
    '''
    a = nor('a', nor('a', 'b'))
    b = nor('a', nor('b'))
    self.assertEqual(b, clean(a))

  def testCsomething(self):
    '''
    ((a) a)
    (( )  )
    '''
    a = nor('a', nor('a'))
    self.assertEqual(Void, clean(a))

  def testCn(self):
    '''
    ((a) ((a)))
    (( )      )
    '''
    a = nor('a')
    a = nor(a, nor(a))
    self.assertEqual(Void, clean(a))

  def testCsomethingElse(self):
    '''
    (((a) b) a)
    ((( ) b) a)
    ((( )  ) a)
    (        a)
    '''
    b = nor('a')
    a = nor('a', nor('b', b))
    self.assertEqual(b, clean(a))

  def testNoredLeaves(self):
    '''
    ((((((a))))) ((((a)))) (((a))) ((a)) b)
    ((((     ))) ((     )) (     ) ((a)) b)
    (                      (     )        )
    (())
    '''
    a = nor(nor('a'))
    b = 'b'
    x = nor(b, a, nor(a), nor(nor(a)), nor(nor(nor(a))))
    self.assertEqual(Void, clean(x))


class ToughNutTest(unittest.TestCase):

  def testCn(self):
    '''
    ((a) (a  b))
    ((a) (() b))
    ((a) (()  ))
    ((a)       )
      a
    '''
    a = nor('a')
    a = nor(a, nor('a', 'b'))
    e = standard_form('b', a)
    print e
    e = standard_form('a', a)
    print e
    self.assertEqual('a', e)


class UnwrapTest(unittest.TestCase):

  def testMark(self):
    self.assertEqual(Mark, unwrap(Mark))

  def testVoid(self):
    self.assertEqual(Void, unwrap(Void))

  def testLeaf(self):
    self.assertEqual('a', unwrap('a'))

  def testNegatedLeaf(self):
    a = nor('a')
    self.assertEqual(a, unwrap(a))

  def testTriple(self):
    a = nor(Void)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))
    a = nor(a)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))
    a = nor(a)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))
    a = nor(a)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))
    a = nor(a)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))
    a = nor(a)
    self.assertEqual(Mark, unwrap(a))
    a = nor(a)
    self.assertEqual(Void, unwrap(a))

  def testMultiUnwrapLeaf(self):
    A = 'a'
    B = nor(A)
    a = nor(B)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    self.assertEqual(A, unwrap(a))
    b = nor(a)
    self.assertEqual(B, unwrap(b))
    a = nor(b)
    
  def testManyLeaves(self):
    a = nor(nor('a'))
    b = 'b'
    
    x = nor(b, a)
    t = nor('a', b)
    self.assertEqual(t, unwrap(x))
    
    a = nor(a)
    x = nor(b, a)
    t = nor(nor('a'), b)
    self.assertEqual(t, unwrap(x))

    a = nor(a)
    x = nor(b, a)
    t = nor('a', b)
    self.assertEqual(t, unwrap(x))

    a = nor(a)
    x = nor(b, a)
    t = nor(nor('a'), b)
    self.assertEqual(t, unwrap(x))

    a = nor(a)
    x = nor(b, a)
    t = nor('a', b)
    self.assertEqual(t, unwrap(x))
    
  def testNoredLeaves(self):
    '''
    ((((((a))))) ((((a)))) (((a))) ((a)) b)
    ((a) a b)
    '''
    a = nor(nor('a'))
    b = 'b'
    x = nor(b, a, nor(a), nor(nor(a)), nor(nor(nor(a))))
    t = nor('a', b, nor('a'))
    self.assertEqual(t, unwrap(x))

  def testNegatedLeaves(self):
    '''
    (a b)
    '''
    a = nor('a', 'b')
    self.assertEqual(a, unwrap(a))

  def testOrLeaves(self):
    '''
    ((a b))
    '''
    a = or_('a', 'b')
    self.assertEqual(a, unwrap(a))

  def testOrLeaves2(self):
    '''
    ((((((b)) a)) c))
    ((    b   a   c))
    '''
    a = or_('a', or_('b'))
    a = or_(a, 'c')
    t = or_(*'abc')
    self.assertEqual(t, unwrap(a))

  def testFoo(self):
    '''
    ((((a b) (a) a)) (a))
    (  (a b) (a) a   (a))
    (  (a b) (a) a      )
    '''
    a, b, c = map(K, ('a', 'ab', ('a', 'b')))
    k = K(('a', a, b, c))
    x = and_('a', k)
    self.assertEqual(k, unwrap(x))

  def testBar(self):
    '''
    (((((((((a b) (a) a)) (a))))) (((a)))))
    ((((  (((a b) (a) a)) (a)  ))   (a)  ))
    ((((    (a b) (a) a   (a)  ))   (a)  ))
    ((      (a b) (a) a   (a)       (a)  ))
    ((      (a b) (a) a                  ))
    '''
    a, b, c = map(K, ('a', 'ab', ('a', 'b')))
    k = K(('a', a, b, c))
    x = and_('a', k)
    j = nand(nor(a), nor(nor(x)))
    self.assertEqual(nor(k), unwrap(j))

  def testBazA(self):
    '''
    (((a)) (a))
    (  a   (a))
    '''
    a = nor('a')
    k = nor(a, nor(a))
    t = nor(a, 'a')
    self.assertEqual(t, unwrap(k))

  def testBazB(self):
    '''
    ((((a))) (a))
    (  (a)   (a))
    (  (a)      )
        a
    '''
    a = nor('a')
    k = nor(a, nor(nor(a)))
    h = unwrap(k)
    self.assertEqual('a', h)
    
  def testHu(self):
    '''
    ((((())) (()) ()))
    ()
    '''
    x = nor(nor(Mark, Void, nor(Void)))
    self.assertEqual(Mark, unwrap(x))


if __name__ == '__main__':
  unittest.main()


'''


a = nor(nor('a'), nor(*'ab'))
print a
c = each_way(a, 'a')
print c
d = clean(c)
print d


    ((a) (a  b))

E = ( (E x) (E (x)) )


E = ( (((a) (a  b)) a) (((a) (a  b)) (a)) )


























'''