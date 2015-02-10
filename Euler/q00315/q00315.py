#!/usr/bin/env python

import sys
import itertools
import shared

# Sam and Max are asked to transform two digital clocks into two "digital root" clocks.
# A digital root clock is a digital clock that calculates digital roots step by step.

# When a clock is fed a number, it will show it and then it will start the calculation, showing all the intermediate values until it gets to the result.
# For example, if the clock is fed the number 137, it will show: "137"  "11"  "2" and then it will go black, waiting for the next number.

# Every digital number consists of some light segments: three horizontal (top, middle, bottom) and four vertical (top-left, top-right, bottom-left, bottom-right).
# Number "1" is made of vertical top-right and bottom-right, number "4" is made by middle horizontal and vertical top-left, top-right and bottom-right. Number "8" lights them all.

# The clocks consume energy only when segments are turned on/off.
# To turn on a "2" will cost 5 transitions, while a "7" will cost only 4 transitions.

# Sam and Max built two different clocks.

# Sam's clock is fed e.g. number 137: the clock shows "137", then the panel is turned off, then the next number ("11") is turned on, then the panel is turned off again and finally the last number ("2") is turned on and, after some time, off.
# For the example, with number 137, Sam's clock requires:
# "137"	:	(2 + 5 + 4)  2 = 22 transitions ("137" on/off).
# "11"	:	(2 + 2)  2 = 8 transitions ("11" on/off).
# "2"	:	(5)  2 = 10 transitions ("2" on/off).
# For a grand total of 40 transitions.
# Max's clock works differently. Instead of turning off the whole panel, it is smart enough to turn off only those segments that won't be needed for the next number.
# For number 137, Max's clock requires:
# "137":
# 2 + 5 + 4 = 11 transitions ("137" on)
# 7 transitions (to turn off the segments that are not needed for number "11").
# "11":
# 0 transitions (number "11" is already turned on correctly)
# 3 transitions (to turn off the first "1" and the bottom part of the second "1"; 
# the top part is common with number "2").
# "2"

# :

# 4 transitions (to turn on the remaining segments in order to get a "2")
# 5 transitions (to turn off number "2").
# For a grand total of 30 transitions.
# Of course, Max's clock consumes less power than Sam's one.
# The two clocks are fed all the prime numbers between A = 10^7 and B = 2*10^7. 
# Find the difference between the total number of transitions needed by Sam's clock and that needed by Max's one.



#  top, nw, ne, middle, sw, se, bottom
# 7: top, nw, ne, se  (yes, 4!)

expected = 13625242

OFF = -1
lights = {
    OFF: (0, 0, 0, 0, 0, 0, 0,),
    0: (1, 1, 1, 0, 1, 1, 1,),
    1: (0, 0, 1, 0, 0, 1, 0,),
    2: (1, 0, 1, 1, 1, 0, 1,),
    3: (1, 0, 1, 1, 0, 1, 1,),
    4: (0, 1, 1, 1, 0, 1, 0,),
    5: (1, 1, 0, 1, 0, 1, 1,),
    6: (1, 1, 0, 1, 1, 1, 1,),
    7: (1, 1, 1, 0, 0, 1, 0,),
    8: (1, 1, 1, 1, 1, 1, 1,),
    9: (1, 1, 1, 1, 0, 1, 1,),
}


move_for_digits = {}
for k1, v1 in lights.items():
    for k2, v2 in lights.items():
        move_for_digits[(k1,k2)] = sum((1 for i in range(len(v1)) if v1[i] != v2[i]))

def digits(n):
    result = []
    while n > 0:
        (n, digit) = divmod(n, 10)
        result.append(digit)
    return result

def digital_root(n):
    return sum((d for d in digits(n)))

def count_moves_for_number(f, to):
    result = 0
    f_digits = digits(f)
    to_digits = digits(to)
    for i in range(len(to_digits)):
        result += move_for_digits[(f_digits[i], to_digits[i])]
    for i in range(len(to_digits), len(f_digits)):
        result += move_for_digits[f_digits[i], OFF]
    return result

def count_moves_to_zero(n):
    result = 0
    while n > 0:
        (n, digit) = divmod(n, 10)
        result += move_for_digits[(digit, OFF)]
    return result

@shared.Memoize
def sam_solve(n):
    one_number_count =  count_moves_to_zero(n)
    new_n = digital_root(n)
    while new_n != n:
        #print ' ', new_n, n
        one_number_count += count_moves_to_zero(new_n)
        n, new_n = new_n, digital_root(new_n)
    return 2 * one_number_count

@shared.Memoize
def max_solve(n):
    one_number_count = 0
    new_n = digital_root(n)
    while new_n != n:
        #print ' ', new_n, n
        one_number_count += count_moves_for_number(n, new_n)
        n, new_n = new_n, digital_root(new_n)
    one_number_count +=  count_moves_to_zero(n)
    return one_number_count

def solve():


    result = 0
    min = 10**7
    max = 2*10**7


    #print max_solve(137), sam_solve(137)
    #return
    g = shared.prime_generator(max)

    generator = itertools.dropwhile(lambda n: n < min, g)
    for p in generator:
        # print p
        result += count_moves_to_zero(p) # sam takes twice this, max once
        n = digital_root(p)
        result -= count_moves_for_number(p, n) # max

        # add their costs starting from the digital root of p
        max_result = max_solve(n)
        sam_result = sam_solve(n)
        result += (sam_result - max_result)
        
#     max_result = max_solve(19999999)
#     sam_result = sam_solve(19999999)
#     print 'max', max_result
#     print 'sam', sam_result
#     result += (sam_result - max_result)
    return result


