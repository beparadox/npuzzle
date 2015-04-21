"""How to print all possible states for an n-puzzle
Use breadth_first_search to generate ALL possible states for the 8puzzle
"""
import search
import sys
import getopt
from Problem import NPuzzleProblem

def usage():
    """ print modoule usage to the command line if run with incorrect
    parameters"""
    print "Usage: <%s> -d <int:dimension of npuzzle> " % (__name__)
    sys.exit(0)


def invalid_init_state(dim=3):
    """ create an invalid initial state. An invalid initial state is one
    in which the city block distance plus the number of inversions"""
    invalid_state = range(1, dim*dim + 1)
    tmp = invalid_state[0]
    invalid_state[0] = invalid_state[1]
    invalid_state[1] = tmp
    invalid_state = tuple(invalid_state)

    return invalid_state

def get_all_states(dim=3):
    """ In order to get all possible states for an npuzzle, you can simply pass
    any valid n-puzzle state as the initial state, and an invalid n-puzzle
    state as the goal; the
    """
    # goal state should be a tuple of the the first dim*dim positive intgers
    goal_state = tuple(range(1, dim*dim + 1))

    invalid_state = invalid_init_state(dim)
    # invalid_state is easy to produce.
    npp = NPuzzleProblem(invalid_state, goal_state)

    allstates = search.breadth_first_search(npp)

    return allstates

def main():
    """ to be run when script is run from the command line"""
    dim = 3
    (options, values) = getopt.getopt(sys.argv[1:], "-d")
    for option in options:
        print option
        if option[0] == '-d':
            try:
                dim = int(values[0])
            except ValueError:
                usage()
    print invalid_init_state(dim)

if __name__ == '__main__':
    main()
