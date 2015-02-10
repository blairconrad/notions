#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared


def generate_products(alphabet, multiplicand_length, mulitplier_length):
    for multiplicand in shared.pick_without_replacement(alphabet, multiplicand_length):
        m = int(multiplicand)
        for multiplier in shared.pick_without_replacement(alphabet, mulitplier_length):
            product = m * int(multiplier)
            if product > 9876:
                break
            if ''.join(sorted(multiplicand + multiplier + str(product))) == alphabet:
                yield product
    

def solve(n):
    matches = set()
    alphabet = '123456789'
    for p in generate_products(alphabet, 1, 4):
        matches.add(p)
    for p in generate_products(alphabet, 2, 3):
        matches.add(p)
    return sum(matches)

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
    assert 45228 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

