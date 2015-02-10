#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def digits(n):
    return (int(c) for c in str(n))

def extend(numbers):
    new_numbers = set()
    for number in numbers:
        for start in range(len(number)):
            if number[start] != 0:
                break
        for i in range(start, len(number)):
            new_number = number[:]
            new_number = number[:i] + (number[i]+1,) + (number[i+1:])
            new_numbers.add(new_number)
    return new_numbers
            
factorials = [1]
for i in range(1,10):
    factorials.append(i*factorials[-1])

def get_string(number):
    s = ''
    for i in range(len(number)):
        s += str(i) * number[i]
    return s

def get_total(number):
    return sum((number[i] * factorials[i] for i in range(len(number))))

def solve(n):
    totals = set()
    
    numbers = set()
    for i in range(10):
        number = ((0,)*10)[:]
        number = number[:i] + (number[i]+1,) + (number[i+1:])
        numbers.add(number)

    for i in range(2, n):
        numbers = extend(numbers)
        for number in numbers:
            total = get_total(number)
            if ''.join(sorted(str(total))) == get_string(number):
                #print get_string(number), total, number
                totals.add(total)
    return sum(totals)
        
def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 8
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert 40730 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

