#-*- coding:utf-8 -*-
import re
from decimal import *
from operator import truediv
from operator import add
from operator import mul
from operator import sub

def operation(op, N):
    """
    >>> nums = [3, 6]
    >>> operation('/', nums)
    >>> len(nums) == 1
    True
    >>> nums[0]
    0.5
    """
    b, a = N.pop(), N.pop()
    if op == '/':
        e = truediv(a, b)
    elif op == '*':
        e = mul(a, b)
    elif op == '+':
        e = add(b, a)
    elif op == '-':
        e = sub(b, a)
    else:
        raise NotImplementedError('operator: %s'%op)
    N.append(e)

def normalize_fraction(d):
    """http://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal"""
    normalized = d.normalize()
    sign, digits, exponent = normalized.as_tuple()
    if exponent > 0:
        return Decimal((sign, digits + (0,) * exponent, 0))
    else:
        return normalized

def calcul(s):
    """
    >>> calcul('( 1 + ( ( 2 + 3 ) * ( 4 * 500 ) ) )')
    '10001'
    >>> calcul('(10-21)')
    '-11'
    >>> calcul('12*12')
    '144'
    >>> calcul('120/12')
    '10'
    >>> calcul('((1+2)*2)')
    '6'
    >>> calcul('((2+2))')
    '4'
    >>> calcul('((2--2))')
    '4'
    >>> calcul('((1+2+3+4+5+6+7+8+9+10)*2)')
    '110'
    >>> calcul('(1.5*4)')
    '6'
    >>> calcul('((1+2)/2)')
    '1.5'
    >>> calcul('(((1+2)+3+4+(5+6+7)+(8+9+10)*3)/2*5)')
    '272.5'
    >>> calcul('(((1.1+2)+3.14+4+(5+6+7)+(8+9+10)*4267387833344334647677634)/2*553344300034334349999000)')
    '31878018903828899277492024491376690701584023926880'
    >>> calcul('((-1)+(1))')
    '0'
    >>> calcul('((-1.1)+(1.1))')
    '0'
    >>> calcul('((-1.1)+(1))')
    '-0.1'
    >>> calcul('((-1.1)+(1.1))')
    '0'
    >>> calcul('(1.0000000000000000000000000000000000000000000000001*1.0000000000000000000000000000000000000000000000001)')
    '1.00000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000001'
    >>> calcul('((55 - 15 + 3*5)/5)')
    '11'
    """
    s = re.sub(r'([+/*]|(?<![()+/*-])[-]|[()])', r' \1 ', s)
    # decimal precision
    getcontext().prec = 100
    O, N = list(), list()
    for c in s.split():
        if c == '(':
            O.append(c)
        # ----
        elif c in ')':
            if len(N) < 2: continue
            op = O.pop()
            # reverse op and numbers and put them in O2, N2
            # in order to read the expression from left to right
            O2, N2 = list(), list()
            while op != '(':
                O2.append(op)
                N2.append(N.pop())
                op = O.pop()
            N2.append(N.pop())
            while O2:
                op = O2.pop()
                operation(op, N2)
            N.append(N2[0])
        # ---- operateurs
        elif c in '+-*/':
            O.append(c)
        # ---- nombres
        else:
            N.append(Decimal(c))
            if O and O[-1:][0] in '/*':
                operation(O.pop(), N)

    return str(normalize_fraction(N[0]))

if __name__ == '__main__':
    print calcul('((1+2+3+4+5+6+7+8+9+10)*2)')
    print calcul('(1.5*4)')
    print calcul('((1+2)/2)')
    print calcul('(((1+2)+3+4+(5+6+7)+(8+9+10)*3)/2*5)')
