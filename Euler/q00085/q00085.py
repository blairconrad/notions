#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import math


def tri(n):
    return (n+1) * n  / 2

def solve(n):

    smallest_diff = n
    best_area = 0

    width = 1
    while width <= math.sqrt(n)*2:
        tri_width = tri(width)
        if 2000000 % tri_width < smallest_diff:

            height = 1
            while height <= width:
                area = tri(height) * tri_width
                abs_diff = abs(n-area)
                if abs_diff < smallest_diff:
                    smallest_diff = abs_diff
                    best_area = width * height
                height += 1
        width += 1
    return best_area

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 2000000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 2772 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

