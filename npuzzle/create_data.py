"""  Create data module. Create data files for examination"""
import numpy as np
from read_solutions import get_collection
from config import DATAPATH

FILENAMES = {
        # the npuzzle state with the path cost as the last column
        'states_pc': 'states_pc.txt',

        # the npuzzle state with the heuristic function value as the last column. The heuristic function in this case is the manhattan distance heuristic
        'state_hfv':  'states_hfv.txt',

        # the vectors transformed to () form with the path cost as the last colun
        'tvpc': 'tv_pc.txt',

        # the vectors transformed to () form with the heuristic function value as the last column
        'tvhf': 'tv_hf.txt'
        }

def write_fvector_target(fname):
    """ write the npuzzle states to file along with the path cost
    
    Args:
        fname: string labeling """
    # get collection 
    collection = get_collection()
    # states with their path cost and heuristic function values
    state_hfvpc = collection.find({}, {'state': 1, 'hfvalue': 1, 'path_cost': 1})
    # create a list of ordered pairs, states and hfvalue 
    state_hf = [(node['state'], node['hfvalue']) for node in state_hfvpc]
    # append the hf values to the state
    [el[0].append(el[1]) for el in state_hf]
    # now create a new list consisting of the state with hfvalue appended
    shfnpa = np.array([el[0] for el in state_hf])
    # write the data to a file
    np.savetxt(DATAPATH + FILENAMES['state_hfv'])

