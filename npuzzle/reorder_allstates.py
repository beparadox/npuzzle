#! /usr/bin/python
""" Randomize the states in 8puzzle_states.txt 

"""

import read_allstates
import random

states = read_allstates.from_txt('../data/8puzzle_states.txt')
random.shuffle(states)

fptr = open('../data/random_puzzle_states.txt', 'w')
for state in states:
    fptr.write(str(state) + "\n")

fptr.close()
