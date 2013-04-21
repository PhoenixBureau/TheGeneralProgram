#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint as p_
from random import choice, random, shuffle, sample
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

  def reset(self):
    self.R = dict.fromkeys(self.R.keys(), ((),))
    self.score = 0
    self.seen.clear()

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

  def __repr__(self):
    return '<LM at %i: %s>' % (self.score, view_register(self.R))


class Repro(object):

  def __init__(self):
    self.prob = 0.5

  def hmm(self):
    self.prob = max((self.prob - 0.001, 0.01))
    return self.prob < random()

  def reproduce(self, one, mate):
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


def cyc(pop):
  for lm in pop[:]:
    try:
      lm.next()
    except StopIteration:
      pop.remove(lm)


def cyc2(pop):
  for lm in pop[:]:
    lm.reset()
    for _ in lm:
      pass
    if lm.score < 1:
      pop.remove(lm)


def repopulate(N, pop, selection):
  if len(pop) < N:
    p = sorted(pop, reverse=True, key=selection)
    p = p[:N - len(pop)]
    for parent in p:
      pop.append(reproduce(parent, choice(pop)))


if __name__ == '__main__':

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
  print 'done.'

  Gens = 0
  while max(lm.score for lm in population) < 1024:

    population.sort(key=lambda lm: lm.score)
    del population[:M / 4]
#    winners = population[M / 4:]

    while len(population) < M:
      population.sort(key=lambda lm: lm.score)
      winners = population[M / 4:]

      # And a sport for luck.
      winners.append(LilMachine(K, **dict(generate_program(5, K))))

      for p in winners:
        k = reproduce(p, choice(population))
        for _ in k: pass
        if k.score > p.score:
          population.append(k)

    print Gens, max(lm.score for lm in population)
    Gens += 1

