#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared


def works(n):
    target_digits =  '1234567890'
    s = str(n)[::2]
    return s == target_digits

def solve(n):
    last_two = 30
    base = 1000000000
    while base < 1500000000:
        for end in (30,70):
            attempt = base + end
            product = attempt ** 2
            if works(product):
                return attempt
        base += 100

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
    assert 1389019170 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

