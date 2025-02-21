import solver
import unittest
from collections import deque

start_state = {
    'F': [['R', 'R', 'Y'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
    'L': [['O', 'G', 'G'], ['O', 'O', 'O'], ['O', 'O', 'O']],
    'R': [['B', 'B', 'W'], ['R', 'R', 'W'], ['R', 'R', 'R']],
    'U': [['W', 'W', 'G'], ['W', 'W', 'R'], ['W', 'W', 'R']],
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'B']]
}

goal_state = {
    'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
    'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
    'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
    'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
}

allowed_moves = ['U', 'R', 'L', 'B', 'F', 'D']

class TestSolver(unittest.TestCase):
    # def get_cube_state_to_string(cube):
    #     return "".join("".join(row) for face in cube.values() for row in face)
    # def test_solution(self):
    #     # solution = solver.bidirectional_search(start_state, goal_state, allowed_moves)
    #     # print("Solution found:", solution)
    #     test_queue = deque([(start_state, [])])  # Queue with the starting state
    #     test_visited = {solver.get_cube_state_to_string(start_state): []}  # Visited dictionary
    #     test_opposite_visited = {}  # Assume no opposite direction yet
    #     test_moves = ["T", "T'", "R", "R'", "F", "F'", "D", "D'", "L", "L'"]  # Basic moves

    #     # Test search_step() once
    #     solver.search_step(test_queue, test_visited, test_opposite_visited, test_moves)
    # # def test_align_top_white_edge(self):

    def test_solve(self):


        solution = solver.bidirectional_search(start_state, goal_state, allowed_moves)
        if solution is not None:
            print("Final solution:", solution)
        else:
            print("No solution found.")

    # def test_find_white_edge(self):
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'L'), [(1, 0)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'F'), [(0, 1)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'B'), [])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'R'), [(0,1)])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'U'.), [])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'D'), [(0,1)])

    # def test_get_adjacent_face_and_sticker(self):
        # self.assertEqual(solver.get_adjacent_face_and_sticker(test_state, 'D', 0, 1), 'G')



if __name__ == '__main__':
    unittest.main()