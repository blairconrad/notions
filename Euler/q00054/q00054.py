#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

rank_translation = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
    }
    

high_card = 0
one_pair = 1
two_pair = 2
three_of_a_kind = 3
straight = 4
flush = 5
full_house = 6
four_of_a_kind = 7
straight_flush = 8

def expand_hand(hand):
    cards = [(rank_translation[card[0]], card[1]) for card in hand]
    cards.sort()
    cards = cards[::-1]
    return ([c[0] for c in cards], [c[1] for c in cards])

def find_set(ranks, length):
    #print 'find_set', ranks, length
    for i in range(len(ranks)-length+1):
        found_set = True
        for j in range(i+1, i+length):
            #print i, j, ranks[i], ranks[j]
            found_set = found_set and ranks[i] == ranks[j]
        if found_set:
            return i
    return -1
        
def score(hand):
    ranks = hand[0][:]
    suits = hand[1]

    is_straight = True
    for i in range(1, len(ranks)):
        is_straight = is_straight and ranks[i] == ranks[i-1]-1
    if is_straight:
        return (straight, ranks)

    is_flush = True
    for i in range(1, len(suits)):
        is_flush = is_flush and suits[0] == suits[i]
    if is_flush and is_straight:
        return (straight_flush, ranks)
    elif is_straight:
        return (straight, ranks)
    elif is_flush:
        return (flush, ranks)

    four_of_a_kind_index = find_set(ranks, 4)
    if four_of_a_kind_index >= 0:
        four_of_a_kind_rank = ranks[four_of_a_kind_index]
        del ranks[four_of_a_kind_index:four_of_a_kind_index+4]
        return (four_of_a_kind, four_of_a_kind_rank, ranks[0])

    three_of_a_kind_index = find_set(ranks, 3)
    if three_of_a_kind_index >= 0:
        three_of_a_kind_rank = ranks[three_of_a_kind_index]
        del ranks[three_of_a_kind_index:three_of_a_kind_index+3]
        pair_index = find_set(ranks, 2)
        if pair_index >= 0:
            return (full_house, three_of_a_kind_rank, ranks[pair_index])
        else:
            return (three_of_a_kind, three_of_a_kind_rank, ranks)

    pair_index = find_set(ranks, 2)
    if pair_index >= 0:
        #print 'p:', pair_index
        pair_rank = ranks[pair_index]
        #print 'p:', ranks
        del ranks[pair_index:pair_index+2]
        pair_index2 = find_set(ranks,2)
        if pair_index2 >= 0:
            pair2_rank = ranks[pair_index2]
            del ranks[pair_index2:pair_index2+2]
            return (two_pair, pair_rank, pair2_rank, ranks[0])
        else:
            return (one_pair, pair_rank, ranks)
    return (high_card, ranks)
    
def solve(input_file):
    oneWins = 0
    for line in input_file:
        cards = line.split()
        hand1 = expand_hand(cards[:5])
        hand2 = expand_hand(cards[5:])
        s1 = score(hand1)
        s2 = score(hand2)
        if s1 > s2:
            oneWins += 1
    return oneWins
        

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 20
    else:
        n = int(args[0])

        
    f = file('poker.txt')
    start = datetime.datetime.now()
    result = solve(f)
    end = datetime.datetime.now()
    print result
    assert 376 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

