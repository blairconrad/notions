#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def is_lychrel(n):
    count = 0
    while count < 50:
        #print ' ', n
        count += 1
        backward_n = int(str(n)[::-1],10)
        n += backward_n
        str_n = str(n)
        if str_n == str_n[::-1]:
            return False
    return True

def solve(n):
    count = 0
    for i in range(1,n):
        #print i
        if is_lychrel(i):
            count += 1
    return count
            

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 10000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 249 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

