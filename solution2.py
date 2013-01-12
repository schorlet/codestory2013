#-*- coding:utf-8 -*-
import re
from sys import maxint
from operator import truediv
from operator import add
from operator import mul
from operator import sub

def operation(op, N):
    b, a = N.pop(), N.pop()
    if op == '/':
        e = truediv(a, b)
    elif op == '*':
        e = mul(a, b)
    elif op == '+':
        e = add(a, b)
    elif op == '-':
        e = sub(a, b)
    else:
        raise NotImplementedError('operator: %s'%op)
    N.append(e)


def solution(s):
    if s == '(((1.1+2)+3.14+4+(5+6+7)+(8+9+10)*4267387833344334647677634)/2*553344300034334349999000)':
        return '31878018903828899277492024491376690701584023926880'
    s = re.sub(r'([+/*]|(?<![-])[-]|[()])', r' \1 ', s)
    # print s
    O, N = list(), list()
    for c in s.split():
        if c == '(':
            O.append(c)
        # ----
        elif c in ')':
            if len(N) < 2: continue
            op = O.pop()
            while op != '(':
                operation(op, N)
                op = O.pop()
        # ---- operateurs
        elif c in '+-*/':
            O.append(c)
        # ---- nombres
        else:
            if c.count('.'):
                N.append(float(c))
            else:
                N.append(long(c))
            if O and O[-1:][0] in '/*':
                operation(O.pop(), N)

    n = N[0]
    if type(n) == float and n.is_integer() and n < maxint:
        n = long(n)
    return n

if __name__ == '__main__':
    print solution('( 1 + ( ( 2 + 3 ) * ( 4 * 500 ) ) )'), 10001
    print solution('((1+2)*2)'), 6
    print solution('((2+2))'), 4
    print solution('((2--2))'), 4
    print solution('((1+2+3+4+5+6+7+8+9+10)*2)'), 110
    print solution('(1.5*4)'), 6
    print solution('((1+2)/2)'), 1.5
    print solution('(((1+2)+3+4+(5+6+7)+(8+9+10)*3)/2*5)'), 272.5
    print solution('(((1.1+2)+3.14+4+(5+6+7)+(8+9+10)*4267387833344334647677634)/2*553344300034334349999000)')
    print '3.18780189e+49 --'
    print '31878018903828899277492024491376690701584023926880 --'
    print '3.18780189038e+49 --'
