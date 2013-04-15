from egg import *


def convert(form):
  if isinstance(form, basestring):
    return form
  return frozenset(convert(inner) for inner in form)


def depth(form):
  if isinstance(form, basestring):
    return 0
  return 1 + (max(depth(inner) for inner in form) if form else 0)


def count(form):
  if isinstance(form, basestring):
    return 0
  return 1 + sum(count(inner) for inner in form)


def sort_key(form):
  return depth(form), count(form)


def normalize(form):
  if isinstance(form, basestring):
    return form
  return tuple(sorted(form, key=sort_key))
