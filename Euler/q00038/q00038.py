#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def can_be_made_from_concatenated_product(pandigital):
    chunksize = 1
    while chunksize <= len(pandigital)/2:
        rest_of_pandigital = pandigital
        multiplicand = int(pandigital[:chunksize])
        multiplier = 1
        while len(rest_of_pandigital) > 0:
            #print multiplicand, multiplier, rest_of_pandigital
            product = str(multiplicand * multiplier)
            if not  rest_of_pandigital.startswith(product):
                break
            rest_of_pandigital = rest_of_pandigital[len(product):]
            multiplier += 1
        if len(rest_of_pandigital) == 0:
            return True
        chunksize += 1
            
                           

def solve(n):
    alphabet = '987654321'
    for f in shared.pick_without_replacement(alphabet, 9):
        if can_be_made_from_concatenated_product(f):
            return int(f)

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
    assert 932718654 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

