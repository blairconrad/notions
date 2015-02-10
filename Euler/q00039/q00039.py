#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def count_triangles(p):
    triangles = []
    for a in range(1, p-1):
        # solve a + b + c = p and a*a + b*b + c*c to get b and c in terms of a and p
        b = p * (p-2*a)/2/(p-a)
        c = p - b- a
        if a*a + b*b == c*c:
            triangles.append((a,b,c))
            
    return (len(triangles), p)

def solve(n):
    # only need to check even ps, since if a and b are even, so must be c,
    # if a and b are odd, so much be c,
    # if one of a and be are odd, c will be odd
    return max((count_triangles(p) for p in xrange(12, n+1, 2)))[1]
        
    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 840 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

