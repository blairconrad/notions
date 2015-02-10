#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def get_arms(shared_value, last_shared, total, remaining_numbers):
    if len(remaining_numbers) == 1:
        if shared_value + last_shared + remaining_numbers[0] == total:
            return [[[remaining_numbers[0], shared_value, last_shared]]]
        else:
            return []
    
    possibilties = []
    for n in remaining_numbers:
        other_num = total - n - shared_value 
        if n != other_num and other_num in remaining_numbers:
            remaining_candidates = remaining_numbers[:]
            remaining_candidates.remove(n)
            remaining_candidates.remove(other_num)
            for more_arms in get_arms(other_num, last_shared, total, remaining_candidates):
                possibilty = [[n, shared_value, other_num]]
                possibilty += more_arms
                possibilties.append(possibilty)
    return possibilties


def digitize(arms):
    result = ''
    for arm in arms:
        for d in arm:
            result += str(d)
    return result

def order(arms):
    best_index = 0
    best = arms[best_index][0]

    for i in range(1, len(arms)):
        if arms[i][0] < best:
            best_index = i
            best = arms[best_index][0]
    return arms[best_index:] + arms[:best_index]


def solve():
    candidates = []
    for pair in shared.pick_without_replacement([1,2,3,4,5,6,7,8,9], 2):
        arm  = [10] + pair

        nums_left = [1,2,3,4,5,6,7,8,9]
        nums_left.remove(arm[1])
        nums_left.remove(arm[2])
        for arms in get_arms(arm[2], arm[1], sum(arm), nums_left):
            candidates.append([arm] + arms)
    candidates = [order(arms) for arms in candidates]
    candidates = [digitize(arms) for arms in candidates]
    return max(candidates)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert '6531031914842725' == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

