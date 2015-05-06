#! /usr/bin/python
"""This will open up a text file that has all states
for an npuzzle instance

@author: Bambridge E. Peterson
"""
from getopt import getopt
from sys import argv

def clean_line(line):
    """clean a line from the file

    Every line is of the form (1, 2, 3, 4, 5, 6, 7, 8, 9), depending upon the
    tuple length. This is considered to be a string, since they are
    stored in a text file.

    turn every line into a tuple
    invovles removing the leading '('
    the trailing ')'
    and the commas
    and coverting each str to an int ('9' to 9)
    """
    # strip leading
    #line1 = line.strip().split("(")[1].strip().split(')')[0].strip().split(",")
    #line = map(lambda s: int(s), line1)

    #return tuple(line)
    #return tuple(map(lambda s: int(s),\

    #return tuple([int(s) for s in
    return tuple([int(s) for s in\
            line.strip().split("(")[1].strip().split(')')[0].strip().split(",")])

def to_tuples(states):
    """change states into tuples"""
    length = len(states)
    for index in range(0, length):
        states[index] = tuple(states[index])


def from_txt(filename):
    """get states from the filename"""
    allstates = []
    try:
        fptr = open(filename, 'r')
        line = fptr.readline()
        while line:
            line = clean_line(line)
            allstates.append(line)
            line = fptr.readline()
        fptr.close()
        return allstates
    except IOError:
        print "in from_txt and unable to open " + filename

def main():
    """ run this when the file is executed from the command line"""
    (options, value) = getopt(argv[1:], "-f")
    for option in options:
        if option[0] == '-f':
            try:
                print from_txt(str(value[0]))
            except IOError as err:
                print "error: " + err

if __name__ == '__main__':
    main()
