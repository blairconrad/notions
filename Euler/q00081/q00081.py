#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

matrix = []

def min_sum(x, y):
    here = matrix[x][y]
    previous = 0
    if x > 0:
        if y > 0:
            previous = min(min_sum(x-1,y), min_sum(x,y-1))
        else:
            previous = min_sum(x-1,0)
    elif y > 0:
        previous = min_sum(0, y-1)
    return here + previous

min_sum = shared.Memoize(min_sum)
def solve(matrix):
    return min_sum(len(matrix[0])-1, len(matrix)-1)
    

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
    assert 427337 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

