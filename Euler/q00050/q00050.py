#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def solve(n):
    primes = []
    g = shared.PrimeGenerator()
    p = g.next()
    while p < n:
        primes.append(p)
        p = g.next()

    buffer = []
    next_index = 0
    while sum(buffer) < n:
        buffer.append(next_index)
        next_index += 1
    max_buffer_length = len(buffer)
    buffer = []
    while True:
        buffer = primes[:max_buffer_length]
        total = sum(buffer)
        next_prime = max_buffer_length
        while total < n:
            if g.is_prime(total):
                return total
            total -= buffer.pop(0)
            buffer.append(primes[next_prime])
            next_prime += 1
            total += buffer[-1]
        max_buffer_length -= 1
        
        
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000000
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 997651 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

