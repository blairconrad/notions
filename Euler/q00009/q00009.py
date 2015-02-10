#!/usr/bin/env python

import sys

def solve(n):
    for c in xrange(3, n+1):
        for b in xrange(2, c):
            a = n - c - b
            if a*a + b*b  == c*c:
                    return a*b*c

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    assert 31875000 == solve(1000)

    return 0


if __name__ == '__main__':
    sys.exit(main())

