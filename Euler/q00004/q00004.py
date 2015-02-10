#!/usr/bin/env python

import sys


def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def solve(n):
    return max(find_candidates(n))

def find_candidates(n):
    upper_limit = 10**n
    lower_limit = 10**(n-1)
    for i in range(lower_limit, upper_limit):
        for j in range(lower_limit, i + 1):
            candidate = i * j
            if is_palindrome(candidate):
                yield candidate
    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 3
    else:
        n = int(args[0])

    assert 906609 == solve(n)

    return 0


if __name__ == '__main__':
    sys.exit(main())

