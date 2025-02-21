import permutations as perm
import copy
import unittest

test_state = {
        'F': [['Y', 'W', 'R'], ['G', 'G', 'W'], ['W', 'B', 'R']],
        'B': [['B', 'Y', 'R'], ['R', 'B', 'G'], ['G', 'Y', 'O']],
        'L': [['G', 'O', 'R'], ['O', 'O', 'R'], ['B', 'W', 'O']],
        'R': [['B', 'R', 'O'], ['O', 'R', 'Y'], ['G', 'R', 'O']],
        'U': [['Y', 'B', 'Y'], ['Y', 'W', 'B'], ['B', 'B', 'W']],
        'D': [['G', 'O', 'W'], ['G', 'Y', 'W'], ['W', 'G', 'Y']]
        }

test_state2 = {
        'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
        'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
        'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['W', 'O', 'R']],
        'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
        'U': [['W', 'W', 'B'], ['R', 'W', 'W'], ['G', 'G', 'G']],
        'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
        }

class TestPermutations(unittest.TestCase):
    def test_update_adjacent_faces_F(self):
        res = {
        'F': [['W', 'G', 'Y'], ['B', 'G', 'W'], ['R', 'W', 'R']],
        'B': [['B', 'Y', 'R'], ['R', 'B', 'G'], ['G', 'Y', 'O']],
        'L': [['G', 'O', 'G'], ['O', 'O', 'O'], ['B', 'W', 'W']],
        'R': [['B', 'R', 'O'], ['B', 'R', 'Y'], ['W', 'R', 'O']],
        'U': [['Y', 'B', 'Y'], ['Y', 'W', 'B'], ['O', 'R', 'R']],
        'D': [['G', 'O', 'B'], ['G', 'Y', 'W'], ['W', 'G', 'Y']]
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('F', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['U'], res['U'])
        self.assertEqual(test['D'], res['D'])

    def test_update_adjacent_faces_B(self):
        res = {
        'F': [['Y', 'W', 'R'], ['G', 'G', 'W'], ['W', 'B', 'R']],
        'B': [['R', 'G', 'O'], ['R', 'B', 'O'], ['B', 'Y', 'G']],
        'L': [['W', 'O', 'R'], ['G', 'O', 'R'], ['Y', 'W', 'O']],
        'R': [['B', 'R', 'Y'], ['O', 'R', 'B'], ['G', 'R', 'Y']],
        'U': [['B', 'O', 'G'], ['Y', 'W', 'B'], ['B', 'B', 'W']],
        'D': [['G', 'O', 'W'], ['G', 'Y', 'W'], ['O', 'Y', 'O']]
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('B', test)
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['U'], res['U'])
        self.assertEqual(test['D'], res['D'])
    
    def test_update_adjacent_faces_T(self):
        res = {
        'F': [['B', 'R', 'O'], ['G', 'G', 'W'], ['W', 'B', 'R']],
        'B': [['G', 'O', 'R'], ['R', 'B', 'G'], ['G', 'Y', 'O']],
        'L': [['Y', 'W', 'R'], ['O', 'O', 'R'], ['B', 'W', 'O']],
        'R': [['B', 'Y', 'R'], ['O', 'R', 'Y'], ['G', 'R', 'O']],
        'U': [['Y', 'B', 'Y'], ['Y', 'W', 'B'], ['B', 'B', 'W']],
        'D': [['G', 'O', 'W'], ['G', 'Y', 'W'], ['W', 'G', 'Y']]
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('U', test)
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['D'], res['D'])
    
    def test_update_adjacent_faces_D(self):
        res = {
        'F': [['Y', 'W', 'R'], ['G', 'G', 'W'], ['G', 'R', 'O']],
        'B': [['B', 'Y', 'R'], ['R', 'B', 'G'], ['B', 'W', 'O']],
        'L': [['G', 'O', 'R'], ['O', 'O', 'R'], ['W', 'B', 'R']],
        'R': [['B', 'R', 'O'], ['O', 'R', 'Y'], ['G', 'Y', 'O']],
        'U': [['Y', 'B', 'Y'], ['Y', 'W', 'B'], ['B', 'B', 'W']],
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('D', test)
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['U'], res['U'])
    
    def test_update_adjacent_faces_R(self):
        res = {
        'F': [['Y', 'W', 'W'], ['G', 'G', 'W'], ['W', 'B', 'Y']],
        'B': [['W', 'Y', 'R'], ['B', 'B', 'G'], ['Y', 'Y', 'O']],
        'L': [['G', 'O', 'R'], ['O', 'O', 'R'], ['B', 'W', 'O']],
        'R': [['B', 'R', 'O'], ['O', 'R', 'Y'], ['G', 'R', 'O']],
        'U': [['Y', 'B', 'R'], ['Y', 'W', 'W'], ['B', 'B', 'R']],
        'D': [['G', 'O', 'G'], ['G', 'Y', 'R'], ['W', 'G', 'B']]
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('R', test)
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['U'], res['U'])
    
    def test_update_adjacent_faces_L(self):
        res = {
        'F': [['Y', 'W', 'R'], ['Y', 'G', 'W'], ['B', 'B', 'R']],
        'B': [['B', 'Y', 'W'], ['R', 'B', 'G'], ['G', 'Y', 'G']],
        'R': [['B', 'R', 'O'], ['O', 'R', 'Y'], ['G', 'R', 'O']],
        'U': [['O', 'B', 'Y'], ['G', 'W', 'B'], ['R', 'B', 'W']],
        'D': [['Y', 'O', 'W'], ['G', 'Y', 'W'], ['W', 'G', 'Y']]
        }
        test = copy.deepcopy(test_state)
        perm.update_adjacent_faces('L', test)
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['U'], res['U'])

