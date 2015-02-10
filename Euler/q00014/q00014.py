#!/usr/bin/env python

import sys

def seq(start, known={1: 0}):
    num_steps = 0
    next = start
    while True:
        num_steps += 1
        if next in known:
            result = known[start] = num_steps + known[next]
            return result
        elif next % 2 == 0:
            next /= 2
        else:
            next = 3 * next + 1


def solve(n):
    max_length = 0
    best_start = 1
    for start in range(1, n+1):
        length = seq(start)
        if length > max_length:
            max_length = length
            best_start = start
    return best_start
    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000000
    else:
        n = int(args[0])

    assert 837799 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())
