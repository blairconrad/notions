#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared


# Let D_(0) be the two-letter string "Fa". For n>=1, derive D_(n) from D_(n-1) by the string-rewriting rules:

# "a" -> "aRbFR"
# "b" -> "LFaLb"
#
# Thus, D_(0) = "Fa", D_(1) = "FaRbFR", D_(2) = "FaRbFRRLFaLbFR", and so on.
#
# These strings can be interpreted as instructions to a computer
# graphics program, with "F" meaning "draw forward one unit", "L"
# meaning "turn left 90 degrees", "R" meaning "turn right 90 degrees",
# and "a" and "b" being ignored. The initial position of the computer
# cursor is (0,0), pointing up towards (0,1).
#
# Then D_(n) is an exotic drawing known as the Heighway Dragon of
# order n. For example, D_(10) is shown below; counting each "F" as
# one step, the highlighted spot at (18,16) is the position reached
# after 500 steps.
#
# "a" -> "aRbFR"
# "b" -> "LFaLb"
#
# What is the position of the cursor after 10^(12) steps in D_(50) ?
# Give your answer in the form x,y with no spaces.



north = (0,1)
east = (1,0)
west = (-1, 0)
south = (0,-1)

class R:
    def __call__(self, position, direction):
        return (position,
                { north: east,
                  east: south,
                  south: west,
                  west: north,
                 }[direction])

    def num_steps(self):
        return 0

    def __repr__(self):
        return 'R'

class L(R):
    def __call__(self, position, direction):
        return (position,
                { north: west,
                  east: north,
                  south: east,
                  west: south,
                 }[direction])

    def __repr__(self):
        return 'L'

class F:
    def __call__(self, position, direction):
        return ((position[0] + direction[0], position[1] + direction[1]),
                direction)

    def num_steps(self):
        return 1

    def __repr__(self):
        return 'F'

def num_steps_for_move(depth):
    if depth == 0:
        return 0
    return 2 * num_steps_for_move(depth-1) + 1


cached_moves = {}

class a:
    def __init__(self, depth):
        self.type = 'a'
        self.depth = depth

    def expand(self):
        return [a(self.depth-1), R(), b(self.depth-1), F(), R()]

    def __call__(self, position, direction):
        if self.depth == 0:
            return (position, direction)

        if (self.type, self.depth, direction) in cached_moves:
            move = cached_moves[(self.type, self.depth, direction)]
            #print ' ' * self.depth, 'move for', self, direction, 'is', move
            new_position, new_direction = move
        else:
            # not cached! expand
            #print ' ' * self.depth, self, direction, 'is not cached'
            new_direction = direction
            script = self.expand()
            #print ' ' * self.depth, 'script =', script
            new_position = (0,0)
            for move in script:
                new_position, new_direction = move(new_position, new_direction)
            #print ' ' * self.depth, 'caching', self, direction, 'as', new_position, new_direction
            cached_moves[(self.type, self.depth, direction)] = (new_position, new_direction)
            
        position = (position[0] + new_position[0], position[1] + new_position[1])
        return position, new_direction

    def __repr__(self):
        return self.type + '(' + str(self.depth) + ')'

    def num_steps(self):
        return num_steps_for_move(self.depth)
    
class b(a):
    def __init__(self, depth):
        self.depth = depth
        self.type = 'b'

    def expand(self):
        return [L(), F(), a(self.depth-1), L(), b(self.depth-1)]


def move(position, direction, num_steps, script):
    while num_steps > 0:
        #print script
        next_move = script.pop(0)
        n =  next_move.num_steps()
        if n <= num_steps:
            (position, direction) = next_move(position, direction)
            num_steps -= n
        else:
            #print 'need ', num_steps, 'steps, but will move', n, 'expanding'
            script[0:0] = next_move.expand()
            continue
    return position

def solve(n):
    position = (0,0)
    direction = north

    #print move(position, direction, 8, [F(), a(3)])
    return ','.join(map(str, move(position, direction, 10**12, [F(), a(50)])))



def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) == 0:
        n = 50
    else:
        n = int(args[0])

    start = datetime.datetime.now()
    result = solve(n)
    end = datetime.datetime.now()
    print result
    assert '139776,963904' == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())

