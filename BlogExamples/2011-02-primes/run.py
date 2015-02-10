#!/usr/bin/env python


import math

class PrimeGenerator:
    __primes_so_far = [5]
    __increment = 2

    def __init__(self):
        self.__next_index = -1


    def is_prime(self, n):
        if n == 2 or n == 3:
            return True
        elif n % 2 == 0 or n %3 == 0:
            return False
        elif n <= PrimeGenerator.__primes_so_far[-1]:
            return n in PrimeGenerator.__primes_so_far
        else:
            return self.__is_prime(n)

    def __is_prime(self, n):
        limit = math.sqrt(n)
        g = PrimeGenerator()
        g.next() # skip 2
        g.next() # skip 3
        p = g.next()
        while p <= limit:
            if  n % p == 0:
                return False
            p = g.next()
        return True
        
    def next(self):
        self.next = self.__next3
        return 2

    def __next3(self):
        self.next = self.__next5
        return 3

    def __next5(self):
        self.__next_index += 1
        if self.__next_index < len(PrimeGenerator.__primes_so_far):
            return PrimeGenerator.__primes_so_far[self.__next_index]
            
        candidate = PrimeGenerator.__primes_so_far[-1]

        while True:
            candidate += PrimeGenerator.__increment
            PrimeGenerator.__increment = 6 - PrimeGenerator.__increment
        
            if self.__is_prime(candidate):
                PrimeGenerator.__primes_so_far.append(candidate)
                return candidate

    def __iter__(self):
        return self


def naive_trial():
    n = 2
    while True:
        may_be_prime = True
        for k in xrange(2, n):
            if n % k == 0:
                may_be_prime = False
                break
        if may_be_prime:
            yield n
        n += 1

def trial_until_root():
    n = 2
    while True:
        may_be_prime = True
        for k in xrange(2, int(n**0.5)+1):
            if n % k == 0:
                may_be_prime = False
                break
        if may_be_prime:
            yield n
        n += 1


def trial_by_primes():
    primes_so_far = []
    n = 2
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if n % p == 0:
                may_be_prime = False
                break
            if p * p > n: # it's prime
                break
        if may_be_prime:
            primes_so_far.append(n)
            yield n
        n += 1

def odd_trial_by_primes():
    primes_so_far = [2]
    yield 2
    n = 3
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if n % p == 0:
                may_be_prime = False
                break
            if p * p > n: # it's prime
                break
        if may_be_prime:
            primes_so_far.append(n)
            yield n
        n += 2

# def blah(): primes_so_far= [2] yield 2 n = 3 while True: may_be_prime
#     = True for p in primes_so_far: if not n % p: may_be_prime = False
#     break

#         if may_be_prime:
#             # it is!
#             primes_so_far.append(n)
#             yield n
#         n += 1


def naive_by_2():
    primes_so_far = []
    yield 2

    n = 3
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break

        if may_be_prime:
            # it is!
            primes_so_far.append(n)
            yield n
        n += 2

def naive_limit_divisors():
    primes_so_far = [2]
    yield 2
    n = 3
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break
            if p * p >= n: break

        if may_be_prime:
            # it is!
            primes_so_far.append(n)
            yield n
        n += 1

def naive_by_2_limit_divisors():
    primes_so_far = []
    yield 2

    n = 3
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break
            if p * p > n: break

        if may_be_prime:
            # it is!
            primes_so_far.append(n)
            yield n
        n += 2

def naive_by_6_limit_divisors():
    primes_so_far = []
    yield 2
    yield 3

    step = 2
    n = 5
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break
            if p * p > n: break

        if may_be_prime:
            # it is!
            primes_so_far.append(n)
            yield n
        n += step
        step = 6 - step

def naive_by_2_limit_divisors_max():
    primes_so_far = []
    yield 2

    n = 3
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break
            if p * p > n: break

        if may_be_prime:
            # it is!
            if n * n < max: primes_so_far.append(n)
            yield n
        n += 2

def naive_by_6():
    primes_so_far = []
    yield 2
    yield 3

    n = 5
    step = 2
    while True:
        may_be_prime = True
        for p in primes_so_far:
            if not n % p:
                may_be_prime = False
                break

        if may_be_prime:
            # it is!
            primes_so_far.append(n)
            yield n
        n += step
        step = 6 - step


def sieve():
    composites = {}
    n = 2
    while True:
        factor = composites.pop(n, None)
        if factor:
            q = n + factor
            while composites.has_key(q):
                q += factor
            composites[q] = factor
        else:
            # not there - prime
            composites[n*n] = n
            yield n
        n += 1

def sieve_by_2():
    composites = {}
    yield 2
    n = 3
    while True:
        factor = composites.pop(n, None)
        if factor:
            q = n + 2 * factor
            while composites.has_key(q):
                q += 2 * factor
            composites[q] = factor
        else:
            # not there - prime
            composites[n*n] = n
            yield n
        n += 2

