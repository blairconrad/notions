#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# Using a combination of black square tiles and oblong tiles chosen
# from: red tiles measuring two units, green tiles measuring three
# units, and blue tiles measuring four units, it is possible to tile a
# row measuring five units in length in exactly fifteen different
# ways.

# How many ways can a row measuring fifty units in length be tiled?

# NOTE: This is related to problem 116.

expected = 100808458960497L

@shared.Memoize
def fit(num_squares):
    if num_squares < 0:
        return 0
    if num_squares == 0:
        return 1
    
    return sum(fit(num_squares-tile_size) for tile_size in range(1,5))

def solve():
    return fit(50)

