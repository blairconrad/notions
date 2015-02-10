#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared
import collections

def build_prob_table(num_sides, num_dice):
    table = {0:1}
    for die in range(num_dice):
        new_table = collections.defaultdict(int)
        for value in range(1,num_sides+1):
            for old_sum, count in table.items():
                new_table[old_sum + value] += count
        table = new_table
    return table
    
def solve():
    fours_table =  build_prob_table(4,9)
    sixes_table =  build_prob_table(6,6)

    num_wins = 0
    for four_score, four_count in fours_table.items():
        for six_score, six_count in sixes_table.items():
            if four_score > six_score:
                num_wins += four_count * six_count
    num_outcomes = float(4**9 * 6**6)
    return '%9.7f' % (num_wins/float(num_outcomes))
    


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    start = datetime.datetime.now()
    result = solve()
    end = datetime.datetime.now()
    print result
    assert '0.5731441' == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

