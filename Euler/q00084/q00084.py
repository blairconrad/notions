#!/usr/bin/env python

# In the game, Monopoly, the standard board is set up in the following way:

# GO	A1	CC1	A2	T1	R1	B1	CH1	B2	B3	JAIL
# H2	 	C1
# T2	 	U1
# H1	 	C2
# CH3	 	C3
# R4	 	R2
# G3	 	D1
# CC3	 	CC2
# G2	 	D2
# G1	 	D3
# G2J	F3	U2	F2	F1	R3	E3	E2	CH2	E1	FP

# A player starts on the GO square and adds the scores on two 6-sided
# dice to determine the number of squares they advance in a clockwise
# direction. Without any further rules we would expect to visit each
# square with equal probability: 2.5%. However, landing on G2J (Go To
# Jail), CC (community chest), and CH (chance) changes this
# distribution.

# In addition to G2J, and one card from each of CC and CH, that orders
# the player to go directly to jail, if a player rolls three
# consecutive doubles, they do not advance the result of their 3rd
# roll. Instead they proceed directly to jail.

# At the beginning of the game, the CC and CH cards are shuffled. When
# a player lands on CC or CH they take a card from the top of the
# respective pile and, after following the instructions, it is
# returned to the bottom of the pile. There are sixteen cards in each
# pile, but for the purpose of this problem we are only concerned with
# cards that order a movement; any instruction not concerned with
# movement will be ignored and the player will remain on the CC/CH
# square.

# Community Chest (2/16 cards):
# Advance to GO
# Go to JAIL

# Chance (10/16 cards):
# Advance to GO
# Go to JAIL
# Go to C1
# Go to E3
# Go to H2
# Go to R1
# Go to next R (railway company)
# Go to next R
# Go to next U (utility company)
# Go back 3 squares.
#
# The heart of this problem concerns the likelihood of visiting a
# particular square. That is, the probability of finishing at that
# square after a roll. For this reason it should be clear that, with
# the exception of G2J for which the probability of finishing on it is
# zero, the CH squares will have the lowest probabilities, as 5/8
# request a movement to another square, and it is the final square
# that the player finishes at on each roll that we are interested
# in. We shall make no distinction between "Just Visiting" and being
# sent to JAIL, and we shall also ignore the rule about requiring a
# double to "get out of jail", assuming that they pay to get out on
# their next turn.

# By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate these two-digit numbers to produce strings that correspond with sets of squares.

# Statistically it can be shown that the three most popular squares,
# in order, are JAIL (6.24%) = Square 10, E3 (3.18%) = Square 24, and
# GO (3.09%) = Square 00. So these three most popular squares can be
# listed with the six-digit modal string: 102400.

# If, instead of using two 6-sided dice, two 4-sided dice are used,
# find the six-digit modal string.

import random


expected = '101524'

GO = 0
JAIL = 10
G2J = 30
RR = [5, 15, 25, 35]
CC = [2, 17, 33]
CH = [7, 22, 36]
C1 = 11
E3 = 24
H2 = 39
R1 = RR[0]
U = [12, 38]

chance_cards = [
    lambda position: GO,
    lambda position: JAIL,
    lambda position: C1,
    lambda position: E3,
    lambda position: H2,
    lambda position: R1,
    lambda position: ((position + 5)/10 * 10 + 5) % 40,
    lambda position: ((position + 5)/10 * 10 + 5) % 40,
    lambda position: (U[0] < position < U[1]) and U[1] or U[0],
    lambda position: (position-3) % 40] + [lambda position: position] * 6

community_chest_cards = [
    lambda position: GO,
    lambda position: JAIL,
    ] + [lambda position: position] * 14

def roll():
    return random.randint(1,4), random.randint(1,4)

def act(position):
    if position == G2J:
        return JAIL

def solve():
    history = [0]*40
    num_doubles = 0

    position = 0
    count = 0
    while count < 100000:
        dice = roll()
        position = (position + dice[0] + dice[1]) % 40

        if dice[0] == dice[1]:
            num_doubles += 1
        else:
            num_doubles = 0
            
        if num_doubles == 3:
            position = JAIL
            num_doubles = 0

        elif position in CC:
            move = community_chest_cards.pop(0)
            community_chest_cards.append(move)
            position = move(position)
        
        elif position in CH:
            move = chance_cards.pop(0)
            chance_cards.append(move)
            position = move(position)

        elif position == G2J:
            position = JAIL
            
        history[position] += 1
        count += 1

    report = []
    for i in range(len(history)):
        report.append((history[i], i))
    report.sort()
    return ''.join('%02d' % x[1] for x in report[-1:-4:-1])


