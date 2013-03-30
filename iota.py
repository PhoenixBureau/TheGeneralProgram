
S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
O = lambda c: c(S)(K)

# xSK  ->  x(S)(K)
#
# "[F]"  "the meaning of the expression F"
#
#  F -> I        lambda x: x(S)(K)
#  F -> *FF      [F][F]
#
# i, *ii, *i*ii, **ii*ii
# 0  100  10100  1100100  Iota is the encoding.
#
##  (let iota ()
##    (if (eq? #\* (read-char)) ((iota)(iota))
##        (lambda (c) ((c (lambda (x) (lambda (y) (lambda (z) ((x z)(y z))))))
##                     (lambda (x) (lambda (y) x))))))
##


I = O(O)

# K = *i*i*ii = 1010100
#
print K is O(O(O(O)))

# S = *i*i*i*ii = 101010100
print S is O(O(O(O(O))))


# All of these return O itself.
print O is O
print O is O(O)(O)

print O is O(   O     )  ( O(O)(O) )
print O is O( O(O)(O) )  (   O     )
print O is O( O(O)(O) )  ( O(O)(O) )


def _decode(path):
  if next(path) == '0':
    return O, path
  A, path = _decode(path)
  B, path = _decode(path)
  return A(B), path

_decode('1010100')
