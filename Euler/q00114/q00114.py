#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# A row measuring seven units in length has red blocks with a minimum
# length of three units placed on it, such that any two red blocks
# (which are allowed to be different lengths) are separated by at
# least one black square. There are exactly seventeen ways of doing
# this.

# How many ways can a row measuring fifty units in length be filled?

#NOTE: Although the example above does not lend itself to the
#possibility, in general it is permitted to mix block sizes. For
#example, on a row measuring eight units in length you could use red
#(3), black (1), and red (4).

expected = 16475640049L

@shared.Memoize
def fit(row_size):
    if row_size < 0:
        return 0

    if row_size < 3:
        return 1

    result = fit(row_size - 1) + \
           sum(fit(row_size - tile_size - 1) for tile_size in range(3,row_size+1)) + \
           1
    return result

def solve():
    row_size = 50
    return fit(row_size)

