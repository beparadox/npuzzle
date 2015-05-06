""" A class for npuzzle heuristic functions """
class NPuzzleHeuristics(object):
    """ For use with the NPuzzleProblem class
    """
    def __init__(self, hnfun='md', dim=3):
        """ initialze the classes heuristic function
        and the name of the heuristic function"""
        self.hfuns = {
            'md': [
                self.manhattan_distance,
                'manhattan distance'],

            'mt': [
                self.misplaced_tiles,
                'misplaced tiles'],

            'ff': [
                self.ffann,
                'feed forward ann'],

            'svm': [
                self.ffann,
                'support vector machine']
            }
        try:
            self.hnfun = self.hfuns[hnfun][0]
            self.hfname = self.hfuns[hnfun][1]
            self.dim = dim
            self.size = dim * dim
            self.goaldict = dict(zip(range(1, self.size + 1), range(0, self.size)))
            self.md_table = self.init_md_table()
        except KeyError as err:
            print "Invalid hnfun value given for NPuzzleHeuristics: %s" % err
            exit(0)

    def init_md_table(self):
        """
        Returns: dictionary of integers as keys and lists as values

        Initialize md_table
        md_table is the manhattan distance table. It sets the md_table
        property as a dictionary of lists, where each key represents an index
        of the goal state (square on the board), and it's value is a list
        of the manhattan distances to all other locations in the tuple

        For dim=3 (size = dim*dim), the md_table will be:

        {0: [0, 1, 2, 1, 2, 3, 2, 3, 4],
         1: [1, 0, 1, 2, 1, 2, 3, 2, 3],
         2: [2, 1, 0, 3, 2, 1, 4, 3, 2],
         3: [1, 2, 3, 0, 1, 2, 1, 2, 3],
         4: [2, 1, 2, 1, 0, 1, 2, 1, 2],
         5: [3, 2, 1, 2, 1, 0, 3, 2, 1],
         6: [2, 3, 4, 1, 2, 3, 0, 1, 2],
         7: [3, 2, 3, 2, 1, 2, 1, 0, 1],
         8: [4, 3, 2, 3, 2, 1, 2, 1, 0]}
	"""
        # size of the board (total spaces). Square of the dimension
        dim = self.dim
        size = dim * dim
        # define the md_table as a dictionary
        md_table = dict()
        # value is the key for a list of manhattan distances
        for value in range(0, size):
            md_table[value] = []
            # the md can be calculated as follows:
            # the 'horizontal' value is abs val of (current / dim - dest / dim)
            # the 'veritical' value is abs val (current % dim - dest % dim)
            for els in range(0, size):
                md_table[value].append(abs((els / dim) - (value / dim))\
                        + abs(els % dim - value % dim))

        return md_table

    def manhattan_distance(self, node):
        """
        Args:
            node: instance of the Node class found in Problem.py. We need
            the state property of the node

            
	manhatan_distance expects a list to perform its calculation.
        current_node.state is a tuple
	"""
        state = node.state
        size = len(state)
        return sum([self.md_table[i][self.goaldict[state[i]]]\
                for i in range(0, size)\
                if state[i] != size])

    def md_dictionary(self, dictionary):
        """
        To get manhattan distance for a set of keys in a dictionary.
        Could be only
        a single key
        """
        return sum([self.md_table[key][self.goaldict[dictionary[key]]]\
                for key in dictionary.keys()])

    @classmethod
    def md_element(cls, element, current_index, dim):
        """get the manhattan distance for a particular element from
        its location in the goal state"""
        goal_index = element - 1
        return abs(current_index / dim - goal_index / dim) +\
                abs(current_index % dim - goal_index % dim)


    def misplaced_tiles(self, node):
        """ heuristic function calculating number of tiles not in
        their 'home' position
        
        Args:
            node: """
        state = node.state
        return sum(0 if index == self.goaldict[element] else 1 for index,\
                element in enumerate(state))

    def ffann(self, state):
        """ using a trained feed-forward neural network as the heuristic
        function

        atype = self.ann_atype
        weights = self.ann_weights
        output = []
        output.append(np.array(transform_vector(state)))
        for i in range(1, 3):
            inp = np.array([1])
            net = np.append(inp, output[i - 1])
            output.append(np.array(actfun(np.inner(net, weights[i - 1]),\
                    atype[i - 1])))

        # optimal
        if self.ann_pc == 1:
            heur = scale([output[2]], 5, 31)
        # optimal - hn
        elif self.ann_pc == 2:
            heur = scale([output[2]], 0, 18)

            return round(heur[0]/2.0, 2) + self.manhattan_distance(state)
        # average
        elif self.ann_pc == 3:
            heur = scale([output[2]], 5, 26)
        # md
        else:
            heur = scale([output[2]], 4, 22)
            return round((heur[0] + self.manhattan_distance(state) + 1)/2.0, 1)

        return round(heur[0], 1)
        #return self.manhattan_distance(state)
        """
        pass

    def svm_heur(self, node):
        """ use a support vector machine developed heuristic"""
        pass
