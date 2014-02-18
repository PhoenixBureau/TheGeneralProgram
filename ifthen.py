#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from void import pretty, truth_table, value, reify


a, b, q = 'abq'


ifthen = lambda a, b, q: ((a, (q,)), (q, b))


form = ifthen(a, b, q)

print pretty(form)
print
truth_table(form)

print
print ; print 'a if q else b'
print ; print 'q ? a : b'
