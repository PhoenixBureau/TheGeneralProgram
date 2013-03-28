#!/usr/bin/env python
from ebtoo import encode, decode, map_it, decode_tree


def make_interval_game(n=0, m=10):
  if n == m:
    return
  assert n < m, (n, m)
  midpoint = n + (m - n) / 2

  def encode(value):
    if value > m or value < n:
      raise ValueError(value)
    if value <= midpoint:
      return 1, make_interval_game(n, midpoint)
    return 0, make_interval_game(midpoint + 1, m)

  return encode


if __name__ == '__main__':
  from ebt import decode, O

  for n in range(1, 11):
    print 'for n =', n
    e = make_interval_game(0, n)
    d = O(0, n)
    for i in range(n + 1):
      path = encode(e, i)
      print i, '->', path, '->', decode(d, path)
    print '-' * 70






