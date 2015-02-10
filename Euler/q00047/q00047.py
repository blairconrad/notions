#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def count_factors(n):
    #print '  ', n
    s = set()
    for f in shared.find_factors(n):
        s.add(f)
    return len(s)

def solve():
    base = 3
    i = 4
    while True:
        i += 4
        if count_factors(i) == 4:
            # yay! check 1 below
            if count_factors(i-1) == 4:
                if count_factors(i-2) == 4:
                    #print(i-3)
                    #yay! check the one below
                    if count_factors(i-3) == 4:
                        return i-3
                    else:
                        # 2 below was okay - just need one above
                        if count_factors(i+1) == 4:
                            return i-2
                else:
                    # 1 below was okay - just need 1 above and 2 above
                    if count_factors(i+2) == 4:
                        #print i+1
                        if count_factors(i+1) == 4:
                            return i-1
            else:
                # only have i
                if count_factors(i+2) == 4 and count_factors(i+1) == 4  and count_factors(i+3) == 4:
                    return i

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 134043 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

