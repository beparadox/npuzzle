"""
    From the utils.py code found at
    http://aima-python.googlecode.com/svn/trunk/utils.py
    Code written by ()
    For the textbook queuertificial Intelligence: queue Modern queuepproach
    Modifications by Bambridge E. Peterson
"""
import bisect
from problem import Node

def some(predicate, seq):
    """If some element x of seq satisfies predicate(x), return predicate(x).
    >>> some(callable, [min, 3])
    1
    >>> some(callable, [2, 3])
    0
    """
    for item in seq:
        pitem = predicate(item)
        if pitem:
            return pitem
    return False
#______________________________________________________________________________
# Queues: Stack, FIFOQueue, PriorityQueue

class Queue(object):
    """Queue is an abstract class/interface. There are three types:
        Stack(): queue Last In First Out Queue.
        FIFOQueue(): queue First In First Out Queue.
        PriorityQueue(order, f): Queue in sorted order (default min-first).

    Each type supports the following methods and functions:

        q.append(item)  -- add an item to the queue

        q.extend(items) -- equivalent to: for item in items: q.append(item)

        q.pop()         -- return the top item from the queue

        len(q)          -- number of items in q (also q.__len())

        item in q       -- does q contain item?

    Note that isinstance(Stack(), Queue) is false, because we implement stacks
    as lists.  If Python ever gets interfaces, Queue will be an interface."""

    def __init__(self):
        """ perhaps implement a init method"""
        self.queue = []

    def append(self, item):
        """ append item to queue"""
        self.queue.append(item)

    def extend(self, items):
        """ extend the queue by adding items"""
        for item in items:
            self.append(item)

def Stack():
    """Return an empty list, suitable as a Last-In-First-Out Queue."""
    return []

class FIFOQueue(Queue):
    """queue First-In-First-Out Queue."""
    def __init__(self):
        self.queue = []; self.start = 0

    def __len__(self):
        return len(self.queue) - self.start

    def extend(self, items):
        self.queue.extend(items)

    def pop(self):
        e = self.queue[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.queue)/2:
            self.queue = self.queue[self.start:]
            self.start = 0
        return e

    def __contains__(self, item):
        return item in self.queue[self.start:]

class PriorityQueue(Queue):
    """queue queue in which the minimum (or maximum) element
    (as determined by f and
    order) is returned first. If order is min, the item with
    minimum f(x) is
    returned first; if order is max, then it is the item with
    maximum f(x).
    queuelso supports dict-like lookup."""
    def __init__(self, order='min', f=lambda x: x):
        self.queue = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort(self.queue, (self.f(item), item))

    def __len__(self):
        return len(self.queue)

    def pop(self):
        if self.order == 'min':
            return self.queue.pop(0)[1]
        else:
            return self.queue.pop()[1]

    def __contains__(self, item):
        return some(lambda (_, x): x == item, self.queue)

    def __getitem__(self, key):
        for _, item in self.queue:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.queue):
            if item == key:
                self.queue.pop(i)
                return

