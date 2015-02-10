#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

# The rules for writing Roman numerals allow for many ways of writing each number
# (see FAQ: Roman Numerals).
# However, there is always a "best" way of writing a particular number.
# 
# For example, the following represent all of the legitimate ways of writing the number
# sixteen:
# 
# IIIIIIIIIIIIIIII
# VIIIIIIIIIII
# VVIIIIII
# XIIIIII
# VVVI
# XVI
# 
# The last example being considered the most efficient, as it uses the least number of numerals.
# 
# The 11K text file, roman.txt (right click and 'Save Link/Target
# As...'), contains one thousand numbers'written in valid, but not
# necessarily minimal, Roman numerals; that is, they are arranged in
# descending units and obey the subtractive pair rule (see FAQ for the
# definitive rules for this problem).
# 
# Find the number of characters saved by writing each of these in
# their minimal form.
# 
# Note: You can assume that all the Roman numerals in the file contain
# no more than four consecutive identical units.

roman_to_value = {
    'M': 1000,
    'CM': 900,
    'D': 500,
    'CD': 400,
    'C': 100,
    'XC': 90,
    'L': 50,
    'XL': 40,
    'X': 10,
    'IX': 9,
    'V': 5,
    'IV': 4,
    'I': 1
    }
value_to_roman = {}
for (r, v) in roman_to_value.items():
    value_to_roman[v] = r
values = value_to_roman.keys()
values.sort()
values.reverse()
romans = [value_to_roman[v] for v in values]

def convert_roman_to_arabic(r):
    value = 0
    while len(r) > 0:
        for prefix in romans:
            if r.startswith(prefix):
                value += roman_to_value[prefix]
                r = r[len(prefix):]
    return value

def convert_arabic_to_roman(a):
    roman = ''
    for value in values:
        quot, rem = divmod(a, value)
        roman += value_to_roman[value] * quot
        a = rem
    return roman
            
            

def solve(romans):
    return sum((len(roman) - len(convert_arabic_to_roman(convert_roman_to_arabic(roman))) for roman in romans))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    romans = [line.strip() for line in file('roman.txt')]

    start = datetime.datetime.now()
    result = solve(romans)
    end = datetime.datetime.now()
    print result
    assert 743 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

