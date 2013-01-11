#-*- coding:utf-8 -*-
import re

def solution(s):
    s = re.sub(r'([+/*]|(?<![-])[-]|[()])', r' \1 ', s)
    print 'solution2:', s
    O, N = list(), list()
    for c in s.split():
        if c == '(':
            pass
        elif c in ')':
            if len(N) < 2: continue
            r = '%(a)s %(c)s %(b)s'%{'b':N.pop(), 'a':N.pop(), 'c':O.pop()}
            e = eval(r)
            N.append(e)
        elif c in '+-*/^':
            O.append(c)
        else:
            N.append(c)
    return N[0]

if __name__ == '__main__':
    print solution('( 1 + ( ( 2 + 3 ) * ( 4 * 500 ) ) )')
    print solution('((1+2)*2)')
    print solution('((2+2))')
    print solution('((2--2))')
    print solution('((1+2+3+4+5+6+7+8+9+10)*2)')
