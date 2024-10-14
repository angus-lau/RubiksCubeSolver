import unittest
import checker

class TestChecker(unittest.TestCase):
    def test_white_cross_check(self):
        # No white cross
        no_white_cross = {
            'F': [['R', 'B', 'R'], ['O', 'G', 'Y'], ['Y', 'G', 'O']],
            'B': [['O', 'Y', 'R'], ['Y', 'B', 'R'], ['R', 'W', 'Y']],
            'L': [['B', 'G', 'B'], ['B', 'O', 'Y'], ['O', 'O', 'O']],
            'R': [['G', 'G', 'B'], ['G', 'R', 'B'], ['W', 'O', 'W']],
            'T': [['W', 'R', 'W'], ['O', 'W', 'R'], ['Y', 'W', 'Y']],
            'D': [['B', 'W', 'G'], ['B', 'Y', 'W'], ['G', 'R', 'G']]
        }
        # White cross with correct edge pieces
        white_cross_correct_edge = {
            'F': [['W', 'G', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'B', 'Y'], ['Y', 'B', 'R'], ['B', 'G', 'Y']],
            'L': [['G', 'O', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'T': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
            'D': [['W', 'O', 'W'], ['R', 'Y', 'B'], ['R', 'Y', 'W']]
        }
        # White cross with incorrect edge pieces
        white_cross_incorrect_edge = {
            'F': [['W', 'R', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'O', 'Y'], ['Y', 'B', 'R'], ['B', 'W', 'Y']],
            'L': [['G', 'G', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'B', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'T': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
            'D': [['W', 'O', 'W'], ['R', 'Y', 'B'], ['R', 'Y', 'W']]
        }
        self.assertTrue(checker.white_cross_check(white_cross_correct_edge))
        self.assertFalse(checker.white_cross_check(no_white_cross)) 
        self.assertFalse(checker.white_cross_check(white_cross_incorrect_edge))

    def test_white_corners_check(self):
        # White corners with correct corner pieces
        white_corners_correct= {
            'F': [['G', 'G', 'G'], ['B', 'G', 'G'], ['Y', 'Y', 'O']],
            'B': [['B', 'B', 'B'], ['R', 'B', 'G'], ['B', 'B', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['B', 'B', 'R']],
            'R': [['R', 'R', 'R'], ['Y', 'R', 'G'], ['G', 'O', 'R']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'R', 'Y'], ['R', 'Y', 'Y'], ['O', 'Y', 'Y']]
        }

        # White corners with incorrect corner pieces
        white_corners_false = {
            'F': [['W', 'G', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'B', 'Y'], ['Y', 'B', 'R'], ['B', 'G', 'Y']],
            'L': [['G', 'O', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'T': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
            'D': [['W', 'O', 'W'], ['R', 'Y', 'B'], ['R', 'Y', 'W']]
        }

        # White corners with wrong corner pieces
        white_corners_wrong_corner = {
            'F': [['R', 'G', 'O'], ['Y', 'G', 'Y'], ['G', 'B', 'Y']],
            'B': [['O', 'B', 'R'], ['Y', 'B', 'G'], ['Y', 'B', 'G']],
            'L': [['B', 'O', 'G'], ['R', 'O', 'G'], ['R', 'O', 'O']],
            'R': [['G', 'R', 'B'], ['R', 'R', 'O'], ['B', 'B', 'B']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'O'], ['G', 'Y', 'R'], ['Y', 'O', 'R']]
        }

        self.assertTrue(checker.white_corners_check(white_corners_correct))
        self.assertFalse(checker.white_corners_check(white_corners_false))
        self.assertFalse(checker.white_corners_check(white_corners_wrong_corner))

    def test_middle_edge(self):
        # Middle layer with correct edge pieces
        middle_edge_correct = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'O', 'Y']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['G', 'Y', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['Y', 'Y', 'B']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['G', 'B', 'O']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'R'], ['G', 'Y', 'Y'], ['R', 'R', 'Y']]
        }

        # Middle layer with 2 incorrect edge pieces
        middle_edge_two_false = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'O'], ['B', 'Y', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['O', 'O', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'R'], ['G', 'R', 'Y']],
            'R': [['R', 'R', 'R'], ['G', 'R', 'R'], ['B', 'B', 'Y']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['O', 'G', 'Y'], ['Y', 'Y', 'Y'], ['R', 'Y', 'G']]
        }

        # Middle layer wiht all wrong edge pieces
        middle_edge_false = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'O'], ['R', 'R', 'G']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'Y'], ['B', 'Y', 'Y']],
            'L': [['O', 'O', 'O'], ['R', 'O', 'R'], ['B', 'O', 'G']],
            'R': [['R', 'R', 'R'], ['G', 'R', 'Y'], ['Y', 'Y', 'R']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'B', 'O'], ['B', 'Y', 'O'], ['O', 'G', 'Y']]
        }

        self.assertTrue(checker.middle_edge(middle_edge_correct))
        self.assertFalse(checker.middle_edge(middle_edge_two_false))
        self.assertFalse(checker.middle_edge(middle_edge_false))


    # TODO !!!
    def test_yellow_pattern_switch(self):
        # Yellow cross
        yellow_cross = {
            'F': [['Y', 'B', 'W'], ['G', 'G', 'O'], ['O', 'G', 'G']],
            'B': [['O', 'W', 'W'], ['B', 'B', 'W'], ['B', 'B', 'B']],
            'L': [['G', 'R', 'G'], ['O', 'O', 'W'], ['Y', 'O', 'B']],
            'R': [['B', 'G', 'W'], ['B', 'R', 'W'], ['Y', 'R', 'W']],
            'T': [['R', 'R', 'G'], ['G', 'W', 'O'], ['R', 'R', 'O']],
            'D': [['Y', 'Y', 'O'], ['Y', 'Y', 'Y'], ['R', 'Y', 'R']]
        }

        # Yellow line
        yellow_line = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'T': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'R'], ['Y', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        self.assertEqual(checker.yellow_pattern_switch(yellow_cross), 'Yellow Cross')
        self.assertEqual(checker.yellow_pattern_switch(yellow_line), 'Yellow Line')

        


    # TODO !!!
    def test_yellow_dot(self):
        pass

    # TODO !!!
    def test_yellow_L(self):
        pass

    # TODO !!!
    def test_yellow_line(self):
        pass

    # TODO !!!
    def test_yellow_cross(self):
        yellow_cross_correct_edge = {
            'F': [['Y', 'B', 'W'], ['G', 'G', 'O'], ['O', 'G', 'G']],
            'B': [['O', 'W', 'W'], ['B', 'B', 'W'], ['B', 'B', 'B']],
            'L': [['G', 'R', 'G'], ['O', 'O', 'W'], ['Y', 'O', 'B']],
            'R': [['B', 'G', 'W'], ['B', 'R', 'W'], ['Y', 'R', 'W']],
            'T': [['R', 'R', 'G'], ['G', 'W', 'O'], ['R', 'R', 'O']],
            'D': [['Y', 'Y', 'O'], ['Y', 'Y', 'Y'], ['R', 'Y', 'R']]
        }

        yellow_cross_false = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'T': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'R'], ['Y', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        yellow_cross_incorrect_edge = {

        }

        self.assertTrue(checker.yellow_cross(yellow_cross_correct_edge))
        self.assertFalse(checker.yellow_cross(yellow_cross_false))
        #TODO: Implement this test case after checker function is updated
        # self.assertFalse(checker.yellow_cross(yellow_cross_incorrect_edge))

    # TODO !!!
    def test_yellow_edge(self):
        yellow_edge_correct = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'Y']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'G']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['G', 'R', 'R']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['O', 'Y', 'R'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

        self.assertTrue(checker.yellow_edge(yellow_edge_correct))

    # TODO !!!
    def test_yellow_corners(self):
        pass

    # TODO !!!
    def test_yellow_corners_solved(self):
        pass

if __name__ == '__main__':
    unittest.main()