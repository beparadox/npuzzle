""" Write all possible states to a .txt file
get_all returns all possible states for the
"""
from all_npuzzle_states import get_all_states
from getopt import getopt
from pymongo import MongoClient

def write_states(write, dim=3):
    """ write all states to file"""
    if write == 'mongo':
        client = MongoClient()
        database = client['npuzzle']

        if dim == 2:
            coll_name = '3puzzle_solutions'
        elif dim == 3:
            coll_name = '8puzzle_solutions'
        elif dim == 4:
            coll_name = '15puzzle_solutions'
        else:
            coll_name = '24puzzle_solutions'

        collection = database[coll_name]

        allstates = get_all_states()

        collection.insert({'allstates': allstates})
    else:
        allstates = get_all_states()

        fptr = open('../data/8puzzle_states.txt', 'w')

        for state in allstates:
            fptr.write(str(state))
            fptr.write('\n')

def main():
    """ called when the file itself is executed"""
    (options, values) = getopt.getopt(sys.argv[1:], "-d")
    for option in options:
        #print value
        if option[0] == '-s':
            try:
                write_states('mongo')
            except ValueError:
                pass

if __name__ == '__main__':
    main()
