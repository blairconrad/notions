#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

matrix = []

def min_sum(x, y, last_direction=0):

    here = matrix[x][y]
    if y == 0:
        return here

    candidates = [min_sum(x,y-1)]
    if x > 0 and last_direction != 1:
        candidates.append(min_sum(x-1, y, -1))
    if x < len(matrix[0])-1 and last_direction != -1:
        candidates.append(min_sum(x+1,y, 1))
        
    return here + min(candidates)

min_sum = shared.Memoize(min_sum)

def solve(matrix):
    return min((min_sum(x, len(matrix[0])-1) for x in range(len(matrix))))
    

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    global matrix

    for line in file('matrix.txt'):
        matrix.append([int(s, 10) for s in line.split(',')])
        
    start = datetime.datetime.now()
    result = solve(matrix)
    end = datetime.datetime.now()
    print result
    assert 260324 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

