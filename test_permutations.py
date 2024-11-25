import permutations as perm
import unittest

test_state = {
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

class TestPermutations(unittest.TestCase):
    def test_rotate_face_clockwise(self):
        perm.rotate_face_clockwise('F', test_state)
        self.assertEqual(test_state['F'], expected_clockwise_rotation_state['F'])
        self.assertEqual(test_state['B'], expected_clockwise_rotation_state['B'])
        self.assertEqual(test_state['L'], expected_clockwise_rotation_state['L'])
        self.assertEqual(test_state['R'], expected_clockwise_rotation_state['R'])
        self.assertEqual(test_state['T'], expected_clockwise_rotation_state['T'])
        self.assertEqual(test_state['D'], expected_clockwise_rotation_state['D'])

if __name__ == '__main__':
    unittest.main()