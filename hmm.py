from random import choice
from lof import I, T
from by import encode, decode, _s


def wrappy(*forms):
  return forms


ops = T, wrappy


def gen(form=None):
  if form is None:
    form = I()
  return choice(ops)(form)


seen = set([()])
while len(seen) < 30:
  for form in seen.copy():
    form = gen(form)
    if form in seen:
      continue
    seen.add(form)

for form in sorted(seen):
  print _s(form, True), '->', encode(*form)
