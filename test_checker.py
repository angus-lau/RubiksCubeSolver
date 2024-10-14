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

    # TODO !!!
    def test_middle_edge(self):
        pass

    # TODO !!!
    def test_yellow_pattern_switch(self):
        pass

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
        pass

    # TODO !!!
    def test_yellow_edge(self):
        pass

    # TODO !!!
    def test_yellow_corners(self):
        pass

    # TODO !!!
    def test_yellow_corners_solved(self):
        pass

if __name__ == '__main__':
    unittest.main()