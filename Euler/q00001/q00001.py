#!/usr/bin/env python

import sys

def solve(supremum=1000):
    return sum(n for n in range(1,supremum) if n % 3== 0 or n % 5 == 0)


expected = 233168
def main(args=sys.argv[1:]):

    if len(args) == 0:
        supremum = 1000
    else:
        supremum = int(args[0])

    assert expected == solve(supremum)

    return 0


if __name__ == '__main__':
    sys.exit(main())

