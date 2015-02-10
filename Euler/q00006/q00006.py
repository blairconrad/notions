#!/usr/bin/env python

import sys

def solve(n):
    sum_of_squares = sum(i*i for i in xrange(1,n+1))
    the_sum = sum(xrange(1,n+1))
    return the_sum*the_sum - sum_of_squares
                  
              

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 100
    else:
        n = int(args[0])

    assert 25164150 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

