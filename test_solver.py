import solver
import unittest

test_state = {
            'F': [['W', 'W', 'Y'], ['R', 'G', 'Y'], ['Y', 'G', 'Y']],
            'B': [['G', 'Y', 'G'], ['O', 'B', 'O'], ['R', 'G', 'B']],
            'L': [['W', 'G', 'R'], ['W', 'O', 'B'], ['W', 'G', 'G']],
            'R': [['B', 'W', 'R'], ['R', 'R', 'Y'], ['B', 'O', 'B']],
            'T': [['O', 'B', 'Y'], ['O', 'W', 'R'], ['G', 'B', 'R']],
            'D': [['O', 'Y', 'O'], ['R', 'Y', 'B'], ['O', 'W', 'W']]
        }

class TestSolver(unittest.TestCase):
    #TODO: This doesn't work
    def test_align_bottom_white_edges(self):
        solver.align_bottom_white_edges(test_state)
        self.assertTrue(test_state['D'][2][1])

    # def test_find_white_edge(self):
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'L'), [(1, 0)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'F'), [(0, 1)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'B'), [])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'R'), [(0,1)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'T'), [])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'D'), [(0,1)])

    # def test_get_adjacent_face_and_sticker(self):
        # self.assertEqual(solver.get_adjacent_face_and_sticker(test_state, 'D', 0, 1), 'G')



if __name__ == '__main__':
    unittest.main()