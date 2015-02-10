#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    g = shared.PrimeGenerator()
    n = 9
    while True:
        if g.is_prime(n):
            n += 2
            continue

        found = False
        t = 1
        square2 = 2 * t * t

        while square2 <= n-3:
            if g.is_prime(n - square2):
                found = True
                break
            t += 1
            square2 = 2 * t * t
        if not found:
            return n
        n += 2
    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 5777 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

