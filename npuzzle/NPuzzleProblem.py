"""NPuzzleProblem definition """
from copy import copy
from Problem import Problem

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
