#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import bisect

def sort_digits(n):
    digits = []
    while n > 0:
        n, r = divmod(n, 10)
        bisect.insort(digits, r)
    return digits

def solve():
    # if i has same digits of 3 * i, then i is divisible by 3. Could cap top 2 digits to be 16 or below, but
    # it runs fast  enough for now
    i = 3 
    while True:
        di = sort_digits(i)
        if di == sort_digits(6*i) == sort_digits(2 * i) == sort_digits(3*i) == sort_digits(4*i) == sort_digits(5*i):
                return i
        i += 3

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 142857 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

