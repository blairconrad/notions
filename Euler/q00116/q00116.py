#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# A row of five black square tiles is to have a number of its tiles
# replaced with coloured oblong tiles chosen from red (length two),
# green (length three), or blue (length four).

# If red tiles are chosen there are exactly seven ways this can be
# done.

# If green tiles are chosen there are three ways.  And if blue tiles
# are chosen there are two ways.

# Assuming that colours cannot be mixed there are 7 + 3 + 2 = 12 ways
# of replacing the black tiles in a row measuring five units in
# length.

# How many different ways can the black tiles in a row measuring fifty
# units in length be replaced if colours cannot be mixed and at least
# one coloured tile must be used?

# NOTE: This is related to problem 117.
expected = 20492570929L

@shared.Memoize
def fit(num_squares, tile_size):
    if num_squares < tile_size:
        return 0
    if num_squares == tile_size:
        return 1
    return fit(num_squares-1, tile_size) + fit(num_squares-tile_size, tile_size) + 1

def solve():
    max_length = 50

    return sum((fit(max_length, tile_length) for tile_length in range(2, 5)))

