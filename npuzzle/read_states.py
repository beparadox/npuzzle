#! /usr/bin/python
"""
 The primary purpose for this module is to allow the reading of a txt file
containing random acceptable states of the N-Puzzle. The textfile needs to
have one and only one state per line in 'tuple' form.

examples: 
    (1, 2, 3, 4, 5, 6, 7, 8, 9), 
    (1, 2, 3, 4, 5, 6, 7, 9, 8),
    (1, 2, 9, 4, 5, 3, 7, 8, 6) 

@author:    Bambridge E. Peterson
@file:      read_states.py
@date:      4/30/14"""

import random
import sys
import getopt

DEFAULT_FILE = '../data/8puzzle_states.txt'

def Usage():
    print "Usage: <%s> -n <int:num_of_states> -d <int: dimension>" % (__name__)
    #return False
    sys.exit(0)


#
def clean_line(line):
    """
    We need to 'clean' the lines in the textfile
    turn every line into a tuple
    invovles removing the leading '('
    the trailing ')'
    and the commas
    and coverting each str to an int ('9' to 9)"""
    # strip leading 
    line1 = line.strip().split("(")[1].strip().split(')')[0].strip().split(",")
    line = map(lambda s: int(s), line1)

    return tuple(line)

def from_txtfile(filename=DEFAULT_FILE, limit=181440, random=False):
    """ You can pass in the name of any file. Whether or not it works
    depends on your file!. 
    
    The data folder contains a file name
    8puzzle_states.txt which contains all 181,440 random states.
    If you want a random selection from this list of NUM elements,
    use that filename, and set limit=NUM and random=True. 

    If you have your own list, and it has less than 181,440 states,
    just pass the filename. Only set random to True if you want a random
    list of 'limit' elements from the main .txt file. So if random is True,
    limit should be set to something other than 181,440

    If you want the first 'limit' elements from the default file, just specify
    the number with limit.

    Return a list of the states"""
    try:
        fptr = open(filename, 'r')
        count = 0
        allstates = []

        line = fptr.readline()
        while line:
            line = clean_line(line)
            allstates.append(line)
            line = fptr.readline()

            count += 1

            if count == limit:
                break

        if random:
            L = len(allstates)
            allstates = [allstates[i] for i in sorted(random.sample(xrange(L), limit))]

        return allstates
    except IOError:
        print "IOError. Something wrong with your file!"

limit = 10
if __name__ == '__main__':
    NUM = 1
    DIM = 3
    (options, values) = getopt.getopt(sys.argv[1:], "-f:-l:-r")

    try:
        for option in options:
            #print value
            if option[0] == '-f':
                filename = option[1]
            elif option[0] == '-l':
                limit = option[1]
            elif option[0] == '-r':
                random = True

    except ValueError:
        Usage()

    print from_txtfile(limit = limit)
    
