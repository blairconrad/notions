#!/usr/bin/env python

import sys

def solve(width, height, memo =
          { (0, 1): 1,
            (1, 0): 1,
            }
          ):
    if (width, height) in memo:
        return memo[(width, height)]

    routes = 0
    if width > 0:
        routes += solve(width-1, height)
    if height > 0:
        routes += solve(width, height-1)
    memo[(width, height)] = routes
    return routes

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) < 2:
        width = 20
        height = 20
    else:
        width = int(args[0])
        height = int(args[1])

    assert 137846528820 == solve(width, height)

    return 0


if __name__ == '__main__':
    sys.exit(main())

