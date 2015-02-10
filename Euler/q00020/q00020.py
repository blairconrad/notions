#!/usr/bin/env python

import sys
sys.path.append('..')
import shared

def solve(n):
    return sum((int(i) for i in str(shared.factorial(n))))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 100
    else:
        n = int(args[0])

    assert 648 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

