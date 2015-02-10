#!/usr/bin/env python

import sys

def solve(n):
    number = 2**n
    return sum((int(c) for c in str(number)))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    assert 1366 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

