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
from NPuzzleProblem import get_unsolvable_problem
from search import build_search_tree
from Queues import FIFOQueue

def get_solution(node):
    """ """
    return invert_solution(node.solution())

def get_search_tree(dim=3, depth=31):
    """ get a search tree for an NPuzzle state space of
    given dimension"""
    npp = get_unsolvable_problem(dim)
    node = build_search_tree(npp, depth=depth)
    return node.root_node()

def expand_search_tree(node, func):
    """ go through entire seach tree using BFS.
    func is a function you want to call on each node of the tree
    """
    #npp = get_unsolvable_problem(dim)
    #node = build_search_tree(npp, depth=depth)
    queue = FIFOQueue()
    queue.extend([node])
    while queue:
        node = queue.pop() 
        # add here what to do
        func(node)
        if hasattr(node, 'children'):
            children = node.children
            queue.extend(children)
        else:
            return

def solution_path_states(state, actions):
    """ 
    Take a list of NPuzzle actions and a starting state
    and return a list of tuples for all states leading back to
    the starting state.  The first element in the list should be the
    state passed to the function (the above parameter state) and the
    last element should be the goal state

    Allowable actions:
    1 move right
    -1 move left
    2 move up
    -2 move down
    """
    states = [state]
    for action in actions:
        state = result(state, action)
        states.append(state)

    return states

def result(state, action):
    """ s is the state,
    a the action. The actions are defined as:
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
    """ the solution is a list detailing the actions
    taken to move from the goal state to the initial state.
    We want to invert that"""
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
    """ insert val into a thelist using the bounds of imin
    and imax. A binary insert algorithm is used.""" 
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
    """ O(n^2) manner to count inversions. Yip-pee.
    Only used to count inversions for small lists < 100 elements
    """
    num_inversions = 0
    length = len(thelist)
    for i in range(0, length - 1):
        for j in range(i + 1, length):
            if thelist[j] < thelist[i]:
                num_inversions += 1

    return num_inversions
        
def count_inversions(l, n):
    '''
    @name: count_inversions 
    param:  l - list of numbers to be sorted
    param:  n - lenght of the list 
    returns
    Description: 
    '''
    if n == 1: 
        return (l, 0)
    else:
        ls = len(l)
        ls1 = len(l[0:ls/2])
        ls2 = len(l[ls/2:])

        if ls1 + ls2 != n:
            print "Error! ls1 +ls2 != n"
            exit(1)

        (B, x) = count_inversions(l[0:ls1], ls1)
        (C, y) = count_inversions(l[ls1:], ls2)
        (D, z) = merge_and_csplinv(B,C,ls1 + ls2)
        return (D, x + y + z)

def merge_and_csplinv(l1, l2, n): 
    '''
    name: merge_and_csplinv
    '''
    len1 = len(l1)
    len2 = len(l2)
    if len1 + len2 != n: 
        print "Error! %d + %d != %d" % (len1, len2, n)
        exit(1)

    p1 = 0
    p2 = 0
    inversions = 0
    newlist = []

    # nastiest code ever!
    # TODO: need to fix this while loop
    while p1 + p2 < n:
        if p1 < len1: 
            if p2 < len2:
                if l1[p1] <= l2[p2]:
                    newlist.append(l1[p1])
                    p1 += 1
                else:
                    newlist.append(l2[p2])
                    inversions += len1 - p1
                    p2 += 1
            else:
                newlist.append(l1[p1])
                p2 += 1
        else:
            newlist.append(l2[p2])
            p2 += 1
        
    return (newlist, inversions)

def manhattan_distance(thelist, goallist, *args):
    """ this function has limited usefulness. It's purpose is to find
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
    """ transform an npuzzle state (tuple) into
    an ndarray from numpy"""
    arr = np.array(state)
    length = len(arr)
    newv = [0 for i in range(length*length)]

    for i in range(length):
        #print i
        t = arr[i]
        newv[length*i + t - 1] = 1

    return newv
      
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
