#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import bisect

# def is_pent(n):
#     i = 1
#     p = pent(i)
#     while p < n:
#         i += 1
#         p = pent(i)        
#     return p == n

# is_pent = shared.Memoize(is_pent)

def pent(n):
    return n * ( 3 * n -1 ) / 2

def solve():
    pents = [0]
    m = 1
    while True:
        pm = pent(m)
        pents.append(pm)
        #print pents[-1]
        #j  = bisect.bisect_left(pents, pm/2)
        j = m-2
        while j > 1:
            pj = pents[j]
            j -= 1
            if pj >= pm/2:
                continue
            pk = pm - pj
            if pents[bisect.bisect_right(pents, pk, j)-1] == pk:
                if pk - pj in pents:
                    return pk-pj
        m += 1

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 5482660 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

