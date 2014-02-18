#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from void import pretty, truth_table, value, reify

q, r, s = 'qrs'

form = ((s, q), r)

print pretty(form)
print
truth_table(form)

