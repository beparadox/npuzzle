""" read solutions to n-puzzle states from the mongodb instance """
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from npuzzle_utils import solution_path_states as sps
import scipy.stats as stats
import sys
from config import DBNAME

def get_collection(dbname=DBNAME, collection='solutions'):
    """get solution nodes from Mongo db instance

    Args:
        dbname:     name of database. Should be 'npuzzle'

        collection: there are a couple different collections. Solutions
        contains the solutions that contain the stats.  Other solutions
        have the state and the solution path.

    Returns:
        solutions:  list of nodes.
    """
    dbcli = MongoClient()
    collection = dbcli[dbname][collection]

    return collection 

def get_solutions_cursor():
    """ Return a cursor to the solutions collection in the npuzzle database"""
    client = MongoClient()
    cursor = client['npuzzle']['solutions'].find()
    return cursor

def get_property(propname, collection):
    """ Get an array of all the values for a particular property of
    solution nodes in the DB
    
    Args: 
        propname: string. name of property
        
    Returns:
        numpy array containing all values of the property defined in propname
        
    Possible properties include:
        state
        path_cost
        hfvalue_path
        added_frontier
        solution
        number_explored
        hfname
        hfvalue
        size"""
    #collection = get_solutions_collection()
    if type(propname) == dict:
        nodes = collection.find({}, propname)
    else:
        nodes = collection.find({}, {propname: 1})
    return np.array([node[propname] for node in nodes])

def read_solutions(arg):
    """ call this when the script is executed from the command line """
    if arg == 1:
        db = 'npuzzle'
        collection = '3puzzle_solutions'
        solutions = read_solutions_db(db, collection)
        for sol in solutions:
            print "state: %s solution: %s" % (str(sol['state']), str(sol['solution']))
        solution_stats()     
    elif arg == 2:
        solution_stats()

if __name__ == '__main__':
    read_solutions(int(sys.argv[1]))
