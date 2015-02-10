#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    powers = set()
    powers.add(1)
    for base in range(2,10):
        exponent = 0
        while True:
            exponent += 1
            power = base ** exponent
            #print power, base, exponent
            if len(str(power)) == exponent:
                #print 'yes'
                powers.add(power)
            elif len(str(power)) < exponent:
                    break
    return len(powers)

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
    assert 49 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

