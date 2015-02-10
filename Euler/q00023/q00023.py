#!/usr/bin/env python

import sys
sys.path.append('..')
import shared

def is_abundant(n):
    return sum(shared.find_divisors(n)[:-1]) > n

def find_abundant():
    return [i for i in xrange(12, 28123) if is_abundant(i)]


def solve(n):
    cannot = {}
    for i in xrange(1, 28124):
        cannot[i] = 0

    ab =  find_abundant()
    for i in range(len(ab)):
        for j in range(i, len(ab)):
            s = ab[i] + ab[j] 
            if s > 28123:
                break
            cannot.pop(s, None)
    return sum(cannot.keys())
        
        



def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    result = solve(n)
    print result
    assert 4179871 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

