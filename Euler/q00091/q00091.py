#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import pprint

# There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between 0 and 2 inclusive; that is,
# 0 <= x_(1), y_(1), x_(2), y_(2) <= 2.
# Given that 0 = x_(1), y_(1), x_(2), y_(2) = 50, how many right triangles can be formed?

expected = 14234

def solve():
    max = 50

    num_with_b_in_corner = 0 # we'll count double, so we can skip a _in_corner
    for ax in range(max+1):
        for ay in range(max+1):
            if ax == ay == 0: continue
            for bx in range(max+1):
                for by in range(max+1):
                    if bx == by == 0: continue
                    if ax == bx and ay == by: continue
                    if (bx*bx + by*by) + (ax-bx)**2 + (ay-by)**2 == (ax*ax + ay*ay):
                        num_with_b_in_corner += 1
                           
    # pprint.pprint(a_in_corner)  
    # pprint.pprint(b_in_corner)
    # pprint.pprint(z_in_corner)
    num_with_z_in_corner = max * max
    return num_with_z_in_corner + num_with_b_in_corner
