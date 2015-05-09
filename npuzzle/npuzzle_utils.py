""" 
    File:       npuzzle_utils.py
    Author:     Bambridge E. Peterson
    Email:      bambridge.peterson@gmail.com
    Date:
    LastMod:
    Desc:
        utilities class for the npuzzle problem. Many of these
        functions
        haven't been used in a while. """
from copy import copy
from math import sqrt, floor 
import numpy as np
from problem import get_unsolvable_problem
from search import build_search_tree
from queues import FIFOQueue
from heuristics import NPuzzleHeuristics

def acceptable_state(state):
    """ determine if a tuple is an acceptable state for an npuzzle.

    Args:
        state - a tuple of integers. The length should be equal to the square
        of a positive integer n. Generally 4, 9, 16, or 25. The numbers should
        be all integers from 1 to n in an acceptable state (see below).

    Returns:
        true if acceptable, false otherwise.

    When is an npuzzle state considered acceptable? When the number of
    inversions plus the manhattan distance of the 'blank space' from it's
    position in the goal configuration is even.
    """
    size = len(state)
    #assert type(state) == tuple, 'state is not acceptable'
    distance = NPuzzleHeuristics.md_element(size, state.index(size),\
            int(np.sqrt(size)))
    #state, inversions = count_inversions(list(state), size)
    inversions = count_inversions_n2(list(state))
    if ((distance + inversions) % 2 == 0): 
        return True
    else:
        return False

def get_solution_actions(node):
    """ get the list of actions that will take you from state in node to
    the goal state. 
    
    Args:
        node: a solution Node found after a search. Note this is not a node
        from the database.

    Returns:
        a list of actions 
        
        Each action is an integer. (-1, 1, -2, 2) are the possible actions
        """
    return invert_solution(node.solution())

def get_search_tree(dim=3, depth=31):
    """ get a search tree for an NPuzzle state space of
    given dimension
    
    Args:
        dim: integer representing the dimension"""
    npp = get_unsolvable_problem(dim)
    node = build_search_tree(npp, depth=depth)
    return node.root_node()

def solution_path_states(state, actions):
    """ 
    Take a list of NPuzzle actions and a starting state
    and return a list of tuples for all states leading back to
    the starting state.  The first element in the list should be the
    state passed to the function (the above parameter state) and the
    last element should be the goal state

    Args:
        state: tuple representing an acceptable npuzzle state

        actions: a list of integers representing actions to peform on the state

    Allowable actions:
    1 move right
    -1 move left
    2 move up:
    -2 move down
    """
    states = [state]
    for action in actions:
        state = result(state, action)
        states.append(state)

    return states

def swap(state, index1, index2):
    """ swap elements in index1 and index2 of state
    
    """
    tmp = state[index1]
    state[index1] = state[index2]
    state[index2] = tmp

def result(state, action):
    """ perform an action on the given state. return the new state.

    Args:
        state: tuple of an acceptable npuzzle state

        action: integer representing the action to perform

    Returns:
        new state
    
     The actions are defined as:
        -1 move left (move the blank space left)
         1 move right
         2 move up
        -2 move down"""
    state = list(copy(state))
    dim = int(sqrt(len(state)))
    size = dim * dim 

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

def invert_solution(solution, func=lambda x: -x):
    """ Get the inverse of the solution
    Args:
        solution: the solution is a list detailing the actions
    taken to move from the goal state to the initial state.

    Returns:
        the inversion of the solution

    What does it mean to invert a solution? For starters, always
    look on the bright side of life. After that, keep in mind that a
    solution involves moving tiles, one at a time, into the empty space,
    until the desired state is reached.
    
    I imagined it the other way around: moving the blank space around the
    board. Integer values represent a move of the blank, or empty, space.
    1  one space to the right
    -1 one space to the left
    2  up one space
    -2 down one space
    
    So a solution is a list of integers. To invert the solution, you invert
    the sign for each number, and then reverse the entire list"""
    solution = [func(x) for x in solution]
    solution.reverse()
    return solution
    
