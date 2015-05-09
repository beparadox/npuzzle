""" Formal abstract definition of a problem and specific problems

@module:    Problem.py
@author:    Bambridge E. Peterson
@mail:      bambridge.peterson@gmail.com

@desc:      Defines a class Problem based upon the definition of
            a formal problem found in the textbook Artificial
            Intelligence: A Modern Approach by Peter Norvig and
            Stuart Kauffman

            A problem is formally defined with a start state and goal state.
            As it has a goal, there's a need for a goal test.
            There is also a step-cost and path cost.
            There are also given actions to be taken for a given state.
            Given a state s, what is the result when action a is applied
            to that state.
"""
from copy import copy

def update(item, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(item, dict):
        item.update(entries)
    else:
        item.__dict__.update(entries)
    return item

#pylint: disable=R0921
class Problem(object):
    """ This is an abstract class implementing the formal definition
    of a problem.

    abstract methods (need to be implemented):
    __init__
    actions
    result
    value
    """
    def __init__(self, initial, goal):
        """ Initialize the problem class with the given intital state and
        goal state.
        You can specify other arugments if need be. There doesn't have to
        be a unique state,
        which may require modifying
        """
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        """test state for goal state"""
        return state == self.goal

    def actions(self, state):
        """ All actions available from state s

        Actions should return a list of all possible
        actions permissable from the given state

        Args:
            state
        """
        raise NotImplementedError

    def result(self, state, action):
        """ resulting state when applying a to s
        """
        raise NotImplementedError

    def value(self, state):
        """Optimization problems have a value for each state.
        Args:
            state
        """
        raise NotImplementedError

    def step_cost(self, state, action):
        """
        step-cost should return the cost to apply
        action 'a' to state 's'
        """
        raise NotImplementedError

    def path_cost(self, node, action):
        """
        Get path cost of going from node using action
        """
        return self.step_cost(node.state, action) + node.path_cost

class Node(object):
    """A Node in a search tree

    These are the nodes the make up the search tree. Charecteristics include:

    state represents the primary characteristic of the Node
    action is the action that led us to this state
    parent is the Node that begot this Node by action
    """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action

        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __repr__(self):
        """ return a repr of the current node"""
        return "<Node %s>" % (str(self.state))

    def expand(self, problem):
        """ List of all successor Nodes of self"""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """ get a node the can be reached from the current
        node by application of the action"""
        nextstate = problem.result(self.state, action)

        return Node(nextstate, parent=self, action=action,\
               path_cost=self.path_cost + 1)

    def solution(self):
        """ return the list of moves used to find the solution
        from the initial state"""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """ return the path from current node back to the root node"""
        node, path = self, []
        while node:
            path.insert(0, node)
            node = node.parent

        return path

    def hn_path(self):
        """heuristic value for all nodes in the solution path"""
        path = self.path()
        return [node.h for node in path[0:len(path)]]

    def root_node(self):
        """get the initial state node"""
        return self.path()[0]

    def __eq__(self, other):
        """does other equal the current node?"""
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        """ return a unique hash of the state"""
        return hash(self.state)

    def __contains__(self):
        return self.state

class NPuzzleProblem(Problem):
    """
    This defines a particular problem, namely the n-puzzle problem.
    An n-puzzle is an example of a
    sliding block puzzle.
    @class:       NPuzzleProblem
    @extends:     Problem
    @param:       {tuple} initial inital state for an NPuzzleProblem
    @param:       {tuple} goal    goal state
    """
    def __init__(self, initial, goal, dim=3):
        """ call the Problem superclass __init__. Also set dim and
        size attribtues, and ensure that both the inital and goal
        states are tuples"""
        #both initial and goal should be tuples
        if not isinstance(initial, tuple) or not isinstance(goal, tuple):
            raise TypeError

        super(NPuzzleProblem, self).__init__(initial, goal)
        self.dim = dim
        self.size = dim*dim

        if len(initial) != self.size or len(goal) != self.size:
            errmsg = "Error: In NPuzzleProblem \n initial size = %d and\
                goal size = %d  self.size = %d" %\
                (len(initial), len(goal), self.size)
            raise ValueError(errmsg)

    def step_cost(self, state, action):
        """step cost of applying action while in state. For an NPuzzle,
        the step cost is always 1"""
        return 1

    def value(self, state):
        """see comments for Problem class """
        if state:
            return state
        else:
            return 1

    def actions(self, state):
        """Determine actions that can be applied on the given state

        Args:
            a sequence of integers representing a state in the NPuzzle

        Return:
            a list of integers representing the actions that can be applied
            to this state

        all actions are a direction to move the blank tile (or empty space) 
        which is the largest value in the state:
            left: -1
            right: 1
            up: 2
            down: -2"""

        size = self.size
        dim = self.dim
        try:
            empty_index = state.index(self.size)
        except ValueError:
            print "ValueError buddy"
            exit(1)

        actions = []
        if empty_index % dim != 0:
            #actions.append(-2)
            actions.append(-1)
        if (empty_index + 1) % dim != 0:
            #actions.append(2)
            actions.append(1)
        if empty_index - dim >= 0:
            #actions.append(1)
            actions.append(2)
        if empty_index + dim < size:
            #actions.append(-1)
            actions.append(-2)

        return actions

    def result(self, state, action):
        """ Get the resulting state from applying action to state

        Args:
            state: the state currently in,

            action: the action to apply to the current state

        Returns:
            the resulting state after applying action to state

        a the action. The actions are defined as:
            -1 move left (move the blank space left)
             1 move right
             2 move up
            -2 move down"""
        state = list(copy(state))
        dim = self.dim
        size = self.size

        try:
            # index of the 'empty' space on the NPuzzle board
            empty_index = state.index(size)
        except ValueError:
            print "Value Error: Unable to get zero index"
            exit(1)

        if action == -1: # move left
            tmp = state[empty_index - 1]
            state[empty_index - 1] = state[empty_index]
            state[empty_index] = tmp
        elif action == 1: # move right
            tmp = state[empty_index + 1]
            state[empty_index + 1] = state[empty_index]
            state[empty_index] = tmp
        elif action == 2: # move up
            tmp = state[empty_index - dim]
            state[empty_index - dim] = state[empty_index]
            state[empty_index] = tmp
        else:           #move down
            tmp = state[empty_index + dim]
            state[empty_index + dim] = state[empty_index]
            state[empty_index] = tmp

        return tuple(state)

def get_unsolvable_problem(dim=3):
    """ returns a NPuzzle problem that is unsolvable. Used for generating
    the search tree of all possible node for a given dimension"""
    size = dim * dim
    initial = tuple(range(1, size + 1))
    goal = range(1, size + 1)
    tmp = goal[0]
    goal[0] = goal[1]
    goal[1] = tmp
    # NPuzzleProblem expects tuple
    return NPuzzleProblem(initial, tuple(goal), dim)
