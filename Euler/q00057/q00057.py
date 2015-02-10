#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared



def solve():
    count = 0
    num = 3
    den = 2
    for i in range(2, 1001):
        num, den = num + 2 * den, num + den
        if len(str(num)) > len(str(den)):
            count += 1
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 153 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

