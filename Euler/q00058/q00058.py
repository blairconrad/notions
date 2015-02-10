#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def sw(i):
    return i*i  - i  + 1

def nw(i):
    return i*i - 2 * i + 2

def ne(i):
    return i*i - 3 * i + 3

def solve():
    g = shared.PrimeGenerator()
    num_primes = 0
    i = 3
    while True:
        for n in (ne(i), nw(i), sw(i)):
            #print n, g.is_prime(n)
            if g.is_prime(n):
                num_primes += 10
        if num_primes < 2 * i - 1:
            return i
        i += 2


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 26241 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

