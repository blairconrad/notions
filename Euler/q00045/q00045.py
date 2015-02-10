#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import bisect

def pent(n):
    return n * ( 3 * n - 1 ) / 2

def hex(n):
    return n*(2*n-1)

def triangle(n):
    return n * ( n + 1 ) / 2

def solve():
    last_triangle = last_pent = last_hex = 40755
    t = 286
    p = 166
    h = 144

    while True:
        last_hex = hex(h)
        h += 1

        while last_pent < last_hex:
            last_pent = pent(p)
            p += 1

        if last_pent == last_hex:
            # don't need triangles - all hexes are triangles
            # I didn't think of this at the time.
            while last_triangle < last_hex:
                last_triangle = triangle(t)
                t += 1

            if last_triangle == last_hex:
                return last_hex

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 1533776805 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