def init_md_table(dim=3):
    """
    @param dim dimension of the problem
    @return dict

    md_table is the manhattan distance table. It sets the md_table
    property as a dictionary of lists, where each key represents an index
    of the goal state (square on the board), and it's value is a list
    of the manhattan distances to all other locations in the tuple

    For dim=3 (size = dim*dim), the md_table will be:

    {0: [0, 1, 2, 1, 2, 3, 2, 3, 4],
     1: [1, 0, 1, 2, 1, 2, 3, 2, 3],
     2: [2, 1, 0, 3, 2, 1, 4, 3, 2],
     3: [1, 2, 3, 0, 1, 2, 1, 2, 3],
     4: [2, 1, 2, 1, 0, 1, 2, 1, 2],
     5: [3, 2, 1, 2, 1, 0, 3, 2, 1],
     6: [2, 3, 4, 1, 2, 3, 0, 1, 2],
     7: [3, 2, 3, 2, 1, 2, 1, 0, 1],
     8: [4, 3, 2, 3, 2, 1, 2, 1, 0]}
    """
    # size of the board (total spaces). Square of the dimension
    size = dim*dim
    # define the md_table as a dictionary
    md_table = dict()
    # value is the key for a list of manhattan distances
    for value in range(0, size):
        md_table[value] = []
        # the md can be calculated as follows:
        # the 'horizontal' value is abs val of (current / dim - dest / dim)
        # the 'veritical' value is abs val (current % dim - dest % dim)
        for els in range(0, size):
            md_table[value].append(abs((els / dim) - (value / dim))\
                    + abs(els % dim - value % dim))

    return md_table

def bsinsert_desc(thelist, val, imin, imax):
    """ binary search insert. insert val into a thelist using the bounds
    of imin and imax.

    Args:
        thelist: the list of elements to insert a value into

        val:     the value to be inserted

        imin:    minimum index value in the list

        imax:    maximum index value in the list
    
    
    """
    if imax < imin: 
        print "nothing inserted"
        return
    length = imax - imin
    if length == 1:
        if imin + 1 == imax:
            if val <= thelist[imax - 1]:
                thelist.append(val)
                return
        # this is because we want newest value insert "first"
        # in case of descending order, "first" is last
        if val <= thelist[imin]:
            thelist.insert(imin+ 1, val)
        else:
            thelist.insert(imin, val)
        print "thelist = " + str(thelist)
        return  

    half = imin + length / 2
    if val <= thelist[half]:
        # this is because of desc order. we want to
        # set imin as the half value
        imin = half 
        bsinsert_desc(thelist, val, imin, imax)
    else:
        # maximum changes, min stays the same
        imax = half
        bsinsert_desc(thelist, val, imin, imax)

def count_inversions_n2(thelist):
    """ O(n^2) version of counting inversions.

    Args:
        thelist: list of intgers in which we count inversions

    Returns:
        num_inversions: integer which counts the number of inversions
   
    This should be used on small lists
    """
    num_inversions = 0
    length = len(thelist)
    for i in range(0, length - 1):
        for j in range(i + 1, length):
            if thelist[j] < thelist[i]:
                num_inversions += 1

    return num_inversions

def get_all_inversions(states):
    """ get a numpy array of all inversions for all states
    
    Args:
        states: list of acceptable npuzzle states
        
    Returns:
        numpy array containing number of inversions in each state"""
    length = len(states)
    inversions = np.array([state_num_inversions(states[i]) for i in range(0, length)])

    return inversions

def state_num_inversions(state):        
    """ return the number of inversions for a given state"""
    if type(state) == tuple:
        state = list(state)

    return count_inversions(state, len(state))[1]

def count_inversions(integers, num):
    """ Count the number of inversions in a sequence of integers
    
    Args:
        integers: a sequence of integers
      
    """
    if num == 1: 
        return (integers, 0)
    else:
        ls = len(integers)
        ls1 = len(integers[0:ls/2])
        ls2 = len(integers[ls/2:])

        (B, x) = count_inversions(integers[0:ls1], ls1)
        (C, y) = count_inversions(integers[ls1:], ls2)
        (D, z) = merge_and_csplinv(B, C, ls1 + ls2)
        return (D, x + y + z)

def merge_and_csplinv(list1, list2, num): 
    """ Merge to sorted lists of integers into one sorted list,
    and count the number of inversions between the two lists

    Args:
        list1: first sorted list
        
        list2: second sorted list

        num: number of elements in both lists

    Returns:
        tuple consisting of the merged list and the number of inversions
        between the two lists
    """
    len1 = len(list1)
    len2 = len(list2)
    if len1 + len2 != num: 
        print "Error! %d + %d != %d" % (len1, len2, num)
        exit(1)

    ptr1 = 0
    ptr2 = 0
    inversions = 0
    newlist = []
    while ptr1 + ptr2 < num:
        if ptr1 > len1 - 1:
            newlist.append(list2[ptr2])
            ptr2 += 1
        elif ptr2 > len2 - 1:
            newlist.append(list1[ptr1])
            ptr1 += 1
        elif list1[ptr1] <= list2[ptr2]:
            newlist.append(list1[ptr1])
            ptr1 += 1
        else:
            newlist.append(list2[ptr2])
            ptr2 += 1
            inversions += len1 - ptr1
       
    return (newlist, inversions)

