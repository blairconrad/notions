#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def is_triangle(n):
    j = 1
    tri = 1
    while True:
        if tri == n:
            return True
        elif tri > n:
            return False
        j += 1
        tri += j

is_triangle = shared.Memoize(is_triangle)

def solve(words):
    count = 0
    for word in words:
        if is_triangle(sum(value(c) for c in word)):
            count += 1
    return count

def value(c):
    return ord(c)-64

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    data = file('words.txt').read()
    data = data.replace('"', '')
    words = data.split(',')

    start = datetime.datetime.now()
    result = solve(words)
    end = datetime.datetime.now()
    print result
    assert 162 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

