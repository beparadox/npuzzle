""" module for printing and writing solution stats from the database
@package: npuzzle
"""
import sys
import getopt
from read_solutions import get_solutions_collection, get_solutions_cursor 
import numpy as np
from scipy.stats import mode 

def print_stats(name, coll):
    """  print stats out to the command line.

    Args:
        name: String. The name of the statistic we're
        printing features of.

        coll:
    
    """
    print "****** %s ******" % name
    print "min: " + str(np.round(np.min(coll), 2))
    print "max: " + str(np.round(np.max(coll), 2))
    print "mean: " + str(np.round(np.mean(coll), 2))
    print "median: " + str(np.round(np.median(coll), 2))
    print "std: " + str(np.round(np.std(coll), 2))
    print ""

def get_stat():
    """ get a statistic for a particular feature"""


def stats_summary(stats):
    """ return a string that summarizes statistics from the database
    
    Args:
        stats: a dictionary of np.arrays
    
    Returns:
        summary: a string containing a summary of the statistics given
        
    """
    summary = "\n *** Latest statistics for the database:\n"
    summary += '\n{0:12s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}'.format('           ', 'min', 'max', 'mean', 'std', 'median', 'mode')

    for key in stats.keys():
        summary += '\n{0:12s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}'.format(key, 
                str(np.min(stats[key])), 
                str(np.max(stats[key])), 
                str(round(np.mean(stats[key]), 3)), 
                str(round(np.std(stats[key]), 3)), 
                str(np.median(stats[key])), 
                str(mode(stats[key])))

    return summary 

def get_path_distribution(cursor, name):
    """ Get the distribution functions for the path cost
    and heuristic function values
        Args:
            cursor: database cursor for the appropriate database and collection

            name:
    
    """
    name = '$' + name 
    prop = cursor.aggregate([{"$group": {"_id": name, "total": {"$sum": 1}}}])
    prop_x = np.array([keys['_id'] for keys in prop['result']])
    prop_y = np.array([keys['total'] for keys in prop['result']])

    return (prop_x, prop_y)


def get_stat_arrays(solutions):
    """ Get a dict whose keys are the name of a particular
    property of the solution nodes for a given state.

    Returns:
        dictionary of stats

    Properties are as follows:
        num_explored: number of nodes explored in the search for the
          solution state

        add_frontier:  nodes added to the frontier while searching for
          the solution state
        
        path_cost: path cost of the solution state
        hfvalue:   value of the heuristic function for the state
    """
    count = solutions.count()
    stats = {
        'num_explored': np.array(np.zeros((1, count))),
        'add_frontier': np.array(np.zeros((1, count))),
        'path_costs': np.array(np.zeros((1, count))),
        'hfvalues': np.array(np.zeros((1, count)))
        }

    for ind in range(0, count):
        stats['num_explored'][0][ind] = solutions[ind]['number_explored']
        stats['add_frontier'][0][ind] = solutions[ind]['added_frontier']
        stats['path_costs'][0][ind] = solutions[ind]['path_cost']
        stats['hfvalues'][0][ind] = solutions[ind]['hfvalue']

    return stats

def solution_stats():
    """ This is called if this module is executed from the command line"""
    print "in solution_stats.py"
    solutions = get_solutions_collection()
    nodes = solutions.find().limit(5)
    stats = get_stat_arrays(nodes)
    for key in stats.keys():
        print_stats(key, stats[key])

if __name__ == '__main__':
    solution_stats()