def manhattan_distance(thelist, goallist, *args):
    """It's purpose is to find
    the manhattan or taxicab distance of an element from it's intended
    destination or goal place. It can also return the sum of the manhattan
    distnces of all elements in the list.

    It takes a list representing the current state of the array and
    another list representing the goal state. An optional third argument
    is a number which we want to calculate the manhattan distance for.
    If that number is not given, we calculate the manhattan distance for the
    entire list

    the length of the given list should be a square. For computational
    purposes we limit this to sizes of l = 4, 9, 16 for square size n = 2,
    3 or 4
    
    if l == 4:
        size = 2
    elif l == 9:
        size = 3
    elif l == 16:
        size = 4
    else:
        return False
    we need to check that the given list actually contains all the numbers
    in the goal state. The numbers should be from 0 to l, but the goal state is
    [1, 2, ...,  l, 0]"""
    l = len(thelist)
    if l != len(goallist) or sqrt(l) > floor(sqrt(l)):
        print "LengthError"
        exit(1)
    size = sqrt(l)
    
    if len(args) == 0:
        md_sum = 0
        for num in range(0, l):
            """ we need to find the current index of num in the given list and
            its index in the goal state"""
            current_index = thelist.index(num)
            goal_index = goallist.index(num)
            #print "current_index = " + str(current_index)
            #print "goal_index = " + str(goal_index)
            """ at this point we can compute the manhattan distance as follows: """
            ci_quo = current_index / size
            ci_rem = current_index % size
            gi_quo = goal_index / size
            gi_rem = goal_index % size 
            md_sum += abs(ci_quo - gi_quo) + abs(ci_rem - gi_rem)
        return md_sum 
    else:
        l = len(args)
        md_sum = 0
        for i in range(0, l):
            num = args[i]
            current_index = thelist.index(num)
            goal_index = goallist.index(num)
            #print "c_i = " +  str(current_index )
            # print "g_i = " +  str(goal_index)
            """ at this point we can compute the manhattan distance as follows: """
            ci_quo = current_index / size
            ci_rem = current_index % size
            gi_quo = goal_index / size
            gi_rem = goal_index % size 
            md_sum += abs(ci_quo - gi_quo) + abs(ci_rem - gi_rem)
        return md_sum
        
    return

def transform_vector(state):
    """ transform an npuzzle state (tuple) of size s into
    an ndarray from numpy of 1's and 0's of size s^2.
    
    Args: 
        state: tuple of size s that is an acceptable state for an npuzzle
        
    Returns:
        newv:  numpy array of size s^2 of 1's and 0's

    the new array is of size s^2. It helps to visualize this as an array
    of s arrays, each of size s, in linear order.
    
    For each of the s 'subarrays' of size s, all elements are 0 except
    for one, which equals 1. Which one depends upon the value of index 
    i in the state.
    
    For the ith 'subarray' in the new array, the state[i] elements in
    this subarray equals 1. 
    
    So, suppose the state was (1, 2, 3, 4). The new array will be:
        [1, 0, 0, 0,| 0, 1, 0, 0,| 0, 0, 1, 0, |0, 0, 0, 1].
        
    For [4, 3, 2, 1], it would be:
    [0, 0, 0, 1,|0, 0, 1, 0|, 0, 1, 0, 0|, 1, 0, 0, 0]

    I added vertical bars for clarification. The first four elements
    correspond to the number 4 in the given state
    """
    length = len(state)
    #newvec = np.zeros((1, length*length))
    newvec = [0 for i in range(0, length*length)]

    for i in range(length):
        #newvec[0][length*i + state[i] - 1] = 1
        newvec[length*i + state[i] - 1] = 1

    return newvec
      
def scale(state, min_t, max_t):
    """ scale each value of state using a min and max value"""
    arr = np.array(state)
    max_v = np.max(arr)
    min_v = np.min(arr)
    if max_v == min_v:
        max_v = 1 
        min_v = 0 
    return (max_t - min_t) * ((arr - min_v)/float((max_v - min_v))) + min_t
    
def actfun(x, funtype, par=[1,0]):
    """ define activation functions for the neural network"""
    xarr = np.array(x)
    #linear
    if funtype == 3:
        a = par[0]
        b = par[1]
        y = a*xarr + b
    # tanh
    elif funtype == 2:  
        T = par[0]
        tmp = np.exp(xarr/T)
        y = ((tmp - 1)/tmp)/((tmp + 1)/tmp)
    # sigmoid
    else:
        T = par[0]
        y = 1/(1 + np.exp(-xarr/T))

    return y

def update_db_solutions():
    """ the db_solutions are wrong. update them! """
    return 0
