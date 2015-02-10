#!/usr/bin/env python

import sys
sys.path.append('..')
import shared

def find_recurring_cycle(n):
    divmods = []
    dividend = 1
    while True:
        while dividend < n:
            dividend *= 10
        (quotient, remainder) = divmod(dividend, n)
        if remainder == 0:
            return '0'

        if (quotient, remainder) in divmods:
            index = divmods.index((quotient, remainder))
            if index >= 0:
                return ''.join((str(d[0]) for d in divmods[index:]))
        else: 
           divmods.append((quotient, remainder))
        dividend = remainder

def solve(n):
    maxlen = 0
    maxi = 0
    for i in range(1, n+1):
        repeater = find_recurring_cycle(i)
        if len(repeater) > maxlen:
            maxlen = len(repeater)
            maxi = i
    return maxi
            

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    result = solve(n)
    print result
    assert 983 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

