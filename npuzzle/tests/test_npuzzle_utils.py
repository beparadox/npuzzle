import unittest
import sys
from npuzzle.npuzzle_utils import merge_and_csplinv, count_inversions,\
        acceptable_state
import random 

class TestNPuzzleUtils(unittest.TestCase):
    def test_merge_and_csplinv(self):
        l1 = [1, 3, 5, 7]
        l2 = [2, 4, 6, 8]
        rl1, i1 = merge_and_csplinv(l1, l2, 8)
        self.assertEquals(6, i1)
        self.assertEquals(range(1,9), rl1)

        l1 = [1, 2, 3, 4]
        l2 = [5, 6, 7, 8]
        rl1, i1 = merge_and_csplinv(l1, l2, 8)
        self.assertEquals(0, i1)
        self.assertEquals(range(1, 9), rl1)

        l1 = [1, 2, 7, 8]
        l2 = [3, 4, 5, 6]
        rl1, i1 = merge_and_csplinv(l1, l2, 8)
        self.assertEquals(8, i1)
        self.assertEquals(range(1, 9), rl1)

        l1 = [1, 2, 3, 8]
        l2 = [4, 5, 6, 7]
        rl1, i1 = merge_and_csplinv(l1, l2, 8)
        self.assertEquals(4, i1)
        self.assertEquals(range(1, 9), rl1)

        l1 = [5, 6, 7, 8]
        l2 = [1, 2, 3, 4]
        rl1, i1 = merge_and_csplinv(l1, l2, 8)
        self.assertEquals(16, i1)
        self.assertEquals(range(1, 9), rl1)

    def test_count_inversions(self):
        l1 = [1, 2, 3, 4, 5]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(0, i1)
        self.assertEquals(range(1, 6), rl1)

        l1 = [5, 4, 3, 2, 1]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(10, i1)
        self.assertEquals(range(1, 6), rl1)

        l1 = [1, 2, 3, 5, 4]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(1, i1)
        self.assertEquals(range(1, 6), rl1)

        l1 = [1, 2, 4, 5, 3]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(2, i1)
        self.assertEquals(range(1, 6), rl1)

        l1 = [1, 3, 4, 5, 2]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(3, i1)
        self.assertEquals(range(1, 6), rl1)

        l1 = [5, 3, 4, 1, 2]
        rl1, i1 = count_inversions(l1, len(l1))
        self.assertEquals(8, i1)
        self.assertEquals(range(1, 6), rl1)

    def test_acceptable_states(self):
        size = 9
        state = (1, 2, 3, 4, 5, 6, 7, 9, 8)
        self.assertTrue(acceptable_state(state))
