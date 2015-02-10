#!/usr/bin/env python

import sys
sys.path.append('..')
import shared


def triangles():
    last_number = 0
    next_increment = 1
    while True:
        last_number += next_increment
        next_increment += 1
        yield last_number

def solve(n):
    t = triangles()
    while True:
        num = t.next()
        if len(shared.find_divisors(num)) > n:
            return num
    
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 500
    else:
        n = int(args[0])

    result = solve(n)
    print result
    assert 76576500 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

