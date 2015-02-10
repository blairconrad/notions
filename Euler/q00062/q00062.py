#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import collections

def cubes():
    i = 0
    while True:
        i += 1
        yield i*i*i

def solve(n):
    all_cubes = collections.defaultdict(list)

    for c in cubes():
        perms = all_cubes[tuple(sorted(shared.digits(c)))]
        perms.append(c)
        if len(perms) == n:
            return perms[0]
    
    pass


        
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 5
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 127035954683 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

