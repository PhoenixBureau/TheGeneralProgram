# -*- coding: utf-8 -*-
'''

_ -> 0    "Nothing"
○ -> 100  "I exist but I'm empty and have no friends."

(A)B ->  1AB

◎ -> 1 100 0
○○ -> 1 0 100

◎○ -> 1 100 100
○◎ -> 1 0 11000
◎◎ -> 1 100 11000

'''

#: Depth-first encoding of forms.
encode = lambda f: '1' + encode(f[0]) + encode(f[1:]) if f else '0'


#: Decode paths from encoder.
decode = lambda path: _decode(iter(path))[0]


def _decode(path):
  if next(path) == '0':
    return (), path
  A, path = _decode(path)
  B, path = _decode(path)
  return (A,) + B, path



#: Depth-first encoding of forms.
encode_breadth = lambda f: '1' + encode_breadth(f[1:]) + encode_breadth(f[0]) if f else '0'


#: Decode paths from encoder.
decode_breadth = lambda path: _decode_breadth(iter(path))[0]


def _decode_breadth(path):
  if next(path) == '0':
    return (), path
  B, path = _decode_breadth(path)
  A, path = _decode_breadth(path)
  return (A,) + B, path


def _s(shell, do_special=False):
  s = ''.join(map(str, shell)).replace(',', '').replace(' ', '')
  if do_special:
    s = s.replace('(())', '◎').replace('()', '○')
  return s


def concat(*paths):
  if not paths:
    return '0'
  return ''.join([path[:-1] for path in paths[:-1]] + [paths[-1]])


if __name__ == '__main__':

  a = ()
  b = ((),)
  c = (((),),)
  d = (((),),(), )
  e = ((), ((),))
  FO = (a, b, c, d, e)
  for shell in FO:
    print _s(shell, True), '->', encode(shell), '->', _s(decode_breadth(encode(shell)), True)
  for shell in FO:
    shell = (shell,) * 2
    print _s(shell, True), '->', encode(shell), '->', _s(decode_breadth(encode(shell)), True)
  for shell in FO:
    shell = (shell,) * 3
    print _s(shell, True), '->', encode(shell), '->', _s(decode_breadth(encode(shell)), True)





def foo():
  new_forms = sorted(set(map(decode, forms) + map(decode_breadth, forms)))
