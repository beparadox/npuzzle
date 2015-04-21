""" get_solutions.py

Get solutions to valid n-puzzle states. 
There are two options:
either select random states using get_random_solutions
provide a state to get_solution,
or a list of states to get_solutions

@author:     Bambridge E. Peterson
@updated:    10/23/14 """


from search import astar_search, idastar_search, build_search_tree
from NPuzzleProblem import NPuzzleProblem, get_unsolvable_problem
from NPuzzleHeuristics import NPuzzleHeuristics
from generate_init_states import generate_init_states as gistates
import sys
import getopt

def usage():
    """ print usage to command line """
    print "usage: <%s> -n <int:num_of_states>" % (__name__)
    sys.exit(0)

def get_random_solutions(num, dim=3, heurfun='md', stats=False):
    """ get solutions to num of random initial states"""
    random_states = gistates(num)
    solutions = []

    for state in random_states:
        # NPuzzleProblem takes inital state, goal and optional dim
        npp = NPuzzleProblem(state, tuple(range(1, len(state) + 1)),\
                dim=dim)
        nph = NPuzzleHeuristics(hnfun=heurfun)
        solutions.append(astar_search(npp, heurfun=nph.hnfun,\
                stats=stats))

    return solutions

def get_solution(state, dim=3, heurfun='md', stats=False):
    """ Get a solution for a possible state """
    goal = tuple(range(1, dim*dim + 1))
    npp = NPuzzleProblem(state, goal, dim=dim)
    nph = NPuzzleHeuristics(hnfun=heurfun, dim=dim)

    if dim == 2 or dim == 3:
        solution = astar_search(npp, heurfun=nph.hnfun, stats=stats)
    elif dim == 4:
        solution = idastar_search(npp, heurfun=nph.hnfun, stats=stats)

    if stats:
        setattr(solution[0], 'hfname', nph.hfname)
    else:
        setattr(solution, 'hfname', nph.hfname)

    return solution

def get_solutions(states, dim=3, heurfun='md', stats=False):
    """ Get solutions for a list of possible states """
    solutions = []

    for state in states:
        solutions.append(get_solution(state, dim, heurfun, stats))

    return solutions

def get_statnodes(solutions):
    """ solutions should be a list of solution nodes for various initial
        states of the puzzle

        the nodes here represent some basic statistics for the solution
        to the given intial state. Include:

        hfname - name of the heuristic function used
        hfn - the output of the heuristic function for the initial state
        hn_path - the output of the heuristic function for each of the
          intermediate states on the path from the state to the goal
        state - the starting state
        solution -  list of actions taken to get from start to the goal nde
        frontier - number of items added to the frontier
        explored - number of states added to the explored set
        path_cost - depth of the state from the goal node
        """
    solution_nodes = []
    for goalnode, explored, frontier in solutions:
        node = {}
        node['state'] = goalnode.root_node().state
        node['size'] = len(node['state'])
        node['path_cost'] = goalnode.path_cost
        node['solution'] = goalnode.solution()

        node['hfname'] = goalnode.hfname
        node['hfvalue'] = goalnode.root_node().h
        node['hfvalue_path'] = goalnode.hn_path()

        # total number added to the explored set before goal node was found
        node['number_explored'] = explored
        # total number added to the frontier before goal node was found
        node['added_frontier'] = frontier
        solution_nodes.append(node)

    return solution_nodes

def main():
    """ For when the file is called itself, not as a module.
    Right now, simply prints a list of random states"""
    num = 1
    (options, value) = getopt.getopt(sys.argv[1:], "-n")
    for option in options:
        if option[0] == '-n':
            try:
                num = int(value[0])
            except ValueError:
                usage()

    states = list(gistates(dim=3, num=num))
    print "printing states..."
    for state in states:
        print state

    print "Getting solutions..."
    for state in states:
        node = get_solution(state, stats=True)
        print node
        print get_statnodes([node])

    print "building search tree..."
    tree = gs_search_tree(2)
    print tree

if __name__ == '__main__':
    main()
