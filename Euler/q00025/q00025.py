#!/usr/bin/env python

import sys
sys.path.append('..')
import shared

def solve(n):
    g = shared.FibonacciGenerator()
    index = 1
    for f in g:
        if len(str(f)) >= n:
            return index
        index += 1

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    result = solve(n)
    print result
    assert 4782 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

