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
encode = lambda *f: '1' + encode(*f[0]) + encode(*f[1:]) if f else '0'


#: Decode paths from encoder.
decode = lambda path: _decode(iter(path))[0]


def _decode(path):
  if next(path) == '0':
    return (), path
  A, path = _decode(path)
  B, path = _decode(path)
  return (A,) + B, path


def _s(shell, do_special=False):
  s = ''.join(map(str, shell)).replace(',', '').replace(' ', '')
  if do_special:
    s = s.replace('(())', '◎').replace('()', '○')
  return s


if __name__ == '__main__':

  a = ()
  b = ((),)
  c = (((),),)
  d = (((),),(), )
  e = ((), ((),))
  FO = (a, b, c, d, e)
  for shell in FO:
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
  for shell in FO:
    shell = (shell,) * 2
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
  for shell in FO:
    shell = (shell,) * 3
    print _s(shell), '->', encode(*shell), '->', _s(*(decode(encode(shell))))
