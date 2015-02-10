#!/usr/bin/env python

import sys
sys.path.append(r'..')
import shared

def solve(n):
    total = 0
    g = shared.PrimeGenerator()
    p = g.next()
    while p < n:
        total += p
        p = g.next()
    return total
        

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 2000000
    else:
        n = int(args[0])

    assert 142913828922 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

