"""This file is used to generate random, allowable instances
of a n-puzzle with dimension = dim.

Uses the A* algorithm to solve these states, as well as the
manhattan distance function

Command line arguments:
  -n <int>: specify the number of unique states you want to
  generate

  -d <int>: specify the dimension of the puzzle

@author: Bambridge E. Peterson
@email:  bambridge.peterson@gmail.com
"""
from npuzzle_utils import count_inversions_n2, acceptable_state
from copy import copy
from heuristics import NPuzzleHeuristics
import sys
import getopt
from random import shuffle

def usage(msg):
    """ print usage to command line"""
    print str(msg)
    print "usage: <%s> -n <int:num_of_states> -d <int: dimension>" % (__name__)
    #return False
    sys.exit(0)

def generate_init_states(num=1, dim=3):
    """ Generate num valid states for the n-puzzle (n = dim^2 - 1)
    Args:  
      dim - dimension of the n-puzzle. 2, 3, 4, or 5 are the most common values
      
      num - number of states to return.
    Returns: returns a set of length num containing tuples of integers,
      which represent randomly generated
      allowable initial states

    @desc:
        An allowable state for an n-puzzle is one in which:
           number of inversions in the n + 1 elements
           +
           the manhattan distance of the
           blanks space from its position in the goal configuration
           = an even integer.
    For example, a matrix of the form
        1 2 3
        4 5 6
        7 9 8
    (where 9 represents the blank space)
    can be mapped to a list or an array as:
    [1, 2, 3, 4, 5, 6, 7, 9, 8].
    There is one inversion in this list of number,
    and the blanks space (9) is one position from its home base.
    1 + 1 = 2 ;)
    """
    #ns = 0
    init_states = set()
    size = dim * dim
    current_state = range(1, size + 1)

    # index of current iteration
    nizzle = 0
    # shuffle the current state
    shuffle(current_state)
    while nizzle < num:
        shuffle(current_state)
        while not acceptable_state(current_state):
            shuffle(current_state)
        if tuple(current_state) not in init_states:
            init_states.add(tuple(current_state))
        nizzle += 1

    return init_states

def main():
    """ run when this file is being called. prints a set of random
    states to the command line """
    num = 1
    dim = 3
    try:
        (options, leftover) = getopt.getopt(sys.argv[1:], "-n:-d:")
    except getopt.GetoptError as err:
        print usage(err)

    for option in options:
        #print value
        if option[0] == '-n':
            try:
                num = int(option[1])
            except ValueError:
                usage('no value given for -n option')
        elif option[0] == '-d':
            try:
                dim = int(option[1])
            except ValueError:
                usage('no value give for -d option')

    if len(leftover) > 0:
        print "leftover args: " + str(leftover)

    print generate_init_states(num, dim)

if __name__ == '__main__':
    main()
