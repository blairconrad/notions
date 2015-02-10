#!/usr/bin/env python

expected = 7273

triangle = []
for row in file('triangle.txt'):
    triangle.append([int(i, 10) for i in row.split()])
    

def solve():
    row_number = len(triangle) - 2
    while row_number >= 0:
        row = triangle[row_number]
        lower_row = triangle[row_number+1]
        for cell_number in range(len(row)):
            row[cell_number] += max(lower_row[cell_number], lower_row[cell_number+1])
        row_number -= 1
    return triangle[0][0]

