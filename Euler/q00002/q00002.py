#!/usr/bin/env python

import shared
from itertools import ifilter as filter, takewhile

expected = 4613732

def solve(maximum=4000000):
    return sum(
        filter(lambda f: f%2 == 0,
                          takewhile(lambda f: f <=  maximum, shared.FibonacciGenerator())))
