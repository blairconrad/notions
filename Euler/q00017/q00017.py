#!/usr/bin/env python

import sys

units_map = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    }
tens_map = {
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety',
    }
hundred = 'hundred'
thousand = 'thousand'
and_symbol = 'and'

def number_to_word(n):
    if n == 1000:
        return 'one' + 'thousand'

    phrase = ''
    units = n % 100
    if units in units_map:

        phrase += units_map[units]
    else:
        tens = (n % 100 / 10) * 10
        if tens in tens_map:
            phrase += tens_map[tens]
            units =  n % 10
            if units in units_map:
                phrase += units_map[units]

    if len(phrase) > 0 and n > 100:
        phrase += and_symbol

    hundreds = ( n / 100 ) % 10
    #print 'hundreds',  hundreds
    if hundreds in units_map:
        phrase += units_map[hundreds] + hundred


    return phrase

def solve(n):
    #for n in range(1, n+1):
    #    print n, number_to_word(n)
    return sum((len(number_to_word(i)) for i in range(1, n+1)))

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 1000
    else:
        n = int(args[0])

    assert 21124 == solve(n)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

