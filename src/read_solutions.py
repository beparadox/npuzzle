#!/usr/bin/python
""" read solutions to n-puzzle states from the mongodb instance """
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from npuzzle_utils import solution_path_states as sps
import scipy.stats as stats
import sys

def read_solutions(dbname, collection):
    """get solution stat nodes from Mongo db """
    dbcli = MongoClient()
    solutions = dbcli[dbname][collection].find()

    return solutions

def get_collection(dbname, collection):
    """ get a collection from the db"""
    client = MongoClient()
    return client[dbname][collection]

def print_stats(name, coll):
    print "****** %s ******" % name
    print "min: " + str(np.round(np.min(coll), 2))
    print "max: " + str(np.round(np.max(coll), 2))
    print "mean: " + str(np.round(np.mean(coll), 2))
    print "median: " + str(np.round(np.median(coll), 2))
    print "std: " + str(np.round(np.std(coll), 2))
    print ""

def solution_stats():
    """
    get the solution stats here

    What stats do we want?

    min, max, mean, median, mode, std for the:
    number_explored
    added_frontier
    path_cost
    hfvalue

    covariance matrix of path costs to number explored and added to frontier

    number of inversions for each state
    """
    client = MongoClient()
    solutions = client['npuzzle']['solutions']

    pcost = solutions.aggregate([{"$group": {"_id": "$path_cost", "total": {"$sum": 1}}}])
    pcost_x = np.array([keys['_id'] for keys in pcost['result']])
    pcost_y = np.array([keys['total'] for keys in pcost['result']])

    hfvals = solutions.aggregate([{"$group": {"_id": "$hfvalue", "total": {"$sum": 1}}}])
    hfvals_x = np.array([keys['_id'] for keys in hfvals['result']])
    hfvals_y = np.array([keys['total'] for keys in hfvals['result']])

    count = solutions.count()
    num_explored = np.array(np.zeros((1, count)))
    add_frontier = np.array(np.zeros((1, count)))
    path_costs = np.array(np.zeros((1, count)))
    hfvalues = np.array(np.zeros((1, count)))

    nodes = solutions.find()
    for ind in range(0, count):
        num_explored[0][ind] = nodes[ind]['number_explored']
        add_frontier[0][ind] = nodes[ind]['added_frontier']
        path_costs[0][ind] = nodes[ind]['path_cost']
        hfvalues[0][ind] = nodes[ind]['hfvalue']

    print_stats("number_explored", num_explored)

    print_stats("added to frontier", add_frontier)

    print_stats("path costs", path_costs)

    print_stats("hfvalues", hfvalues)

def main(arg):
    """ call this when the script is executed from the command line """
    if arg == 1:
        db = 'npuzzle'
        collection = '3puzzle_solutions'
        solutions = read_solutions(db, collection)
        for sol in solutions:
            print sol['state'], sol['solution']
    elif arg == 2:
        solution_stats()

if __name__ == '__main__':
    main(int(sys.argv[1]))
