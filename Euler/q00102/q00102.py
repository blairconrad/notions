#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared


def positive_x_hits_segment(point1, point2):

    rise = point2[1] - point1[1]
    if rise == 0:
        return ((point2[1] <= 0 and point1[1] >= 0) or
                (point2[1] >= 0 and point1[1] <= 0))
    run = point2[0] - point1[0]
    if 0 <= float(-point1[1])/(rise) <= 1:
        return point1[0] + run * float(-point1[1])/(rise) >= 0
    
def origin_in_triangle(triangle):
    count = 0
    if positive_x_hits_segment(triangle[0], triangle[1]):
        count += 1
    if positive_x_hits_segment(triangle[1], triangle[2]):
        count += 1
    if positive_x_hits_segment(triangle[2], triangle[0]):
        count += 1
    return count == 1

def solve(n, triangles):
    count = 0
    for i in range(n):
        if origin_in_triangle(triangles[i]):
            count += 1
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    triangles = []
    for line in file('triangles.txt'):
        vertices = [int(p, 10) for p in line.split(',')]
        triangles.append([[vertices[0], vertices[1]],
                         [vertices[2], vertices[3]],
                         [vertices[4], vertices[5]],
                         ])

    start = datetime.datetime.now()
    result = solve(n, triangles)
    end = datetime.datetime.now()
    print result
    assert 228 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

