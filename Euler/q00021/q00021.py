#!/usr/bin/env python

import sys
sys.path.append('..')
import shared

def amicable(n):
    s = sum(shared.find_divisors(n)[:-1])
    if s == n:
        return None
    if sum(shared.find_divisors(s)[:-1]) == n:
        return n, s
    else:
        return None
            

def solve(n):
    s = 0
    for i in range(2, n):
        a = amicable(i)
        if a:
            s += a[0]
    return s

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 10000
    else:
        n = int(args[0])

    result = solve(n)
    print result
    assert 31626 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

