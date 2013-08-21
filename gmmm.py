#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint as p_
from random import choice, random, shuffle, sample
from heapq import heapify, heappush
from egg import *
import sys
sys.setrecursionlimit(200)


ops = and_, or_, nand, nor, xor


class LilMachine(object):

  def __init__(self, alphabet, **initial_program):
    self.R = dict.fromkeys(alphabet, ((),))
    self.P = initial_program
    self.score = 0
    self.last = 0
    self.seen = set()
    self._note()

  def val(self):
     return sum(
      2**i * (not self.R[bit])
      for i, bit in enumerate(sorted(self.R))
      )

  def _note(self):
    value = self.val()
    self.score += (value - self.last) == 1
    self.last = value
    return value

  def __iter__(self):
    return self

  def next(self):
    cycle(self.R, self.P)
    value = self._note()
    if value in self.seen:
      raise StopIteration
    self.seen.add(value)
    return value

  def __cmp__(self, other):
    return cmp(self.score, other.score)

  def __repr__(self):
    return '<LM at %i: %s>' % (self.score, view_register(self.R))


def reproduce(one, mate):
  kid_p = []
  kid_p.extend(one.P.items())
  kid_p.extend(mate.P.items())
  shuffle(kid_p)
  kid_p = dict(kid_p)
  alphabet = one.R.keys()
  # Mutation
  if one.P == mate.P or random() < 0.01:
    k, expression = next(generate_program(1, alphabet))
    kid_p[k] = expression
  return LilMachine(alphabet, **kid_p)


def generate_program(N, alphabet):
  for _ in range(N):
    op = choice(ops)
    args = sample(alphabet, choice((1, 2, 3)))
    yield choice(alphabet), Reduce(op(*args))


if __name__ == '__main__':
  _f = sys.stdout.flush

  N, M = 10, 200
  K = list(ascii_lowercase[:N])

  population = []

  print 'Generating population...'
  while len(population) < M:
    lm = LilMachine(K, **dict(generate_program(5, K)))
    for _ in lm:
      pass
    if lm.score:
      population.append(lm)
      print '.',
      _f()
  print 'done.'
  k = [lm.score for lm in population]
  m = max(k)
  av = sum(k) / float(M)
  print 'max: %i  min: %i  average: %4g' % (m, min(k), av)

  population.sort()

  def cyc():
##    av = sum(lm.score for lm in population) / float(M)
    m = max(lm.score for lm in population)
    population.pop(0)
    while True:
      x = reproduce(
        choice(population),
        LilMachine(K, **dict(generate_program(5, K)))
        )
      for v in x:
        pass
      if x.score >= m:
        print x, x.score
        heappush(population, x)
        break

  av = sum(lm.score for lm in population) / float(M)
  while av < 12:
    cyc()
    av = sum(lm.score for lm in population) / float(M)
    print av, max(lm.score for lm in population)
    _f()

##  sort_key = lambda lm: lm.score

#  population.sort()#key=sort_key)
##  Gens = 0

#  while m < 100:
##    del population[:M / 4]
##  winners = population[M / 4:]
##  for w in winners:
##    print w
##
##    while len(population) < M:
##      population.sort(key=lambda lm: lm.score)
##      winners = population[M / 4:]
##
##      # And a sport for luck.
##      winners.append(LilMachine(K, **dict(generate_program(5, K))))
##
##      for p in winners:
##        k = reproduce(p, choice(population))
##        for _ in k: pass
##        if k.score > p.score:
##          population.append(k)
##
##    print Gens, max(lm.score for lm in population)
##    Gens += 1

