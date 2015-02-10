#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import math

# It turns out that 12 cm is the smallest length of wire that can be
# bent to form an integer sided right angle triangle in exactly one
# way, but there are many more examples.
#
# 12 cm: (3,4,5)
# 24 cm: (6,8,10)
# 30 cm: (5,12,13)
# 36 cm: (9,12,15)
# 40 cm: (8,15,17)
# 48 cm: (12,16,20)
#
# In contrast, some lengths of wire, like 20 cm, cannot be bent to
# form an integer sided right angle triangle, and other lengths allow
# more than one solution to be found; for example, using 120 cm it is
# possible to form exactly three different integer sided right angle
# triangles.
#
# 120 cm: (30,40,50), (20,48,52), (24,45,51)
#
# Given that L is the length of the wire, for how many values of L <=
# 1,500,000 can exactly one integer sided right angle triangle be
# formed?

# if a, b, c is a primitive integer-sided triangle,
# a = m*m - n*n
# b= 2mn
# c = m*m + n*n
# so a + b + c = 2m(m+n)
# find these triangles, make sure a and b are relatively prime, and
# cross out multiples
def q00075(max_p):
    counts = {}
    for i in xrange(12,max_p+1, 2):
        counts[i] = 0
        
    for m in xrange(2, int(math.sqrt(max_p/2))):
        for n in xrange(1, m):
            if shared.gcd(m*m-n*n,2*m*n) > 1: continue
            p = 2 * m * (m + n)
            if p > max_p:
                continue
            #print p
            this_p = p
            while this_p <= max_p:
                counts[this_p] += 1
                this_p += p

    num = 0
    for k, v in counts.items():
        if v == 1:
            num += 1
    return num
        

    
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1500000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = q00075(n)
    end = datetime.datetime.now()
    print result
    assert 161667 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

