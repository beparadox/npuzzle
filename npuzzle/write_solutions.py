"""
Write solutions to allowable npuzzle states to the npuzzle MongoDB
"""
import read_allstates
from get_solutions import get_solutions, get_statnodes
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
from getopt import getopt, GetoptError
from npuzzle_utils import expand_search_tree, invert_solution, get_search_tree

def get_and_write_solutions_mongodb(**kwargs):
    #filename, num, dim=3, dbname='npuzzle', heurfun='md'):
    """ States is a list of tuples representing acceptable random
    starting states (which you can get from generate_init_states) that you want
    to get the solution nodes for.
    For the 8-Puzzle, we eventually want to write all
    181,440 solutions using the
    AStar search algorithm. However, we don't want duplicates.
    All 181, 440 states
    have already been written to a file, 8puzzle_states.txt
    found in the 'data' folder.
    Use generate_init_states.py to randomly
    generate init states or read_states.py
    to get a list of random starting states
    """
    try:
        # get all possible states from the data file
        all_states = read_allstates.from_txt(kwargs['filename'])
        client = MongoClient()
        db_collection = client[kwargs['dbname']][kwargs['collection']]
        cnt = db_collection.count()
        solutions = get_solutions(all_states[cnt: cnt + kwargs['num']], dim=kwargs['dim'],\
                heurfun=kwargs['heurfun'],\
                stats=True)
        nodes = get_statnodes(solutions)
        print "Writing solutions to the following states to the database..."
        for node in nodes:
            print node['state']
        db_collection.insert(nodes)
    except ValueError:
        print "In write_mongodb. Invalid dimension given; dim must be\
                2, 3, 4, or 5"
        return
    except TypeError:
        print len(solutions)
    except ConnectionFailure as cfail:
        print "connection failure: %s" % cfail

def write_solutions(nodes, dim=3):
    """
    Use this to write states and solution paths to the database

    Args:
        nodes: a list of solution node of type problem.Node
        
    """
    collections = {
        2: '3puzzle_solutions',
        3: '8puzzle_solutions',
        4: '15puzzle_solutions',
        5: '24puzzle_solutions'
        }
    try:
        client = MongoClient()
        collection = client['npuzzle'][collections[dim]]

        for node in nodes:
            collection.insert({
                "state": node.state,
                "solution": invert_solution(node.solution()) 
            })

        client.close()
    except KeyError as kerr:
        print "Error in write_solutions: dim has to be 2, 3, 4 or 5"
        return False
    except ConnectionFailure as cfail:
        print "connection failure: %s" % cfail
        return False

def usage():
    """ print usage to command line"""
    print "usage: <%s> -n <int:num_of_states to write>\
    --dim=<int:d dimension for n-puzzle --db=<database name>" % (__name__)
    sys.exit(0)

def main():
    """ run this when file is directly executed"""
    args = {
        'dbname': 'npuzzle',
        'num': 100,
        'dim': 3,
        'filename': 'data/8puzzle_states.txt',
        'collection': 'solutions',
        'heurfun': 'md'
        }
    try:
        if len(sys.argv[1:]) != 0:
            options = getopt(sys.argv[1:], "-n:",\
                    ['dim=', 'db=', 'filename=', 'collection=', 'heurfun='])
            for option in options[0]:
                if option[0] == '-n':
                    args['num'] = int(option[1])
                elif option[0] == '--dim':
                    args['dim'] = int(option[1])
                elif option[0] == '--db':
                    args['dbname'] = option[1]
                elif option[0] == '--collection':
                    args['filename'] = option[1]
                elif option[0] == '--heurfun':
                    args['heurfun'] = option[1]
                else:
                    args['collection'] = option[1]

        get_and_write_solutions_mongodb(**args)
    except GetoptError as err:
        print err
        usage()
    except ValueError as err:
        print "ValueError: %s" % err
        usage()
    except IOError as err:
        print "Unable to open file %s" % args['filename']

if __name__ == '__main__':
    main()
