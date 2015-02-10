#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

alphabet = 'abcdefghijklmnopqrstuvwxyz'
allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789().,\'";:?!'

def solve(ords):
    # this could be a LOT faster if we evaluated the ciphertext and key character-by-character, but
    # it's good enough for now
    for k1 in alphabet:
        for k2 in alphabet:
            for k3 in alphabet:
                key = (ord(k1), ord(k2), ord(k3))
                plaintext = ''.join(chr(ords[i] ^ key[i%3]) for i in range(len(ords)))
                #print plaintext
                plaintext_is_good = True
                
                for c in plaintext:
                    if c not in allowed_chars:
                        plaintext_is_good = False
                        break
                if plaintext_is_good:
                    return sum((ord(c) for c in plaintext))


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    f = file('cipher1.txt')
    ords = [int(o, 10) for o in f.read().split(',')]

    start = datetime.datetime.now()
    result = solve(ords)
    end = datetime.datetime.now()
    print result
    assert 107359 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

