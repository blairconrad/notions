#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# In the game of darts a player throws three darts at a target board
# which is split into twenty equal sized sections numbered one to
# twenty.

# The score of a dart is determined by the number of the region that
# the dart lands in. A dart landing outside the red/green outer ring
# scores zero. The black and cream regions inside this ring represent
# single scores. However, the red/green outer ring and middle ring
# score double and treble scores respectively.

# At the centre of the board are two concentric circles called the
# bull region, or bulls-eye. The outer bull is worth 25 points and the
# inner bull is a double, worth 50 points.

# There are many variations of rules but in the most popular game the
# players will begin with a score 301 or 501 and the first player to
# reduce their running total to zero is a winner. However, it is
# normal to play a "doubles out" system, which means that the player
# must land a double (including the double bulls-eye at the centre of
# the board) on their final dart to win; any other dart that would
# reduce their running total to one or lower means the score for that
# set of three darts is "bust".

# When a player is able to finish on their current score it is called
# a "checkout" and the highest checkout is 170: T20 T20 D25 (two
# treble 20s and double bull).

# There are exactly eleven distinct ways to checkout on a score of 6:
#	D3
# 	D1	D2
# 	S2	D2
# 	D2	D1
# 	S4	D1
# 	S1	S1	D2
# 	S1	T1	D1
# 	S1	S3	D1
# 	D1	D1	D1
# 	D1	S2	D1
# 	S2	S2	D1

# Note that D1 D2 is considered <b>different</b> to D2 D1 as they
# finish on different doubles. However, the combination S1 T1 D1 is
# considered the <b>same</b> as T1 S1 D1.

# In addition we shall not include misses in considering combinations; for example, D3 is the <b>same</b> as 0 D3 and 0 0 D3.

# Incredibly there are 42336 distinct ways of checking out in total.

# How many distinct ways can a player checkout with a score less than
# 100?

expected = 38182

triples = range(1, 20+1)
doubles = triples[:] + [25]
singles = doubles[:]

def score_one(score):
    plays = []
    for s in singles:
        if s == score: plays.append('s%d' % s)
    for d in doubles:
        if 2 * d == score: plays.append('d%d' % d)
    for t in triples:
        if 3 * t == score: plays.append('t%d' % t)

    return plays

def score_two(score):
    plays = set()
    for  s in singles:
        new_score = score - s
        if new_score <= 0:
            break
        first_throw = 's%d' % s

        for second_throw in score_one(new_score):
            two = [first_throw, second_throw]
            two.sort()
            plays.add(''.join(two))
            
    for d in doubles:
        new_score = score - 2 * d

        if new_score <= 0:
            break
        first_throw = 'd%d' % d

        for second_throw in score_one(new_score):
            two = [first_throw, second_throw]
            two.sort()
            plays.add(''.join(two))
            
    for t in triples:
        new_score = score - 3 * t
        if new_score <= 0:
            break
        first_throw = 't%d' % t

        for second_throw in score_one(new_score):
            two = [first_throw, second_throw]
            two.sort()
            plays.add(''.join(two))
            
    return plays

def solve():

    count = 0

    for score in range(1, 100):

        for d in doubles:
            if 2*d > score: break
            if 2*d == score:
                count += 1
                continue
            new_score = score - 2*d
            count += len(score_one(new_score))
            count += len(score_two(new_score))

    return count


