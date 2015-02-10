#!/usr/bin/env python

import sys
sys.path.append(r'..')
import shared


def solve(n):
    gen = shared.PrimeGenerator()
    while True:
        p = gen.next()
        quot, rem = divmod(n, p)
        if rem == 0:
            if quot == 1:
                return p
            n = quot

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 600851475143
    else:
        n = int(args[0])

    assert 6857 == solve(n)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

