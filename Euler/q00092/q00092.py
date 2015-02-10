#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import collections

# A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.
# For example,
# 44 -> 32 -> 13 -> 10 -> 1 -> 1
# 85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89
# Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.
# How many starting numbers below ten million will arrive at 89?


square = {}
for i in range(10):
    square[str(i)] = i * i


def chain(n):
    while True:
        #print '  ', n
        if n == 89 or n == 1:
            return n
        n = sum((square[c] for c in str(n)))
chain = shared.Memoize(chain)    


def count_square_sums(position, old_sums):
    new_sums = collections.defaultdict(int)
    for k, v in old_sums.items():
        for i in range(10):
            new_sums[k + i * i] += v
    return new_sums

def solve(num_digits):
    count = 0
    sums = {0: 1}
    for position in range(num_digits):
        sums = count_square_sums(position, sums)

    del sums[0]
    total = 0
    for value, count in sums.items():
        c = chain(value)
        if chain(value) == 89:
            total += count
    return total


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) > 0:
        num_digits = int(args[0])
    else:
        num_digits = 7
        
    start = datetime.datetime.now()
    result = solve(num_digits)
    end = datetime.datetime.now()
    print result
    assert 8581146 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

