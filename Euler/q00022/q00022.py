#!/usr/bin/env python

import sys
sys.path.append('../shared')

def score(name):
    return sum(ord(c) - ord('A') + 1 for c in name)

def solve(names):
    names.sort()
    return sum(((i+1) * score(names[i]) for i in range(len(names))))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    f = file('names.txt').read()
    f = f.replace('"', '')
    names = f.split(',')
    result = solve(names)
    print result
    assert 871198282 == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

