from logpy import run, eq, var
from logpy.core import reify

# The pattern of Distribution: ((p)(q))r <---> ((pr)(qr))

params = p, q, r = tuple(var(name) for name in 'pqr')
collect = ((p,), (q,)), r
distribute = ((p, r), (q, r),),


def transform(form, parameters, from_, to):
  for solution in run(0, parameters, eq(from_, form)):
    yield reify(to, dict(zip(parameters, solution)))


a, b = var('a'), var('b')
left = (((a,),), ((b,),)), b
right = (((a,), b), ((b,), b),),


for it in transform(left, params, collect, distribute):
  print it, it == right


for it in transform(right, params, distribute, collect):
  print it, it == left



c = var('c')
M = a, b, c
N = a, (a, (b,)), c


for it in transform((1, 2, 3), M, M, N):
  print it, it == (1, (1, (2,)), 3)
