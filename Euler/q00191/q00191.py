#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# A particular school offers cash rewards to children with good attendance and punctuality. If they are absent for three consecutive days or late on more than one occasion then they forfeit their prize.
# 
# During an n-day period a trinary string is formed for each child consisting of L's (late), O's (on time), and A's (absent).
# 
# Although there are eighty-one trinary strings for a 4-day period that can be formed, exactly forty-three strings would lead to a prize:
# 
# OOOO OOOA OOOL OOAO OOAA OOAL OOLO OOLA OAOO OAOA
# OAOL OAAO OAAL OALO OALA OLOO OLOA OLAO OLAA AOOO
# AOOA AOOL AOAO AOAA AOAL AOLO AOLA AAOO AAOA AAOL
# AALO AALA ALOO ALOA ALAO ALAA LOOO LOOA LOAO LOAA
# LAOO LAOA LAAO
# 
# How many "prize" strings exist over a 30-day period?

expected = 1918080160

# Well, there can be only 0 or 1 L. That makes a difference.
#
# Possibly easiest to take the total and subtract out the number with
# 3+ As in a row. Or maybe not.

# no Ls. We'll handle those separately
@shared.Memoize
def winners_no_ls_ending_in_as(length, num_as):
    #print 'winners_no_ls_ending_in_as', length, num_as
    if length == num_as:
        r = 1

    elif length < num_as:
        r = 0

    else:
        r = winners_no_ls(length - num_as - 1)

    #print 'winners_no_ls_ending_in_as', length, num_as, 'returning', r
    return r

@shared.Memoize
def winners_no_ls(length):
    #print 'winners_no_ls', length
    s = 0
    for num_as in range(0, 3):
        s +=  winners_no_ls_ending_in_as(length, num_as)
    return s
        
def solve():
    days = 30

    num_winners = winners_no_ls(days)
    for l_day in range(days):
        num_winners += winners_no_ls(l_day) * winners_no_ls(days - l_day - 1)

    return num_winners


