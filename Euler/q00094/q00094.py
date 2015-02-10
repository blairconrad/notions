#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import math

# It is easily proved that no equilateral triangle exists with
# integral length sides and integral area. However, the almost
# equilateral triangle 5-5-6 has an area of 12 square units.
#
# We shall define an almost equilateral triangle to be a triangle for
# which two sides are equal and the third differs by no more than one
# unit.
#
# Find the sum of the perimeters of all almost equilateral triangles
# with integral side lengths and area and whose perimeters do not
# exceed one billion (1,000,000,000).



#
# generate Primitive Pythagorean Triples using Funny Math
# http://mathworld.wolfram.com/PythagoreanTriple.html

expected = 518408346

def solve():

    triples = [(3, 4, 5)]
    total_perimiter = 0

    while triples:
        (a, b, c) = triples.pop(0)
        short = min(a, b)
        perimeter = 2*(short + c)

        if perimeter > 10**9:
            continue

        if 2*short == c-1 or 2*short == c+1:
            total_perimiter += perimeter
        else:
            continue

        u_triple = (a - 2*b + 2*c, 2*a - b + 2*c, 2*a - 2*b + 3*c)
        a_triple = (a + 2*b + 2*c, 2*a + b + 2*c, 2*a + 2*b + 3*c)
        d_triple = (-a + 2*b + 2*c, -2*a + b + 2*c, -2*a + 2*b + 3*c)


        triples.append(u_triple)
        triples.append(a_triple)
        triples.append(d_triple)
    return total_perimiter


