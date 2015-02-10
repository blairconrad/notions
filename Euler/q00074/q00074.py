#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

# The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:
#
# 1! + 4! + 5! = 1 + 24 + 120 = 145
#
# Perhaps less well known is 169, in that it produces the longest
# chain of numbers that link back to 169; it turns out that there are
# only three such loops that exist:
#
# 169 -> 363601 -> 1454 -> 169
# 871 -> 45361 -> 871
# 872 -> 45362 -> 872
#
# It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,
#
# 69 -> 363600 -> 1454 -> 169 -> 363601 (-> 1454)
# 78 -> 45360 -> 871 -> 45361 (-> 871)
# 540 -> 145 (-> 145)
#
# Starting with 69 produces a chain of five non-repeating terms, but
# the longest non-repeating chain with a starting number below one
# million is sixty terms.
#
# How many chains, with a starting number below one million, contain
# exactly sixty non-repeating terms?

max_length = 60
factorials = [shared.factorial(i) for i in range(10)]

def fact_it_up(n):
    return sum((factorials[int(d)] for d in str(n)))

fact_it_up = shared.Memoize(fact_it_up)


def get_chain(n):
    chain = []
    while n not in chain:
        chain.append(n)
        n = fact_it_up(n)
    return chain

get_chain = shared.Memoize(get_chain)

"""If the chain is longer than max_length, return max_length+1"""
def get_chain_length(n):
    next_term = fact_it_up(n)
    chain = get_chain(next_term)
    try:
        return chain.index(n) + 1
    except:
        return len(chain) + 1

def solve():
    max_start = 1000000
    desired_number_of_chains = 60

    count = 0
    for n in range(1, max_start):
        length = get_chain_length(n)
        #print n, length
        if 60 == length:
            count += 1
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert 402 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

