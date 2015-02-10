#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def pow(base, exp, modulus):
    result = 1
    if exp > 1:
        k = exp / 2
        m = pow(base, k, modulus)
        result *= m * m
    if exp % 2 == 1:
        result *= base
    return result % modulus


def solve():
    modulus = 10000000000
    return (28433 * pow(2, 7830457, modulus) + 1) % modulus

    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 8739992577 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

