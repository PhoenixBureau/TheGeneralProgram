from by import decode, decode_breadth, _s

for path in open('paths.txt'):
  f0 = decode(path)
  f1 = decode_breadth(path)
  if f0 == f1:
    print _s(f0, True)
  else:
    print _s(f0, True), '---', _s(f1, True)

# xSK  ->  x(S)(K)

# "[F]"  "the meaning of the expression F"

#  F -> I        lambda x: x(S)(K)
#  F -> *FF      [F][F]

# i, *ii, *i*ii, **ii*ii
# 0  100  10100  1100100  Iota is the encoding.

##  (let iota ()
##    (if (eq? #\* (read-char)) ((iota)(iota))
##        (lambda (c) ((c (lambda (x) (lambda (y) (lambda (z) ((x z)(y z))))))
##                     (lambda (x) (lambda (y) x))))))
##


iota = lambda bit: (
  iota(bit)(iota(bit)) if next(bit) == '*' else (
    lambda c: c(lambda x: lambda y: lambda z: x(z)(y(z)))
    (lambda x: lambda y: x)))


print iota(iter('*ii'))(23)
