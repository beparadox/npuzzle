#!/usr/bin/python

""" TODO: comment this properly"""


import sys
import getopt
import read_solutions as rs
import numpy
from scipy import stats

def Usage():
    print "Usage: <%s> -n <int:num_of_states>" % (__name__)
    #return False
    sys.exit(0)

NUM = 1
(options, value) = getopt.getopt(sys.argv[1:], "-n")
for option in options:
    if option[0] == '-n':
        try:
            NUM = int(value[0])
        except ValueError:
            Usage()



class NPuzzleStats(object):
    """
    What stats do we want?
    Max, min, median, mean, std
    State       max, min
    Explored    max, min, media
    Frontier
    hn (for the state)
    path-cost

    Need the dimension
    And the algorithm
    """
    def __init__(self, dim=3, algorithm='astar'):
        self.dim = dim 
        self.algorithm = algorithm
        self.solution_nodes = rs.get_solution_nodes()

    def print_path_nodes(self):
        nodes = self.solution_nodes

        for node in nodes:
            print node
        
    def get_solution_stats(self):
        self.stats = {
                'hn': [],
                'path_cost': [],
                'explored': [],
                'frontier': []
        }


        for node in self.solution_nodes:
            self.stats['hn'].append(node['hn'])

            self.stats['path_cost'].append(node['path_cost'])

            self.stats['explored'].append(node['explored'])

            self.stats['frontier'].append(node['frontier'])

        return self.stats

    def write_stats_file(self, filename):
        fptr = open(filename, 'w')

    def stats_summary(self):
        if hasattr(self, 'stats'):
            totals = self.stats
        else:
            totals = self.get_solution_stats()

        summary = "\n *** Hello, these are the latest statistics for the database:\n"
        summary += '\n{0:12s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}'.format('           ', 'min', 'max', 'mean', 'std', 'median', 'mode')
        for key in totals.keys():
            summary += '\n{0:12s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}'.format(key, str(numpy.min(totals[key])), 
                    str(numpy.max(totals[key])), str(round(numpy.mean(totals[key]), 3)), str(round(numpy.std(totals[key]), 3)), 
                    str(numpy.median(totals[key])), str(stats.mode(totals[key])))

        return summary 

if __name__ == '__main__':
    npstats = NPuzzleStats()
    #print npstats.get_path_nodes()
    #print npstats.print_path_nodes()
    #print npstats.get_solution_stats()
    print npstats.stats_summary()



    
