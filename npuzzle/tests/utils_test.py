import unittest
import sys
sys.path.insert(0, '../src')
from npuzzle import npuzzle_utils as npu
import random 

class TestNPuzzleUtils(unittest.TestCase):
    def runTest(self):
        self.test_count_inversions_sort()

    def where_lists_differ(self, l1, l2):
        len1 = len(l1)
        len2 = len(l2)
        str1 = "all equal"
        inequal = False
        different = []

        if len1 != len2:
            print 'List lengths differ'
            return (len1, len2)
        else:
            print 'List lengths the same'
            print len1

        for i in range(0, len1):
            if l1[i] != l2[i]:
                inequal = True 
                different.append((i, l1[i], l2[i]))

        if inequal:
            return different
        else:
            print str1

    def test_count_inversions_sort(self):
        """ Todo: test count_inversions"""
        pass
