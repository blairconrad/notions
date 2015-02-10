#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve():
    result = 1
    frac = ' '
    next_number = 1
    next_digit = 1
    while next_digit <= 1000000:
        while len(frac) <= next_digit:
            frac += str(next_number) 
            next_number += 1
        result *= int(frac[next_digit], 10)
        next_digit *= 10
    return result


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 210 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

