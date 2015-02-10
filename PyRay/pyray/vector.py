#!/usr/bin/env python

import math

def normalize(vector):
    sum = 0.0
    for elem in vector:
        sum += elem ** 2
    return map(lambda x: x/math.sqrt(sum), vector)

def dotProduct(vector1, vector2):
    sum = 0.0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]
    return sum
