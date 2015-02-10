#!/usr/bin/env python

import sys
sys.path.append('..')
import shared


def solve(alphabet, ordinal):
    result = ''

    mult = shared.factorial(len(alphabet))

    while len(alphabet) > 1:
        mult /= len(alphabet)
        #print ordinal, mult, alphabet
        (index, ordinal) = divmod(ordinal, mult)
        #print ordinal, mult, index, alphabet
        
        
        result += alphabet[index]
        alphabet = alphabet[:index] + alphabet[index+1:]

    result += alphabet[0]
    return result

    
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        alphabet = list('0123456789')
        ordinal = 1000000
    else:
        alphabet = list(args[0])
        ordinal = int(args[1])

    ordinal -= 1 # specified 1-based, we'll count 0-based
    result = solve(alphabet, ordinal)
    print result
    assert '2783915460' == result

    return 0


if __name__ == '__main__':
    sys.exit(main())

