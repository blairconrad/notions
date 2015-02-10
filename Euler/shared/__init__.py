#!/usr/bin/env python
import sys
import math
import pprint

def find_divisors(n, memo={1: [1]}):
    if n in memo:
        return memo[n]

    divisors = set()
    divisors.add(1)
    divisors.add(n)
    
    for f1 in xrange(2, n):
        quot, rem = divmod(n, f1)
        if quot < f1: break
        if rem == 0:
            divisors.add(f1)

            if f1 < quot:
                divisors.add(quot)
                quot_divisors = find_divisors(quot)
                for d in quot_divisors:
                    divisors.add(d)
                    divisors.add(f1 * d)
                break

    divisors = sorted(divisors)
    memo[n] = divisors
    return divisors

def find_factors(n, primes=None):
    if n == 1:
        return []

    if primes is None:
        primes = list(prime_generator(n))

    for p in primes:
        if p * p > n:
            return [n]

        if n % p == 0:
            factors = [p]
            n /= p
            while n % p == 0:
                n /= p
                factors.append(p)

            return factors + find_factors(n, primes)
    
def factorial(n):
    result = 1
    for p in range(2, n+1):
        result *= p
    return result

def prime_generator(max_prime = sys.maxint):
    composites = {}
    yield 2
    yield 3
    skip = 2
    n = 5
    while n <= max_prime:
        if n in composites:
            # composite - move on to the next one
            factor = composites.pop(n)
            next_composite = n + 2 * factor
            while next_composite % 6 == 3 or next_composite in composites:
                next_composite += 2 * factor
            composites[next_composite] = factor
        else:
            # prime! how exciting
            next_composite = n * n
            if next_composite <= max_prime:
                composites[next_composite] = n
            yield n
        n += skip
        skip = 6 - skip
    
def is_prime(n, known_primes):
    for p in known_primes:
        if n == p: return True
        if n % p == 0: return False
        if p*p > n: return True

class FibonacciGenerator:
    def __init__(self):
        self.fibs = [1,1,2]
        self.index = -1

    def next(self):
        self.index += 1
        if self.index == len(self.fibs):
            self.fibs.append(self.fibs[self.index-1] + self.fibs[self.index-2])
        return self.fibs[self.index]        
            
        
        self.one, self.two = self.two, self.one + self.two
        return self.two

    def __iter__(self):
        return self
    
class Memoize:
    """Memoize(fn) - an instance which acts like fn but memoizes its arguments
       Will only work on functions with non-mutable arguments
    """
    def __init__(self, fn, count=None):
        self.fn = fn
        self.memo = {}
        if count == None:
            self.filter = lambda x: x
        else:
            self.filter = lambda x: x[:count]

    def __call__(self, *args):
        key_args = self.filter(args)
        if not self.memo.has_key(key_args):
            self.memo[key_args] = self.fn(*args)
        return self.memo[key_args]

def pick_without_replacement(alphabet, count):
    if count == 1:
        for i in range(len(alphabet)):
            yield alphabet[i:i+1]
    else:
        for i in range(len(alphabet)):
            for sub_string in pick_without_replacement(alphabet[:i] + alphabet[i+1:], count-1):
                yield alphabet[i:i+1] + sub_string

def digits(n):
    while n > 0:
        n, rem = divmod(n,10)
        yield rem

def triangular_numbers():
    n = 0
    while True:
        n += 1
        yield (n * n + n) / 2

def square_numbers():
    n = 0
    while True:
        n += 1
        yield n*n

def pentagonal_numbers():
    n = 0
    while True:
        n += 1
        yield (3 * n * n - n)/2

def hexagonal_numbers():
    n = 0
    while True:
        n += 1
        yield 2 * n * n - n

def heptagonal_numbers():
    n = 0
    while True:
        n += 1
        yield (5 * n * n -  3 * n)/2

def octagonal_numbers():
    n = 0
    while True:
        n += 1
        yield 3 * n * n - 2 * n

        
def gcd(a,b):
    while b != 0:
        a, b = b, a %b
    return a

    
def sum_of_digits(n):
    return sum(digits(n))