def sieve_by_6():
    composites = {}
    yield 2
    yield 3
    step = 2
    n = 5
    while True:
        factor = composites.pop(n, None)
        if factor:
            q = n + 2 * factor
            while composites.has_key(q) or q % 6 not in (1,5):
                q += 2 * factor
            composites[q] = factor
        else:
            # not there - prime
            composites[n*n] = n
            yield n
        n += step
        step = 6 - step

def sieve_by_2_max():
    global max
    composites = {}
    yield 2
    n = 3
    while True:
        factor = composites.pop(n, None)
        if factor:
            q = n + 2 * factor
            while composites.has_key(q):
                q += 2 * factor
            composites[q] = factor
        else:
            # not there - prime
            if n*n <= max:
                composites[n*n] = n
            yield n
        n += 2

def euler_sieve():
    # Create a candidate list within which non-primes will
    # marked as None, noting that only candidates below
    # sqrt(n) need be checked. 
    candidates = range(max+1)
    fin = int(max**0.5)
 
    # Loop over the candidates, marking out each multiple.
    # If the current candidate is already checked off then
    # continue to the next iteration.
    for i in xrange(2, fin+1):
        if not candidates[i]:
            continue
 
        candidates[2*i::i] = [None] * (max//i - 1)
 
    # Filter out non-primes and return the list.
    return [i for i in candidates[2:] if i]
        

def euler_sieve_2():
    # Create a candidate list within which non-primes will
    # marked as None, noting that only candidates below
    # sqrt(n) need be checked. 
    candidates = range(1, max+1, 2)
    fin = int(max**0.5)
 
    # Loop over the candidates, marking out each multiple.
    # If the current candidate is already checked off then
    # continue to the next iteration.
    for i in xrange(3, fin+1, 2):
        if not candidates[i/2]:
            continue

        candidates[i/2+i::i] = [None] * ((len(candidates)-1-(i)/2)/i)
 
    # Filter out non-primes and return the list.
    result = [2]
    result.extend([i for i in candidates[1:] if i])
    return result
        

def iterated_euler_sieve_2():
    block_size = 2 * 10**6
    biggest_candidate = min(max, block_size)
    
    # Create a candidate list within which non-primes will
    # marked as None, noting that only candidates below
    # sqrt(n) need be checked. 
    candidates = range(1, biggest_candidate+1, 2)
    fin = int(biggest_candidate**0.5)
 
    # Loop over the candidates, marking out each multiple.
    # If the current candidate is already checked off then
    # continue to the next iteration.
    for i in xrange(3, fin+1, 2):
        if not candidates[i/2]:
            continue

        candidates[i/2+i::i] = [None] * ((len(candidates)-1-(i)/2)/i)
 
    # Filter out non-primes and return the list.
    result = [2]
    result.extend([i for i in candidates[1:] if i])

    # do another block
    while biggest_candidate < max:
        start = biggest_candidate+1
        biggest_candidate += block_size
        # Create a candidate list within which non-primes will
        # marked as None, noting that only candidates below
        # sqrt(n) need be checked. 
        candidates[:] = range(start, biggest_candidate+1, 2)
        fin = int(biggest_candidate**0.5)

        # Loop over the candidates, marking out each multiple.
        # If the current candidate is already checked off then
        # continue to the next iteration.
        i = 1
        while i < len(result):
            p = result[i]
            if p > fin:
                break
            #start_marking_at = (p*((start+p-1)//p)-start)/2
            mult = (start+p-1)//p
            if mult % 2 == 0: mult += 1
                
            #print p, mult
            start_marking_at = (p*mult-start)/2
            #start_marking_at = (p*((start+p-1)//p)-start)/2
            #print p, start, start_marking_at
            candidates[start_marking_at::p] = [None] * ((len(candidates)-start_marking_at+p+-1)/p)
            #print candidates
            i += 1

        # Filter out non-primes and return the list.
        result.extend([i for i in candidates[:] if i])


    return result

    
        

functions = {}
for k, v in vars().items():
    if hasattr(v, 'func_name'):
        functions[k] = v

import sys
import profile
import datetime


def run(f):
    global max
    start = datetime.datetime.now()
    count = 1
    primes = f()
#    print len(primes), primes
    for p in f():
        count += 1
        if p > max: break
    end = datetime.datetime.now()
    elapsed = end-start
    return max, count, elapsed.seconds + (elapsed.microseconds/1000000.0)

def main(args=None):
    if  len(args) < 2:
        print 'usage: run max method'
        print 'what should I run?'
        print '  ' + ', '.join(functions)
        return 1

    global max
    max = int(args[0])
    print run(functions[args[1]])
    #profile.run('print run(' + args[1] + '); print')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

