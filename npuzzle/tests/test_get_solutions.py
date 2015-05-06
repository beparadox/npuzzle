"""
Testing the get_solutions module
"""
from  npuzzle.get_solutions import get_random_solutions as random, get_solution,\
        get_solutions, get_statnodes
import unittest

class TestGetSolutions(unittest.TestCase):
    """ testing the get_solutions module"""
    def test_get_random_solutions(self):
        """ test get_random_solutions function"""
        num_sols = 1
        sols = random(num_sols)
        self.assertEqual(num_sols, len(sols))

if __name__ == '__main__':
    unittest.main()
