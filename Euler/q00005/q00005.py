#!/usr/bin/env python

import sys
import collections
import datetime
sys.path.append(r'..')
import shared


def find_prime_factors(n):
    factors = {}
    count = 0
    g = shared.PrimeGenerator()

    p = g.next()
    while True:
        if n == 1:
            if count > 0:
                factors[p] = count
            return factors
        quot, rem = divmod(n,p)
        if rem == 0:
            n = quot
            count += 1
        else:
            if count > 0:
                factors[p] = count
                count = 0
            p = g.next()

def solve(n):
    all_factors = collections.defaultdict(lambda: 0)
    for f in range(2, n+1):
        f_factors = find_prime_factors(f)
        for k, v in f_factors.items():
            all_factors[k] = max(v, all_factors[k])

    result = 1
    for k, v in all_factors.items():
        result *= k**v
    return result
        

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
    assert 232792560 == result
    print 'Elapsed:', end - start

    return 0


if __name__ == '__main__':
    sys.exit(main())

