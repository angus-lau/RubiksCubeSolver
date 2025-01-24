import permutations as perm
import unittest

class TestPermutations(unittest.TestCase):
    test_state = {
        'F': [['G', 'G', 'O'], ['B', 'G', 'R'], ['Y', 'O', 'R']],
        'B': [['R', 'B', 'W'], ['R', 'B', 'O'], ['B', 'Y', 'G']],
        'L': [['R', 'R', 'R'], ['B', 'O', 'W'], ['O', 'O', 'G']],
        'R': [['W', 'G', 'B'], ['B', 'R', 'Y'], ['G', 'O', 'Y']],
        'T': [['B', 'Y', 'Y'], ['W', 'W', 'R'], ['Y', 'W', 'B']],
        'D': [['O', 'Y', 'W'], ['G', 'Y', 'W'], ['W', 'G', 'O']]
        }
    
    def test_rotate_face_clockwise(self):
        test_state1 = {
            'F': [['Y', 'B', 'R'], ['Y', 'G', 'Y'], ['O', 'B', 'O']],
            'B': [['B', 'G', 'W'], ['Y', 'B', 'Y'], ['G', 'B', 'O']],
            'L': [['R', 'W', 'R'], ['G', 'O', 'O'], ['W', 'G', 'W']],
            'R': [['G', 'O', 'O'], ['R', 'R', 'B'], ['G', 'O', 'R']],
            'T': [['B', 'R', 'Y'], ['R', 'W', 'W'], ['B', 'R', 'Y']],
            'D': [['B', 'O', 'Y'], ['W', 'Y', 'G'], ['G', 'W', 'W']]
        }
        expected_clockwise_rotation_state = {
            'F': [['O', 'Y', 'Y'], ['B', 'G', 'B'], ['O', 'Y', 'R']],
            'B': [['B', 'G', 'W'], ['Y', 'B', 'Y'], ['G', 'B', 'O']],
            'L': [['R', 'W', 'B'], ['G', 'O', 'O'], ['W', 'G', 'Y']],
            'R': [['B', 'O', 'O'], ['R', 'R', 'B'], ['Y', 'O', 'R']],
            'T': [['B', 'R', 'Y'], ['R', 'W', 'W'], ['W', 'O', 'R']],
            'D': [['G', 'R', 'G'], ['W', 'Y', 'G'], ['G', 'W', 'W']]
        }
    
        perm.rotate_face_clockwise('F', test_state1)
        self.assertEqual(test_state1['B'], expected_clockwise_rotation_state['B'])
        self.assertEqual(test_state1['F'], expected_clockwise_rotation_state['F'])
        self.assertEqual(test_state1['L'], expected_clockwise_rotation_state['L'])
        self.assertEqual(test_state1['R'], expected_clockwise_rotation_state['R'])
        self.assertEqual(test_state1['T'], expected_clockwise_rotation_state['T'])
        self.assertEqual(test_state1['D'], expected_clockwise_rotation_state['D'])

    def test_rotate_face_counter_clockwise(self):
        test_state = {
            'F': [['G', 'G', 'O'], ['B', 'G', 'R'], ['Y', 'O', 'R']],
            'B': [['R', 'B', 'W'], ['R', 'B', 'O'], ['B', 'Y', 'G']],
            'L': [['R', 'R', 'R'], ['B', 'O', 'W'], ['O', 'O', 'G']],
            'R': [['W', 'G', 'B'], ['B', 'R', 'Y'], ['G', 'O', 'Y']],
            'T': [['B', 'Y', 'Y'], ['W', 'W', 'R'], ['Y', 'W', 'B']],
            'D': [['O', 'Y', 'W'], ['G', 'Y', 'W'], ['W', 'G', 'O']]
        }
        expected_counter_clockwise_rotation_state = {
            'F': [['O', 'R', 'R'], ['G', 'G', 'O'], ['G', 'B', 'Y']],
            'B': [['R', 'B', 'W'], ['R', 'B', 'O'], ['B', 'Y', 'G']],
            'L': [['R', 'R', 'B'], ['B', 'O', 'W'], ['O', 'O', 'Y']],
            'R': [['W', 'G', 'B'], ['Y', 'R', 'Y'], ['O', 'O', 'Y']],
            'T': [['B', 'Y', 'Y'], ['W', 'W', 'R'], ['W', 'B', 'G']],
            'D': [['R', 'W', 'G'], ['G', 'Y', 'W'], ['W', 'G', 'O']]
        }

        perm.rotate_face_counter_clockwise('F', test_state)
        self.assertEqual(test_state['L'], expected_counter_clockwise_rotation_state['L'])
        self.assertEqual(test_state['B'], expected_counter_clockwise_rotation_state['B'])
        self.assertEqual(test_state['F'], expected_counter_clockwise_rotation_state['F'])
        self.assertEqual(test_state['R'], expected_counter_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_counter_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_counter_clockwise_rotation_state['D'])

    def test_rotate_face_counter_clockwise_B(self):
        test_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        expected_B_counter_clockwise_rotation_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['W', 'B', 'R'], ['G', 'B', 'R'], ['G', 'G', 'G']],
            'L': [['Y', 'Y', 'R'], ['G', 'O', 'W'], ['Y', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'Y'], ['Y', 'B', 'R']],
            'T': [['B', 'W', 'R'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['O', 'W', 'W']]
        }

        perm.rotate_face_counter_clockwise('B', test_state)
        self.assertEqual(test_state['L'], expected_B_counter_clockwise_rotation_state['L'])
        self.assertEqual(test_state['B'], expected_B_counter_clockwise_rotation_state['B'])
        self.assertEqual(test_state['F'], expected_B_counter_clockwise_rotation_state['F'])
        self.assertEqual(test_state['R'], expected_B_counter_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_B_counter_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_B_counter_clockwise_rotation_state['D'])
        
    def test_rotate_top_clockwise(self):
        test_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        expected_top_clockwise_rotation_state = {
            'F': [['O', 'R', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['O', 'Y', 'R'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['G', 'G', 'B'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['R', 'R', 'G'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'O', 'Y'], ['O', 'W', 'G'], ['W', 'Y', 'Y']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        perm.rotate_top_clockwise(test_state)
        self.assertEqual(test_state['L'], expected_top_clockwise_rotation_state['L'])
        self.assertEqual(test_state['B'], expected_top_clockwise_rotation_state['B'])
        self.assertEqual(test_state['F'], expected_top_clockwise_rotation_state['F'])
        self.assertEqual(test_state['R'], expected_top_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_top_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_top_clockwise_rotation_state['D'])


    def test_rotate_top_counter_clockwise(self):
        test_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        expected_top_counter_clockwise_rotation_state = {
            'F': [['O', 'Y', 'R'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['O', 'R', 'B'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['R', 'R', 'G'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['G', 'G', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'Y', 'W'], ['G', 'W', 'O'], ['Y', 'O', 'Y']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        perm.rotate_top_counter_clockwise(test_state)
        self.assertEqual(test_state['B'], expected_top_counter_clockwise_rotation_state['B'])
        self.assertEqual(test_state['L'], expected_top_counter_clockwise_rotation_state['L'])
        self.assertEqual(test_state['F'], expected_top_counter_clockwise_rotation_state['F'])
        self.assertEqual(test_state['R'], expected_top_counter_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_top_counter_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_top_counter_clockwise_rotation_state['D'])

    def test_rotate_bottom_clockwise(self):
        test_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
            'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
            'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
            'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
        }
        expected_bottom_clockwise_rotation_state = {
            'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['Y', 'B', 'R']],
            'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'B', 'G']],
            'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['O', 'W', 'O']],
            'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['W', 'G', 'G']],
            'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
            'D': [['B', 'Y', 'B'], ['O', 'Y', 'Y'], ['W', 'O', 'R']]
        }
        perm.rotate_bottom_counter_clockwise(test_state)
        self.assertEqual(test_state['B'], expected_bottom_clockwise_rotation_state['B'])
        self.assertEqual(test_state['L'], expected_bottom_clockwise_rotation_state['L'])
        self.assertEqual(test_state['F'], expected_bottom_clockwise_rotation_state['F'])
        self.assertEqual(test_state['R'], expected_bottom_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_bottom_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_bottom_clockwise_rotation_state['D'])

    # def test_rotate_bottom_counter_clockwise(self):
    #     test_state = {
    #         'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
    #         'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
    #         'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
    #         'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
    #         'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
    #         'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
    #     }
    #     expected_bottom_counter_clockwise_state = {
    #         'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['W', 'B', 'G']],
    #         'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['Y', 'B', 'R']],
    #         'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'G', 'G']],
    #         'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['O', 'W', 'O']],
    #         'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
    #         'D': [['R', 'O', 'W'], ['Y', 'Y', 'O'], ['B', 'Y', 'B']]
    #     }
    #     perm.rotate_bottom_counter_clockwise(test_state)
    #     self.assertEqual(test_state['B'], expected_bottom_counter_clockwise_state['B'])
    #     self.assertEqual(test_state['L'], expected_bottom_counter_clockwise_state['L'])
    #     self.assertEqual(test_state['F'], expected_bottom_counter_clockwise_state['F'])
    #     self.assertEqual(test_state['R'], expected_bottom_counter_clockwise_state['R'])
    #     self.assertEqual(test_state['T'], expected_bottom_counter_clockwise_state['T'])
    #     self.assertEqual(test_state['D'], expected_bottom_counter_clockwise_state['D'])

    # def test_rotate_right_column_clockwise(self):
    #     test_state = {
    #         'F': [['G', 'G', 'B'], ['R', 'G', 'R'], ['O', 'W', 'O']],
    #         'B': [['R', 'R', 'G'], ['B', 'B', 'G'], ['W', 'G', 'G']],
    #         'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
    #         'R': [['O', 'R', 'B'], ['B', 'R', 'W'], ['Y', 'B', 'R']],
    #         'T': [['Y', 'G', 'Y'], ['O', 'W', 'Y'], ['Y', 'O', 'W']],
    #         'D': [['W', 'O', 'B'], ['O', 'Y', 'Y'], ['R', 'Y', 'B']]
    #     }

    #     expected_right_column_clockwise_state = {
    #         'F': [['G', 'G', 'B'], ['R', 'G', 'Y'], ['O', 'W', 'B']],
    #         'B': [['W', 'R', 'G'], ['Y', 'B', 'G'], ['Y', 'G', 'G']],
    #         'L': [['O', 'Y', 'R'], ['W', 'O', 'W'], ['W', 'B', 'G']],
    #         'R': [['Y', 'B', 'O'], ['B', 'R', 'R'], ['R', 'W', 'B']],
    #         'T': [['Y', 'G', 'B'], ['O', 'W', 'R'], ['Y', 'O', 'O']],
    #         'D': [['W', 'O', 'W'], ['O', 'Y', 'B'], ['R', 'Y', 'R']]
    #     }
    #     perm.rotate_right_column_clockwise(test_state)
    #     self.assertEqual(test_state['B'], expected_right_column_clockwise_state['B'])
    #     self.assertEqual(test_state['L'], expected_right_column_clockwise_state['L'])
    #     self.assertEqual(test_state['F'], expected_right_column_clockwise_state['F'])
    #     self.assertEqual(test_state['R'], expected_right_column_clockwise_state['R'])
    #     self.assertEqual(test_state['T'], expected_right_column_clockwise_state['T'])
    #     self.assertEqual(test_state['D'], expected_right_column_clockwise_state['D'])
        
if __name__ == '__main__':
    unittest.main()