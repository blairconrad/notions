#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared
import collections
import math

# By replacing each of the letters in the word CARE with 1, 2, 9, and
# 6 respectively, we form a square number: 1296 = 362. What is
# remarkable is that, by using the same digital substitutions, the
# anagram, RACE, also forms a square number: 9216 = 962. We shall call
# CARE (and RACE) a square anagram word pair and specify further that
# leading zeroes are not permitted, neither may a different letter
# have the same digital value as another letter.

# Using words.txt (right click and 'Save Link/Target As...'), a 16K
# text file containing nearly two-thousand common English words, find
# all the square anagram word pairs (a palindromic word is NOT
# considered to be an anagram of itself).

# What is the largest square number formed by any member of such a
# pair?

# NOTE: All anagrams formed must be contained in the given text file.

expected = 18769

# def letter_value(letter):
#     return ord(letter) - 0x40 # ord('A') == 0x41

# def word_value(word):
#     value = 0
#     for letter in word:
#         l = letter_value(letter)
#         value *= 10
#         if l >= 10:
#             value *= 10
#         value += l
#     return value
            

def are_squares(word1, word2, square):
    replacement_map = {}
    position = -1
    shrinking_square = square
    while shrinking_square > 0:
        shrinking_square, digit = divmod(shrinking_square, 10)
        replacement_map[str(digit)] = word1[position]
        position -= 1

    for digit, letter in replacement_map.items():
        word1 = word1.replace(letter, digit)

    try:
        if int(word1, 10) != square:
            return False
    except:
        return False
    
    for digit, letter in replacement_map.items():
        word2 = word2.replace(letter, digit)
        
    if word2[0] != '0':
        square2 = int(word2, 10)
        root2 = math.sqrt(square2)
        if int(root2) == root2:
            return True
    return False


def get_highest(word1, word2):

    best = 0
    highest_square = 10**len(word1)-1
    lowest_square = highest_square/10+1

    lowest_root = int(math.sqrt(lowest_square))
    root = int(math.sqrt(highest_square))

    while root > lowest_root:
        square = root**2

        if are_squares(word1, word2, square):
            return max(best, square)

        if are_squares(word2, word1, square):
            return max(best, square)
        root -= 1
    return 0

def solve():
    word_groups = collections.defaultdict(list)
    words = file('words.txt').read().replace('"', '').split(',')
    words.sort(key=len)
    for word in words:
        chars = list(word)
        chars.sort()

        if len(chars) <= 10:
            word_groups[tuple(chars)].append(word)
    word_groups = [group for group in word_groups.values() if len(group) > 1]
    word_groups.sort(lambda g1, g2: cmp(len(g2[0]), len(g1[0])))

    best = 0
    for group in word_groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                best = max(best, get_highest(group[i], group[j]))
    return best
