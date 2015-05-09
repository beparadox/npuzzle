NPuzzle Project - examining the sliding block puzzle
=======================

Project Overview
-----------------------
Basically, there are two ideas behind this project; one idea was to attempt to see if new heuristics could be created for the NPuzzle using machine learning techniques. The other was simply to examine the NPuzzle problem in a bit more depth. Sliding block puzzles are handy for testing new search algorithms and heuristics. But I feel it also sheds a tiny bit a light on the problem of how an intelligent agent learns. The rules are simple, and it's not impossibly difficult for a person to solve a random instance of a puzzle. The difficult part, at least for a person, is finding an optimal solution once given a random instance of the puzzle.

How many nodes does a search algorithm need to explore in order to find the optimal solution? Should we trade optimality for a reduction in the nodes examined? It likely makes little difference in time for smaller-sized puzzles, but could be very useful in larger dimensions, where the state space suffers from "combinatorial explosion".

NPuzzle Introduction
--------------------
An NPuzzle is a sliding block puzzle in which a square grid of (usually numbered) tiles, containing one empty space, can be rearranged in a particular order. The particular order depends upon the goal state of the puzzle.  Usually the spaces are labeled with the positive integers from 1 to *n*, where *n* is one less than the square of a positive integer (like 3, 8 or 15).   The goal state is generally the numbered block in ascending order starting from the upper left position, going left to right, top to bottom, finishing with the empty space in the bottom right corner. 

The size of the grid can vary, but it's usually of size 4, 9, 16 or 25. The square root of the size is called the *dimension* of the puzzle. 

The grid is represented internally by a tuple (a list would work as well) of positive integers. 
