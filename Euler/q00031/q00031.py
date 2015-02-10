#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n, coins):
    if n == 0:
        return 1
    
    if not coins:
        return 0
    count = 0
    if  coins[0] <= n:
        count += solve(n-coins[0], coins)
    count += solve(n, coins[1:])
    return count

solve = shared.Memoize(solve)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 200
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n, (200, 100, 50, 20, 10, 5, 2, 1))
    end = datetime.datetime.now()
    print result
    assert 73682 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

