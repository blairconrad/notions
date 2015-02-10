#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def is_pandigital(s):
    #print '', s
    for c in '123456789':
        if s.find(c) == -1:
            #print '  c', c
            return False
    return True

def front_fib():
    yield 1
    yield 1
    yield 2
    i = 0
    priors = [1,2]
    while True:
        priors[i] = sum(priors)
        if priors[0] >= 10**20 and priors[1] >= 10**20:
            priors[0] /= 10
            priors[1] /= 10
        result = priors[i]
        i = 1 - i
        yield result

def back_fib():
    yield 1
    yield 1
    yield 2
    i = 0
    priors = [1,2]
    while True:
        result = priors[i] = sum(priors) % 10**10
        i = 1 - i
        yield result

def solve(n):
    i = 0
    ff = front_fib()
    fb = back_fib()
    while True:
        i += 1
        fn = str(ff.next())[:9]
        bn = str(fb.next())[-9:]
        if is_pandigital(fn) or is_pandigital(bn):
            if is_pandigital(fn) and is_pandigital(bn):
                return i

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 329468 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

