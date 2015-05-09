"""
@module: search.py

@desc: This is taken from the code written for the textbook
Artificial Intelligence: A Modern Approach
 url: http://aima-python.googlecode.com/svn/trunk/search.py
"""

from queues import Stack, FIFOQueue, PriorityQueue
from problem import Node
import sys

def if_(test, result, alternative):
    """Like C++ and Java's (test ? result : alternative), except
    both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result):
            return result()
        else:
            return result
    else:
        if callable(alternative):
            return alternative()
        else:
            return alternative

def memoize(fnc, slot=None):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, store results in a dictionary."""
    if slot:
        def memoized_fn(obj, *args):
            """return the attribute stored on object,
            or calculate it"""
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fnc(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            """ create slot cache to store calculations """
            if not memoized_fn.cache.has_key(args):
                memoized_fn.cache[args] = fnc(*args)
            return memoized_fn.cache[args]
        memoized_fn.cache = {}

    return memoized_fn

#_____________________________________________________________________________
# Uniformed search
#_____________________________________________________________________________
def tree_search(problem, frontier):
    """Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Don't wrry about repeated paths to a state. [Fig. 3.7]"""
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def graph_search(problem, frontier, stats=False):
    """Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    If two paths reach a state, only use the first one. [Fig. 3.7]"""
    frontier.append(Node(problem.initial))
    explored = set()
    numexp = 0
    numfron = 0
    while frontier:
        node = frontier.pop()

        if problem.goal_test(node.state):
            if stats:
                return node, numexp, numfron
            else:
                return node
        explored.add(node.state)

        if stats:
            numexp += 1
            toadd = [child for child in node.expand(problem)\
                        if child.state not in explored\
                        and child not in frontier]
            numfron += len(toadd)
            frontier.extend(toadd)
        else:
            frontier.extend(child for child in node.expand(problem)
                            if child.state not in explored
                            and child not in frontier)

    return None

def breadth_first_tree_search(problem):
    "Search the shallowest nodes in the search tree first."
    return tree_search(problem, FIFOQueue())

def depth_first_tree_search(problem):
    "Search the deepest nodes in the search tree first."
    return tree_search(problem, Stack())

def depth_first_graph_search(problem, stats=False):
    "Search the deepest nodes in the search tree first."
    return graph_search(problem, Stack(), stats=stats)

def breadth_first_search(problem, stats=False):
    "[Fig. 3.11]"
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node

    frontier = FIFOQueue()
    frontier.append(node)
    explored = set()
    numexp = 0
    numfron = 0
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        numexp += 1
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    if stats:
                        return (child, numexp, numfron)
                    else:
                        return child
                frontier.append(child)
                numfron += 1
    return explored, node

def best_first_graph_search(problem, fun, stats=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    memfun = memoize(fun, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(order='min', f=memfun)
    frontier.append(node)
    explored = set()
    number_explored = 0
    added_frontier = 0
    while frontier:
        node = frontier.pop()
        #print "\n popped off frontier: " + str(node.state)
        if problem.goal_test(node.state):
            if stats:
                return node, number_explored, added_frontier
            else:
                return node

        explored.add(node.state)
        number_explored += 1

        for child in node.expand(problem):
            #print "child: " + str(child.state)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                added_frontier += 1
            elif child in frontier:
                incumbent = frontier[child]
                if memfun(child) < memfun(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
                    added_frontier += 1
    return None

def uniform_cost_search(problem, stats=False):
    """using best first graph search with path cost as the ordering
    function for the priority queue"""
    return best_first_graph_search(problem, lambda node: node.path_cost,\
           stats=stats)

def depth_limited_search(problem, limit=50):
    """[Fig. 3.17]"""
    def recursive_dls(node, problem, limit):
        """ depth first search with a limited depth """
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return if_(cutoff_occurred, 'cutoff', None)

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)

def iterative_deepening_search(problem):
    "[Fig. 3.18]"
    for depth in xrange(sys.maxint):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result

#______________________________________________________________________________
# Informed (Heuristic) Search

def gbf_graph_search(problem, fun, stats=False):
    """ same as best first search with fun being equal to
    the heuristic function used in the problem"""
    best_first_graph_search(problem, fun, stats=stats)

def astar_search(problem, heurfun=None, stats=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass.

    If stats = True, not only is the goal
    node returned, but the number of nodes added to the frontier and the
    explored set while searching for the solution
    """
    heurfun = memoize(heurfun, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + heurfun(n),\
          stats=stats)

def idastar_search(problem, heurfun=None, states=False, stats=True):
    """ TODO: implement this algorithm"""   
    return True

def build_search_tree(problem, func=None, depth=31):
    """ Build a search tree for a given problem.
    
    Args:
        problem - problem to be solved.

        func - a function to pass each node generated to.

        depth - set the search depth based on the path cost to the node
    """
    frontier = FIFOQueue()
    frontier.append(Node(problem.initial))
    explored = set()
    while frontier:
        node = frontier.pop()

        if node.depth > depth:
            return node.parent

        if func:
            func(node)

        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem) 
                        if child.state not in explored
                        and child not in frontier)

    if func:
        func(False)

    return explored
