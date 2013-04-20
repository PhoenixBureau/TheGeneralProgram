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
    self.generation = 0
    self.seen = {}
    self._note()

  def _note(self):
    r = view_register(self.R)
    if r in self.seen:
      return False
    self.seen[r] = self.generation
    self.generation += 1
    return True

  def reproduce(self, mate):
    kid_p = []
    kid_p.extend(self.P.items())
    kid_p.extend(mate.P.items())
    shuffle(kid_p)
    kid_p = dict(kid_p)
    # Mutation
    if self.P == mate.P or random() < 0.01:
      k, expression = next(generate_program(1, self.R.keys()))
      kid_p[k] = expression
    return LilMachine(self.R.keys(), **kid_p)

  def __iter__(self):
    return self

  def next(self):
    cycle(self.R, self.P)
    if not self._note():
      raise StopIteration
    return view_register(self.R)

  def __repr__(self):
    return '<LM at %i: %s>' % (self.generation - 1, view_register(self.R))


def generate_program(N, alphabet):
  for _ in range(N):
    op = choice(ops)
    args = sample(alphabet, choice((1, 2, 3)))
    yield choice(alphabet), Reduce(op(*args))


def cyc(pop):
  for lm in pop[:]:
    try:
      v = lm.next()
    except StopIteration:
      pop.remove(lm)


def repopulate(N, pop, selection):
  if len(pop) < N:
    p = sorted(pop, reverse=True, key=selection)
    p = p[:N - len(pop)]
    for parent in p:
      pop.append(parent.reproduce(choice(pop)))


if __name__ == '__main__':
  target_generations_number = 768

  N, M = 10, 200
  K = list(ascii_lowercase[:N])
  P = (dict(generate_program(5, K)) for _ in range(M))
  population = [LilMachine(K, **program) for program in P]

  Gens = 0
  while max(lm.generation for lm in population) < target_generations_number:

    cyc(population)

    print Gens, '%-5.3g' % (len(population) / float(M)), max(lm.generation for lm in population)
    Gens += 1

    repopulate(M, population, lambda lm: lm.generation)
    # And a sport for luck.
    population.append(LilMachine(K, **dict(generate_program(5, K))))
