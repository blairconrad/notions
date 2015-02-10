#!/usr/bin/env python

import sys
sys.path.append(r'..')
import shared

def solve(n):
    g = shared.PrimeGenerator()
    for i in xrange(n):
        p = g.next()
    return p

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 10001
    else:
        n = int(args[0])

    assert 104743 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

