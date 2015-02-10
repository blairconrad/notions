#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def get_digit_list(num_digits, num_to_pick):
    s = set()
    for group in shared.pick_without_replacement(range(num_digits), num_to_pick):
        s.add(tuple(sorted(group)))
    return s

def replace_digits(start, replacement_char, digits):
    for d in digits:
        start = start[:d] + replacement_char + start[d+1:]
    return start

def solve(n):
    already_tried_templates = {}
    g = shared.PrimeGenerator()
    p = g.next()
    #while p < 120000:
    #    p = g.next()
    while True:
        p = g.next()
        #print p
        for i in range(1, len(str(p))):
            for digits in get_digit_list(len(str(p)), i):
                template = replace_digits(str(p), 'x', digits)
                if template in already_tried_templates:
                    continue
                else:
                    already_tried_templates[template] = None

                #print 'd', digits
                best = 0
                count = 0
                for j in range(10):
                    replacement_char = str(j)
                    next_try = str(p)
                    next_try = replace_digits(next_try, replacement_char, digits)

                    if next_try.startswith('0'):
                        continue
                    
                    next_try = int(next_try)
                    #print ' ', next_try
                    if  g.is_prime(next_try):
                        if best == 0:
                            best = next_try

                        count += 1
                        #print '   prime', next_try, count
                if count >= n:
                    return best

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 8
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 121313 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

