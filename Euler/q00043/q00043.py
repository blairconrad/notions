#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def march_left(suffixes, divisor):
    results = []
    for suffix in suffixes:
        alphabet = '0123456789'
        for c in suffix:
            alphabet = alphabet.replace(c,'')

        for c in alphabet:
            if int(c + suffix[:2], 10) % divisor == 0:
                results.append(c + suffix)
    return results
    

def solve(n):
    results = [num for num in shared.pick_without_replacement('0123456789', 3)
             if int(num,10) % 17 == 0]
    results = march_left(results, 13)
    results = march_left(results, 11)
    results = march_left(results, 7)
    results = march_left(results, 5)
    results = march_left(results, 3)
    results = march_left(results, 2)
    results = march_left(results, 1)
    return sum(int(n, 10) for n in results)

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
    assert 16695334890 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