########################################################################################

    def test_update_adjacent_faces_counterclockwise_F(self):
        res = {
        'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
        'L': [['R', 'Y', 'G'], ['R', 'O', 'G'], ['W', 'O', 'G']],
        'R': [['R', 'O', 'Y'], ['B', 'R', 'B'], ['G', 'B', 'W']],
        'U': [['W', 'W', 'B'], ['R', 'W', 'W'], ['Y', 'B', 'Y']],
        'D': [['W', 'O', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('F', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['U'], res['U'])

    def test_update_adjacent_faces_counterclockwise_B(self):
        res = {
        'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
        'L': [['B', 'Y', 'W'], ['W', 'O', 'O'], ['W', 'O', 'R']],
        'R': [['Y', 'O', 'R'], ['B', 'R', 'G'], ['Y', 'B', 'O']],
        'U': [['Y', 'B', 'W'], ['R', 'W', 'W'], ['G', 'G', 'G']],
        'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['R', 'R', 'W']]
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('B', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['F'], res['F'])
        self.assertEqual(test['U'], res['U'])

    def test_update_adjacent_faces_counterclockwise_T(self):
        res = {
        'F': [['R', 'Y', 'W'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
        'B': [['Y', 'O', 'Y'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
        'L': [['O', 'R', 'G'], ['R', 'O', 'O'], ['W', 'O', 'R']],
        'R': [['O', 'W', 'O'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
        'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('U', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['F'], res['F'])

    def test_update_adjacent_faces_counterclockwise_D(self):
        res = {
        'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['W', 'O', 'R']],
        'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['Y', 'B', 'W']],
        'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['B', 'Y', 'B']],
        'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'Y', 'B']],
        'U': [['W', 'W', 'B'], ['R', 'W', 'W'], ['G', 'G', 'G']],
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('D', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['U'], res['U'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['F'], res['F'])

    def test_update_adjacent_faces_counterclockwise_R(self):
        res = {
        'F': [['O', 'W', 'B'], ['G', 'G', 'W'], ['Y', 'Y', 'G']],
        'B': [['R', 'R', 'G'], ['W', 'B', 'G'], ['R', 'Y', 'B']],
        'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['W', 'O', 'R']],
        'U': [['W', 'W', 'B'], ['R', 'W', 'O'], ['G', 'G', 'O']],
        'D': [['G', 'B', 'O'], ['Y', 'Y', 'R'], ['O', 'G', 'B']]
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('R', test)
        self.assertEqual(test['L'], res['L'])
        self.assertEqual(test['U'], res['U'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['F'], res['F'])

    def test_update_adjacent_faces_counterclockwise_L(self):
        res = {
        'F': [['G', 'W', 'O'], ['Y', 'G', 'R'], ['O', 'Y', 'B']],
        'B': [['O', 'R', 'G'], ['O', 'B', 'R'], ['B', 'Y', 'W']],
        'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
        'U': [['O', 'W', 'B'], ['G', 'W', 'W'], ['Y', 'G', 'G']],
        'D': [['B', 'B', 'R'], ['G', 'Y', 'W'], ['G', 'G', 'R']]
        }
        test = copy.deepcopy(test_state2)
        perm.update_adjacent_faces_counterclockwise('L', test)
        self.assertEqual(test['R'], res['R'])
        self.assertEqual(test['U'], res['U'])
        self.assertEqual(test['D'], res['D'])
        self.assertEqual(test['B'], res['B'])
        self.assertEqual(test['F'], res['F'])

########################################################################################

    def test_rotate_face_clockwise_F(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('F', test)
        self.assertEqual(test['F'], [['Y', 'G', 'O'], ['Y', 'G', 'W'], ['B', 'R', 'O']])

    def test_rotate_face_clockwise_R(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('R', test)
        self.assertEqual(test['R'], [['Y', 'B', 'Y'], ['B', 'R', 'O'], ['W', 'B', 'Y']])
    
    def test_rotate_face_clockwise_L(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('L', test)
        self.assertEqual(test['L'], [['W', 'R', 'R'], ['O', 'O', 'Y'], ['R', 'O', 'W']])

    def test_rotate_face_clockwise_T(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('U', test)
        self.assertEqual(test['U'], [['G', 'R', 'W'], ['G', 'W', 'W'], ['G', 'W', 'B']])

    def test_rotate_face_clockwise_D(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('D', test)
        self.assertEqual(test['D'], [['R', 'W', 'R'], ['B', 'Y', 'G'], ['G', 'Y', 'O']])

    def test_rotate_face_clockwise_B(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_clockwise('B', test)
        self.assertEqual(test['B'], [['G', 'G', 'B'], ['R', 'B', 'Y'], ['O', 'O', 'B']])

########################################################################################

    def test_rotate_face_counter_clockwise_F(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('F', test)
        self.assertEqual(test['F'], [['O', 'R', 'B'], ['W', 'G', 'Y'], ['O', 'G', 'Y']])

    def test_rotate_face_counter_clockwise_R(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('R', test)
        self.assertEqual(test['R'], [['Y', 'B', 'W'], ['O', 'R', 'B'], ['Y', 'B', 'Y']])
    
    def test_rotate_face_counter_clockwise_L(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('L', test)
        self.assertEqual(test['L'], [['W', 'O', 'R'], ['Y', 'O', 'O'], ['R', 'R', 'W']])

    def test_rotate_face_counter_clockwise_T(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('U', test)
        self.assertEqual(test['U'], [['B', 'W', 'G'], ['W', 'W', 'G'], ['W', 'R', 'G']])

    def test_rotate_face_counter_clockwise_D(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('D', test)
        self.assertEqual(test['D'], [['O', 'Y', 'G'], ['G', 'Y', 'B'], ['R', 'W', 'R']])

    def test_rotate_face_counter_clockwise_B(self):
        test = copy.deepcopy(test_state2)
        perm.rotate_face_counter_clockwise('B', test)
        self.assertEqual(test['B'], [['B', 'O', 'O'], ['Y', 'B', 'R'], ['B', 'G', 'G']])
        
if __name__ == '__main__':
    unittest.main()