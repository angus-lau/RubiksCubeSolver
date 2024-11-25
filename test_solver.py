import solver
import unittest

test_state = {
            'F': [['G', 'G', 'W'], ['Y', 'G', 'Y'], ['O', 'B', 'O']],
            'B': [['R', 'G', 'W'], ['W', 'B', 'Y'], ['Y', 'B', 'O']],
            'L': [['R', 'W', 'R'], ['G', 'O', 'O'], ['W', 'G', 'W']],
            'R': [['G', 'R', 'B'], ['R', 'R', 'O'], ['G', 'B', 'O']],
            'T': [['B', 'R', 'Y'], ['R', 'W', 'B'], ['Y', 'O', 'R']],
            'D': [['B', 'O', 'Y'], ['W', 'Y', 'Y'], ['G', 'W', 'B']]
        }

class TestSolver(unittest.TestCase):
    def test_align_bottom_white_edges(self):
        solver.align_bottom_white_edges(test_state)
        self.assertEqual(test_state['D'][2][1], 'W')
        self.assertEqual(test_state['F'][0][1], 'W')
        self.assertEqual(test_state['R'][0][1], 'W')
        self.assertEqual(test_state['B'][2][1], 'W')
        self.assertEqual(test_state['L'][0][1], 'W')

if __name__ == '__main__':
    unittest.main()