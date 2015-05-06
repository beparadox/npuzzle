""" practice with the NPuzzle Problem"""
import sys
import NPuzzleProblem as NPP 
import NPuzzleHeuristics as NPH
import search
from Queues import FIFOQueue
from npuzzle_utils import solution_path_states, invert_solution 
from pymongo import MongoClient
from write_solutions import write_solutions, write_solutions2

def print_features(node, nph):
    actions = invert_solution(node.solution())
    path = solution_path_states(node.state, actions)
    print "state = " + str(node.state)
    if hasattr(node.parent, 'parent'):
        print "parent = " + str(node.parent.state)
        print path[1] == node.parent.state
    else:
        print "parent = None"
    print "action = " + str(node.action)
    print "path_cost = " + str(node.path_cost)

    print "solution =" + str(actions)
    print "solution state path: " + str(path)

def print_search_tree(node, nph):
    queue = FIFOQueue()
    queue.extend([node.root_node()])
    while queue:
        node = queue.pop() 
        print_features(node, nph)
        if hasattr(node, 'children'):
            children = node.children
            queue.extend(children)
        else:
            return

def afunc():
    """ random stuff"""
    actions = node.solution()
    rev_actions = invert_solution(actions)
    print node.state
    print rev_actions
    print solution_path_states(node.state, rev_actions)

def bfunc():
    """ """ 
    initial = tuple([1,2,3,4])
    goal = tuple([2,1,3,4])

    initial = tuple(range(1, 10))
    goal = tuple([2, 1, 3, 4, 5, 6, 7, 8, 9])
    npp = NPP.NPuzzleProblem(initial, goal, dim=3)
    nph = NPH.NPuzzleHeuristics()
    node = search.build_search_tree(npp, depth=5)
    #print_features(node)
    print_search_tree(node, nph)

def sol1(dim, depth):
    npp = NPP.get_unsolvable_problem(dim=dim)
    func = write_solutions(dim=dim)
    search.build_search_tree(npp, func, depth=depth)

def sol2(dim, depth):
    npp = NPP.get_unsolvable_problem(dim=dim)
    nodes = search.build_search_tree2(npp, depth=depth)
    write_solutions2(nodes, dim=dim)

def main(arg):
    """ run this from command line

    We could change the below to this:
      npp = NPP.get_unsolvable_problem(dim=DIM)
      nodes = search.build_search_tree(npp, depth=31)
      write_solutions(nodes, dim=DIM)

      It would require adding all nodes generated in
      build_search_tree to a list and returning the list
    """
    DIM = 3 
    DEPTH = 31 
    if arg:
        print "running sol1..."
        sol1(DIM, DEPTH)
    else:
        print "running sol2..."
        sol2(DIM, DEPTH)

if __name__ == "__main__":
    main(sys.argv[1:])
