#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from itertools import product, izip


B = ((),), () # Void ◎ and Mark ○


def void(form):
  return any(not void(i) for i in form)


def value(form):
  return '_' if void(form) else '○'


def reify(form, meaning):
  if isinstance(form, basestring):
    return meaning[form]
  return tuple(reify(inner, meaning) for inner in form)


def symbols_of(form, symbols=None):
  if symbols is None:
    symbols = set()
  if isinstance(form, basestring):
    symbols.add(form)
  else:
    for inner in form:
      symbols_of(inner, symbols)
  return symbols


def all_meanings(symbols):
  b = [B] * len(symbols)
  for values in product(*b):
    yield dict(izip(symbols, values))


def truth_table(form):
  symbols = symbols_of(form)
  print ' '.join(symbols), '| Value'
  print '-' * (2 * len(symbols) + 7)
  for meaning in all_meanings(symbols):
    print ' '.join(value(meaning[sym]) for sym in symbols),
    print '|', value(reify(form, meaning))


def pretty(form):
  return(str(form)
         .replace(' ', '')
         .replace("','", ' ')
         .replace("'", '')
         .replace(',', '')
         .replace('(())', '◎')
         .replace('()', '○')
         )


if __name__ == '__main__':
  for form in (
    ('a', 'b'), # nor
    (('a', 'b'),), # or
    (('a',), ('b',)), # and
    ((('a',), ('b',)),), # nand
    ((('a',), ('b',)), ('a', 'b')) # xor
    ):
    print pretty(form) ; print
    truth_table(form)
    print ; print ; print
