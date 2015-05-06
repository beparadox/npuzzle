from npuzzle.NPuzzleHeuristics import NPuzzleHeuristics
import unittest

class TestNPuzzleHeuristics(unittest.TestCase):
    """test the NPuzzleHeuristics class """

    def test_md_element(self):
        state = (9, 2, 3, 1, 4, 6, 7, 5, 8)
        index5 = state.index(5)
        dis = NPuzzleHeuristics.md_element(5, index5, 3) 
        self.assertEquals(dis, 1)

        index = state.index(9)
        dis = NPuzzleHeuristics.md_element(9, index, 3) 
        self.assertEquals(dis, 4)

        index = state.index(1)
        dis = NPuzzleHeuristics.md_element(1, index, 3) 
        self.assertEquals(dis, 1)


