from omega import BaseParser
from logpy import run, eq, membero, var, conde


mark = ()

no_mark = ((),)

class LawsOfFormParser(BaseParser):
  __grammar = '''

    spaces = (' ' | '\r' | '\n' | '\t')* -> ' ' ;
    token :t = spaces seq(t) spaces ;

    mark = "()"+ -> "mark" ;
    no_mark = ( "(" LoF ")" )+ -> "no_mark" ;

    LoF = ( mark | no_mark )+:lof -> (lof[0]);

  '''

for form in ('''\

    ()

    ()()

    (())

    (())()

    ((()))

    (()())

    (())(())

    ( () (()()) ) ( ((())) (()) )

    ((())((())))

  '''.splitlines()):
  form = form.strip()
  if form:
    print form, '->', LawsOfFormParser.match(form)



##
##print LawsOfFormParser.match('''
##
##    (()())
##
##  ''')
##
##print LawsOfFormParser.match('''
##
##    ( () (()()) ) ( ((())) (()) )
##
##  ''')
##
####'''
####
####    # Cribbed "spaces" rule from omega.bootstrap.OmegaParser
####    spaces = (' ' | '\r' | '\n' | '\t')* -> ' ' ;
####
####
####    digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ; 
####
####    digits          = digit+:ds -> ("".join(ds));  
####    optional_digits = digit*:ds -> ("".join(ds));  
####
####    number = digits:i '.' optional_digits:f -> (float(i + '.' + f)) |
####                               '.' digits:f -> (float('.' + f)) |
####                                   digits:i -> (int(i)) ;  
####
####
####    char = anything:ch ?('a' <= ch <= 'z') -> (ch) ;
####
####    variable = char+:chs -> (define(''.join(chs))) ;
####
####    group = '(' termite+:T ')' -> (tuple(T)) ;
####
####    termite = ' '* (group | variable | number) ;
####
####
####    EQ = spaces termite:a ' '* "=" termite:b -> ((eq, a, b)) ;
####
####    query =  spaces variable:x ' '* "?" -> (x) ;
####
####    logic = EQ*:eqs query:x spaces -> (run(0, x, *eqs)) ;
####
####    '''
##
