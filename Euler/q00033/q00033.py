#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve():
    top = 1
    bottom = 1
    for denominator in range(11, 100):
        for numerator in range(11, denominator):
            if numerator % 10 == 0 or denominator % 10 == 0:
                continue
            if numerator % 11 == 0  and denominator % 11 == 0:
                continue
            #xprint numerator, denominator
            s_num = str(numerator)
            s_den = str(denominator)
            common = ''
            for l in s_num:
                if l in s_den:
                    common = l
                    
            if common:
                n = int(s_num.replace(common, '', 1))
                d = int(s_den.replace(common, '', 1))
                if float(numerator)/denominator == float(n)/d:
                    top *= n
                    bottom *= d
    top_factors = shared.find_factors(top)
    bottom_factors = shared.find_factors(bottom)
    for f in top_factors:
        if f in bottom_factors:
            bottom_factors.remove(f)

    result = 1
    for f in bottom_factors:
        result *= f
    return result

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 100 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

