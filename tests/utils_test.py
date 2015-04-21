import unittest
import sys
sys.path.insert(0, '../src')
import npuzzle_utils as npu
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
        NUM_TESTS = 1    
        MAX = 1000

        for i in range(NUM_TESTS):
            ranint = random.randint(1, MAX)
            totest1 = range(ranint)
            random.shuffle(totest1)

            totest2 = range(ranint)
            print sorted(totest1) == totest2
            res1 = npu.count_inversions(totest1, len(totest1))[0]

            print res1 == totest2

            if not res1 == totest2:
                print self.where_lists_differ(res1, totest2)

            
            assert res1 == totest2, 'lists are not equal'
          
test = TestNPuzzleUtils()
test.test_count_inversions_sort()
