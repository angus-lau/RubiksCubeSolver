import solver
import unittest
import time
from collections import deque

start_state = {
        'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
        'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
        'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['W', 'O', 'R']],
        'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
        'T': [['W', 'W', 'B'], ['R', 'W', 'W'], ['G', 'G', 'G']],
        'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
        }

goal_state = {
    'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
    'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
    'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
    'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
}

allowed_moves = ["T", "T'", "R", "R'", "F", "F'", "L", "L'", "B", "B'", "D", "D'"]

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
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'T'), [])
    #     self.assertEqual(solver.find_white_edge_on_face(test_state, 'D'), [(0,1)])

    # def test_get_adjacent_face_and_sticker(self):
        # self.assertEqual(solver.get_adjacent_face_and_sticker(test_state, 'D', 0, 1), 'G')



if __name__ == '__main__':
    unittest.main()