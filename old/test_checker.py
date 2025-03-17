import unittest
import old.checker as checker

class TestChecker(unittest.TestCase):
    def test_white_cross_check(self):
        # No white cross
        no_white_cross = {
            'F': [['R', 'B', 'R'], ['O', 'G', 'Y'], ['Y', 'G', 'O']],
            'B': [['O', 'Y', 'R'], ['Y', 'B', 'R'], ['R', 'W', 'Y']],
            'L': [['B', 'G', 'B'], ['B', 'O', 'Y'], ['O', 'O', 'O']],
            'R': [['G', 'G', 'B'], ['G', 'R', 'B'], ['W', 'O', 'W']],
            'U': [['W', 'R', 'W'], ['O', 'W', 'R'], ['Y', 'W', 'Y']],
            'D': [['B', 'W', 'G'], ['B', 'Y', 'W'], ['G', 'R', 'G']]
        }
        # White cross with correct edge pieces
        white_cross_correct_edge = {
            'F': [['W', 'G', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'B', 'Y'], ['Y', 'B', 'R'], ['B', 'G', 'Y']],
            'L': [['G', 'O', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'U': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
            'D': [['W', 'O', 'W'], ['R', 'Y', 'B'], ['R', 'Y', 'W']]
        }
        # White cross with incorrect edge pieces
        white_cross_incorrect_edge = {
            'F': [['W', 'R', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'O', 'Y'], ['Y', 'B', 'R'], ['B', 'W', 'Y']],
            'L': [['G', 'G', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'B', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'U': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
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
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'R', 'Y'], ['R', 'Y', 'Y'], ['O', 'Y', 'Y']]
        }

        # White corners with incorrect corner pieces
        white_corners_false = {
            'F': [['W', 'G', 'Y'], ['Y', 'G', 'O'], ['O', 'G', 'B']],
            'B': [['R', 'B', 'Y'], ['Y', 'B', 'R'], ['B', 'G', 'Y']],
            'L': [['G', 'O', 'R'], ['G', 'O', 'R'], ['G', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['Y', 'R', 'B'], ['R', 'O', 'O']],
            'U': [['O', 'W', 'Y'], ['W', 'W', 'W'], ['G', 'W', 'B']],
            'D': [['W', 'O', 'W'], ['R', 'Y', 'B'], ['R', 'Y', 'W']]
        }

        # White corners with wrong corner pieces
        white_corners_wrong_corner = {
            'F': [['R', 'G', 'O'], ['Y', 'G', 'Y'], ['G', 'B', 'Y']],
            'B': [['O', 'B', 'R'], ['Y', 'B', 'G'], ['Y', 'B', 'G']],
            'L': [['B', 'O', 'G'], ['R', 'O', 'G'], ['R', 'O', 'O']],
            'R': [['G', 'R', 'B'], ['R', 'R', 'O'], ['B', 'B', 'B']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
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
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'R'], ['G', 'Y', 'Y'], ['R', 'R', 'Y']]
        }

        # Middle layer with 2 incorrect edge pieces
        middle_edge_two_false = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'O'], ['B', 'Y', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['O', 'O', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'R'], ['G', 'R', 'Y']],
            'R': [['R', 'R', 'R'], ['G', 'R', 'R'], ['B', 'B', 'Y']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['O', 'G', 'Y'], ['Y', 'Y', 'Y'], ['R', 'Y', 'G']]
        }

        # Middle layer wiht all wrong edge pieces
        middle_edge_false = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'O'], ['R', 'R', 'G']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'Y'], ['B', 'Y', 'Y']],
            'L': [['O', 'O', 'O'], ['R', 'O', 'R'], ['B', 'O', 'G']],
            'R': [['R', 'R', 'R'], ['G', 'R', 'Y'], ['Y', 'Y', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'B', 'O'], ['B', 'Y', 'O'], ['O', 'G', 'Y']]
        }

        self.assertTrue(checker.middle_edge(middle_edge_correct))
        self.assertFalse(checker.middle_edge(middle_edge_two_false))
        self.assertFalse(checker.middle_edge(middle_edge_false))

    def test_yellow_pattern_switch(self):
        yellow_cross = {
            'F': [['Y', 'B', 'W'], ['G', 'G', 'O'], ['O', 'G', 'G']],
            'B': [['O', 'W', 'W'], ['B', 'B', 'W'], ['B', 'B', 'B']],
            'L': [['G', 'R', 'G'], ['O', 'O', 'W'], ['Y', 'O', 'B']],
            'R': [['B', 'G', 'W'], ['B', 'R', 'W'], ['Y', 'R', 'W']],
            'U': [['R', 'R', 'G'], ['G', 'W', 'O'], ['R', 'R', 'O']],
            'D': [['Y', 'Y', 'O'], ['Y', 'Y', 'Y'], ['R', 'Y', 'R']]
        }

        yellow_line = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'R'], ['Y', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        yellow_L = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['G', 'G', 'O'], ['B', 'Y', 'Y'], ['B', 'Y', 'O']]
        }

        yellow_dot = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['G', 'G', 'O'], ['B', 'Y', 'B'], ['O', 'B', 'O']]
        }

        self.assertEqual(checker.yellow_pattern_switch(yellow_cross), 'Yellow Cross')
        self.assertEqual(checker.yellow_pattern_switch(yellow_line), 'Yellow Line')
        self.assertEqual(checker.yellow_pattern_switch(yellow_L), 'Yellow L')
        self.assertEqual(checker.yellow_pattern_switch(yellow_dot), 'Yellow Dot')

    def test_yellow_dot(self):
        yellow_dot_false = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['Y', 'Y', 'R'], ['O', 'Y', 'R'], ['G', 'R', 'R']]
        }

        yellow_dot = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['G', 'G', 'O'], ['B', 'Y', 'B'], ['O', 'B', 'O']]
        }
        self.assertTrue(checker.yellow_dot(yellow_dot))
        self.assertFalse(checker.yellow_dot(yellow_dot_false))

    # TODO check if the yellow L can be oriented differently when arriving at this step
    def test_yellow_L(self):
        yellow_L = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['G', 'G', 'O'], ['B', 'Y', 'Y'], ['B', 'Y', 'O']]
        }

        yellow_L_false = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'Y', 'Y'], ['R', 'Y', 'R'], ['G', 'R', 'R']]
        }

        self.assertTrue(checker.yellow_L(yellow_L))
        self.assertFalse(checker.yellow_L(yellow_L_false))

    def test_yellow_line(self):
        yellow_line = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'R'], ['Y', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        yellow_line_false = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'Y'], ['R', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        self.assertTrue(checker.yellow_line(yellow_line))
        self.assertFalse(checker.yellow_line(yellow_line_false))

    def test_yellow_cross(self):
        yellow_cross_correct_edge = {
            'F': [['Y', 'B', 'W'], ['G', 'G', 'O'], ['O', 'G', 'G']],
            'B': [['O', 'W', 'W'], ['B', 'B', 'W'], ['B', 'B', 'B']],
            'L': [['G', 'R', 'G'], ['O', 'O', 'W'], ['Y', 'O', 'B']],
            'R': [['B', 'G', 'W'], ['B', 'R', 'W'], ['Y', 'R', 'W']],
            'U': [['R', 'R', 'G'], ['G', 'W', 'O'], ['R', 'R', 'O']],
            'D': [['Y', 'Y', 'O'], ['Y', 'Y', 'Y'], ['R', 'Y', 'R']]
        }

        yellow_cross_false = {
            'F': [['G', 'G', 'O'], ['O', 'G', 'G'], ['W', 'B', 'Y']],
            'B': [['B', 'B', 'B'], ['W', 'B', 'B'], ['W', 'W', 'O']],
            'L': [['W', 'R', 'Y'], ['W', 'O', 'B'], ['W', 'O', 'B']],
            'R': [['B', 'G', 'Y'], ['W', 'R', 'O'], ['G', 'R', 'G']],
            'U': [['R', 'Y', 'R'], ['G', 'W', 'O'], ['O', 'Y', 'Y']],
            'D': [['O', 'R', 'R'], ['Y', 'Y', 'Y'], ['G', 'R', 'R']]
        }

        yellow_cross_incorrect_edge = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['R', 'R', 'Y']],
            'L': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'B', 'Y']],
            'R': [['G', 'G', 'G'], ['G', 'R', 'G'], ['Y', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['B', 'Y', 'G'], ['Y', 'Y', 'Y'], ['G', 'Y', 'B']]
        }

        self.assertTrue(checker.yellow_cross(yellow_cross_correct_edge))
        self.assertFalse(checker.yellow_cross(yellow_cross_false))
        self.assertFalse(checker.yellow_cross(yellow_cross_incorrect_edge))

    def test_yellow_edge(self):
        yellow_edge_correct = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'Y']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'G']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['G', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['O', 'Y', 'R'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

        yellow_cross_incorrect_edge = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['R', 'R', 'Y']],
            'L': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'B', 'Y']],
            'R': [['G', 'G', 'G'], ['G', 'R', 'G'], ['Y', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['B', 'Y', 'G'], ['Y', 'Y', 'Y'], ['G', 'Y', 'B']]
        }

        self.assertTrue(checker.yellow_all_edge(yellow_edge_correct))
        self.assertFalse(checker.yellow_all_edge(yellow_cross_incorrect_edge))

    def test_yellow_edge_two(self):
        yellow_cross_two_correct_edge = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['R', 'R', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'B', 'Y']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['B', 'Y', 'G'], ['Y', 'Y', 'Y'], ['G', 'Y', 'B']]
        }

        yellow_cross_one_correct_edge = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'O', 'O']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['Y', 'B', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['R', 'R', 'Y']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'G', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'Y', 'B'], ['Y', 'Y', 'Y'], ['B', 'Y', 'G']]
        }

        self.assertTrue(checker.yellow_adjacent_edge(yellow_cross_two_correct_edge))
        self.assertFalse(checker.yellow_adjacent_edge(yellow_cross_one_correct_edge))

    def test_yellow_opposite_edge(self):
        yellow_opposite_edge_correct = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['R', 'B', 'B']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['G', 'G', 'R']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['B', 'O', 'G']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['O', 'R', 'O']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

        yellow_opposite_edge_incorrect = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'O', 'O']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['Y', 'B', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['Y', 'Y', 'Y']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['G', 'G', 'G']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'Y', 'G'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'G']]
        }

        self.assertTrue(checker.yellow_opposite_edge(yellow_opposite_edge_correct))
        self.assertFalse(checker.yellow_opposite_edge(yellow_opposite_edge_incorrect))


    def test_yellow_corners(self):
        yellow_corners_correct_spot = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'Y']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'Y', 'G'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }
        yellow_corners_incorrect_spot = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['Y', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['G', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['Y', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'R', 'O']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['B', 'Y', 'G'], ['Y', 'Y', 'Y'], ['R', 'Y', 'Y']]
        }
        
        self.assertTrue(checker.yellow_corners(yellow_corners_correct_spot))
        self.assertFalse(checker.yellow_corners(yellow_corners_incorrect_spot))

    def test_yellow_corners_solved(self):
        yellow_corners_correct_spot_unsolved = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['O', 'G', 'R']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'Y']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['Y', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['G', 'Y', 'G'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

        yellow_corners_solved = {
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

        self.assertFalse(checker.yellow_corners_solved(yellow_corners_correct_spot_unsolved))
        self.assertTrue(checker.yellow_corners_solved(yellow_corners_solved))



if __name__ == '__main__':
    unittest.main()