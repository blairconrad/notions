#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import pprint


def copy(grid):
    return [row[:] for row in grid]

def what_can_be_in(grid, row_num, col_num):
    what = set(range(10))
    for i in range(9):
        d = grid[row_num][i]
        what.discard(d)
        what.discard(grid[i][col_num])
    r = 3*(row_num/3)
    for i in range(3):
        c = 3*(col_num/3)
        for j in range(3):
            what.discard(grid[r+i][c+j])
    return what


def load_grids(input, n):
    grids = []
    for i in range(n):
        name = input.next()
        grid = []
        for j in range(9):
            grid.append([ord(c)-ord('0') for c in input.next().strip()])
        grids.append(grid)
    return  grids

def solve_one_grid(grid, row_num=0, col_num=0):
    while row_num < 9:
        while col_num < 9:
            if grid[row_num][col_num] == 0:
                break
            else:
                col_num += 1
        if col_num >= 9:
            # walked off the end
            col_num = 0
            row_num += 1
        else: # didn't
            break
    if row_num >= 9:
        # walked off the bottom
        return grid # done!
    # okay, we found a 0 - see what could be here, and for each value,
    # copy it in and continue to solve from this point on
    potentials = what_can_be_in(grid, row_num, col_num)
    #print row_num, col_num, potentials
    for p in potentials:
        #print '  ', p
        g = copy(grid)
        g[row_num][col_num] = p
        solution = solve_one_grid(g, row_num, col_num+1)
        if solution:
            return solution
    # no solution
    return None

def solve(grids):
    solutions = []
    for grid in grids:
        solutions.append(solve_one_grid(grid))
    return sum((100 * solution[0][0] + 10 * solution[0][1] + solution[0][2] for solution in solutions))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 50
    else:
        n = int(args[0])

    f = file('sudoku.txt')
    start = datetime.datetime.now()
    grids = load_grids(f, n)
    result = solve(grids)
    end = datetime.datetime.now()
    print result
    assert 24702 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

