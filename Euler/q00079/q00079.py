#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import collections



def find_minimum_position(c, keys):
    pos = 0
    for key in keys:
        new_pos = key.find(c)
        if pos < new_pos:
            pos = new_pos
    return pos

def get_alphabet(keys):
    alphabet = collections.defaultdict(int)
    for key in keys:
        key_count = collections.defaultdict(int)
        for c in key:
            key_count[c] = key_count[c] + 1
        for c, count in key_count.items():
            if count > alphabet[c]:
                alphabet[c] = count
    alphabet = alphabet.items()
    alphabet.sort()
    result = ''
    for c, count in alphabet:
        result += c * count
    return result
            

def find_password(alphabet,  keys):
    for c in alphabet:
        if find_minimum_position(c, keys) == 0:
            new_keys = set(((key for key in ((k.replace(c, '', 1) for k in keys)) if key != '')))
            return c + find_password(alphabet.replace(c, '', 1), new_keys)
    return ''
    
def solve(n):
    passing_keys = set([line.strip() for line in file('keylog.txt')])
    alphabet = get_alphabet(passing_keys)
    return find_password(alphabet, passing_keys)


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert '73162890' == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

