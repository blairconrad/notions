#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def bstr(n):
    if n == 0:
        return '0'
    s = ''
    while n > 0:
        s += str(n % 2)
        n /= 2
    return s[::-1]


def solve(n):
    s = 0
    for i in range(1,n):
        if str(i) == str(i)[::-1]:
            bin = bstr(i)
            if bin == bin[::-1]:
                s += i
    return s

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 872187 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

