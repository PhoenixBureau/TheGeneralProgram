Python 2.7.3 (default, Aug  1 2012, 05:14:39) 
[GCC 4.6.3] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> ================================ RESTART ================================
>>> 
aa = reify(P, a)
>>> a
((('a',), ('z',)), ('a', 'z'))
>>> aa = reify(P, a)
>>> aa
((('a',), ('z',)), ('a', 'z'))
>>> 
>>> aa = reify({'a': 'hmm'}, a)
>>> aa
((('hmm',), ('z',)), ('hmm', 'z'))
>>> aa = reify({'a': aa}, a)
>>> aa
(((((('hmm',), ('z',)), ('hmm', 'z')),), ('z',)), (((('hmm',), ('z',)), ('hmm', 'z')), 'z'))
>>> s(aa)
'((((((hmm)(z))(hmm z)))(z))((((hmm)(z))(hmm z))z))'
>>> aa = Reduce(aa)
>>> aa
(((('hmm',), ('z',)), ('hmm', 'z'), ('z',)), (((('hmm',), ('z',)), ('hmm', 'z')), 'z'))
>>> s(aa)
'((((hmm)(z))(hmm z)(z))((((hmm)(z))(hmm z))z))'
>>> aa = reify({'hmm': 'a'}, aa)
>>> aa
(((('a',), ('z',)), ('a', 'z'), ('z',)), (((('a',), ('z',)), ('a', 'z')), 'z'))
>>> s(aa)
'((((a)(z))(a z)(z))((((a)(z))(a z))z))'
>>> s(reify({'a': ((),)}, aa))
'((((\xe2\x97\x8e)(z))(\xe2\x97\x8ez)(z))((((\xe2\x97\x8e)(z))(\xe2\x97\x8ez))z))'
>>> print s(reify({'a': ((),)}, aa))
((((◎)(z))(◎z)(z))((((◎)(z))(◎z))z))
>>> a0 = reify({'a': ((),)}, aa)
>>> print s(a0)
((((◎)(z))(◎z)(z))((((◎)(z))(◎z))z))
>>> a0 = Reduce(a0)
>>> print s(a0)
(((z)(z))(z z))
>>> a1 = reify({'a': ()}, aa)
>>> print s(a1)
(((◎(z))(○z)(z))(((◎(z))(○z))z))
>>> a1 = Reduce(a1)
>>> print s(a1)
((z(z))((z)z))
>>> '(z(z))'
'(z(z))'
>>> ()'(z(z))'
