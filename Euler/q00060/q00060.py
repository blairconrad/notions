#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import bisect

# The primes 3, 7, 109, and 673, are quite remarkable. By taking any
# two primes and concatenating them in any order the result will
# always be prime. For example, taking 7 and 109, both 7109 and 1097
# are prime. The sum of these four primes, 792, represents the lowest
# sum for a set of four primes with this property.

# Find the lowest sum for a set of five primes for which any two
# primes concatenate to produce another prime.

g = shared.prime_generator()

def are_okay(p1, p2):
    sp1 = str(p1)
    sp2 = str(p2)
    d1 = int(sp1+sp2, 0)
    if shared.is_prime(d1):
        d2 = int(sp2+sp1, 0)
        if shared.is_prime(d2):
            return True
    return False

are_okay = shared.Memoize(are_okay)

def insert(sets_so_far, new_prime, old_primes):
    new_primes = old_primes + (new_prime,)
    new_set = (sum(new_primes), new_primes)
    #print new_set, sets_so_far
    bisect.insort(sets_so_far, new_set)

expected = 26033

def solve():
    n = 5
    sets_of_sets = [[] for size in range(n+1)]
    g.next() # discard the 2!
    
    top_prime = g.next() # 3
    sets_of_sets[1].append((top_prime, (top_prime,)))
    top_prime = g.next() # 5 - no good!

    # top_prime = g.next() # 7
    # sets_of_sets[1].append((top_prime, (top_prime,)))
    # sets_of_sets[2].append((3+7, (3,7)))

    while True:
        top_prime = g.next()
        top_mod = top_prime % 3
        #print top_prime
        size = n-1
        while size >= 1:
            for s in sets_of_sets[size]:
                total = s[0]
                primes = s[1]
                if primes[-1] % 3 + top_mod == 0:
                    continue
                okay = True
                for p in primes:
                    if not are_okay(p, top_prime):
                        okay = False
                        break
                if okay:
                    #print 'okay', top_prime, primes
                    insert(sets_of_sets[size+1], top_prime, primes)
            size -= 1
        
        sets_of_sets[1].append((top_prime, (top_prime,)))
        if len(sets_of_sets[n]) > 0:
            return sets_of_sets[n][0][0]
    pass

