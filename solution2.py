#-*- coding:utf-8 -*-
import re
from operator import truediv

def solution(s):
    s = re.sub(r'([+/*]|(?<![-])[-]|[()])', r' \1 ', s)
    # print 'solution2:', s
    # s = re.sub(r'([-]?\d+(.\d+)?\s+[+/*]\s+[-]?\d+(.\d+)?)', r'( \1 )', s)
    # print 'solution2:', s

    O, N = list(), list()
    for c in s.split():
        if c == '(':
            O.append(c)
        elif c in ')':
            if len(N) < 2: continue
            op = O.pop()
            while op != '(':
                b, a = N.pop(), N.pop()
                if op == '/':
                    e = truediv(float(a), float(b))
                else:
                    e = eval('%(a)s %(c)s %(b)s'%{'a':a, 'b':b, 'c':op},
                            {'__builtins__': None})
                N.append(e)
                op = O.pop()
        elif c in '+-*/':
            O.append(c)
        else:
            N.append(c)

    return N[0]

if __name__ == '__main__':
    print solution('( 1 + ( ( 2 + 3 ) * ( 4 * 500 ) ) )')
    # 10001
    print solution('((1+2)*2)')
    # 6
    print solution('((2+2))')
    # 4
    print solution('((2--2))')
    # 4
    print solution('((1+2+3+4+5+6+7+8+9+10)*2)')
    # 110
    print solution('(1.5*4)')
    # 6.0
    print solution('((1+2)/2)')
    # 1.5
    print solution('(((1+2)+3+4+(5+6+7)+(8+9+10)*3)/2*5)')
    # 272.5
