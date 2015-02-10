#!/usr/bin/env python

import sys

def get_days_in_month(year, month):
    if month == 1 and year % 4 == 0 and ( year % 400 == 0 or year % 100 != 0 ):
        days = 29
    else:
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]
    return days

def solve():
    day = 2 # Tuesday
    count = 0
    for year in xrange(1901, 2001):
        for month in xrange(12):
            if day == 0:
                count += 1
            day += get_days_in_month(year, month)
            day %= 7
    return count

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    assert 171 == solve()
    return 0


if __name__ == '__main__':
    sys.exit(main())

