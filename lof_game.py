#!/usr/bin/env python
from ebtoo import encode, decode, map_it, decode_tree

def a_mark(value):
  if value == ():
    return 0, None
  return 1, have_contents

def have_contents(value):
  if value == ((),):
    return 0, None
  return 1, single_empty_mark

def single_empty_mark(value):
  if value == (((),),):
    return 0, None
  return 1, are_A_and_B_different

def are_A_and_B_different(value):
  print
  print '(A(B)) ->', value
  A, B = value[0], value[1:]
  print 'A ->', A
  print 'B ->', B
  if A == B:
    return 0, lambda value: encode(a_mark, A)
  return 1, now_what(A, B)

def now_what(A, B):
  print 'now_what', A, B
  if A < B:
    return lambda value: (0, breadth_first(A, B))
  return lambda value: (1, depth_first(A, B))

def breadth_first(A, B):
  print 'breadth_first', A, B
  return lambda value: (0, None)

def depth_first(A, B):
  print 'depth_first', A, B
  return lambda value: (0, None)

if __name__ == '__main__':
  for form in (
    (),
    ((),),
    (((),),),
    ((), (),),
    ):
    print form, '->', encode(a_mark, form)
    print '_' * 70

