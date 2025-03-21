import time

from .cubes import Coord, Face
from .pieces import Color
from .tables import Tables

class SolutionSolver:
    def __init__(self, facelets):
        self.tables = Tables()
        self.facelets = facelets.upper()

        status = self.verify()
        error_messages = {
            -1: "each colour should appear exactly 9 times",
            -2: "not all edges exist exactly once",
            -3: "one edge should be flipped",
            -4: "not all corners exist exactly once",
            -5: "one corner should be twisted",
            -6: "two corners or edges should be exchanged",
        }
        if status in error_messages:
            raise ValueError(f"Invalid cube configuration: {error_messages[status]}")
        
    def solve(self, max_length=25, timeout=float('inf')):
        self._phase_1_init(max_length)
        self._allowed_length = max_length
        self._timeout = timeout

        # Start IDA*
        for curr_depth in range(self._allowed_length):
            search_res = self._phase_1_search(0, curr_depth)

            if search_res >= 0:
                # Solution has been found
                return self._solution_to_string(search_res)
            
            elif search_res == -2:
                # Search stopped due to time limit
                return -2
            
        # No solution found
        return -1
    
    def verify(self):
        # List to store count of each color
        color_counts = [0] * 6

        try:
            for facelet in self.facelets:
                # Convert each facelet to the respective color index and increase count
                color_counts[Color[facelet]] += 1
        except (IndexError, ValueError):
            return -1
        for i in range(6):
            if color_counts[i] != 9:
                return -1
        
        fc = Face(self.facelets)
        cc = fc.convert_to_cubie()

        return cc.verify()
    
    def _phase_1_init(self, max_length):
        # axis list stores which face is turned at each move
        # power list stores the number of quarter turns
        self.axis = [0] * max_length
        self.power = [0] * max_length

        # phase 1
        # twist, flip, udslice lists store cube state after n moves
        # index[0] represents initial state, index[n] represents state after n moves
        self.twist = [0] * max_length
        self.flip = [0] * max_length
        self.udslice = [0] * max_length

        # phase 2
        # similar to above
        self.corner = [0] * max_length
        self.edge4 = [0] * max_length
        self.edge8 = [0] * max_length

        # these lists store the min number of moves required to reach phase 2, and to reach the solution
        self.min_moves_to_phase_2 = [0] * max_length
        self.min_moves_to_solution = [0] * max_length

        # convert facelet representation to cubie
        self.f = Face(self.facelets)
        self.c = Coord.from_cubie(self.f.convert_to_cubie())

        # store the initial cube state parameters
        self.twist[0] = self.c.twist
        self.flip[0] = self.c.flip
        self.udslice[0] = self.c.udslice
        self.corner[0] = self.c.corner
        self.edge4[0] = self.c.edge4
        self.edge8[0] = self.c.edge8
        
        # get ~min move to reach phase 2 with pruning tables
        self.min_moves_to_phase_2[0] = self._phase_1_cost(0)

    def _phase_2_init(self, num_moves):
        if time.time() > self._timeout:
            # time limit exceeded
            return -2
        # initialize phase 2 from phase 1 solution
        # convert facelet to cubie representation
        cc = self.f.convert_to_cubie()
        # apply all moves from phase 1 to reach current state
        for move_index in range(num_moves):
            for j in range(self.power[move_index]):
                cc.move(self.axis[move_index])

        # store updated phase 2 coords
        self.edge4[num_moves] = cc.edge4
        self.edge8[num_moves] = cc.edge8
        self.corner[num_moves] = cc.corner

        # find min moves to solve cube from this state
        self.min_moves_to_solution[num_moves] = self._phase_2_cost(num_moves)

        # IDA* for phase 2
        for depth in range(self._allowed_length - num_moves):
            solution_moves = self._phase_2_search(num_moves, depth)
            if solution_moves >= 0:
                return solution_moves
            
        # no solution within move limit
        return -1
    
    def _phase_1_cost(self, move_count):

        # return the maximum of the two heuristics calculated from pruning tables
        # so we won't underestimate the required moves 
        return max(
            self.tables.udslice_twist_prune[self.udslice[move_count], self.twist[move_count]],
            self.tables.udslice_flip_prune[self.udslice[move_count], self.flip[move_count]],
        )
    
    def _phase_2_cost(self, move_count):
        
        # same as above
        return max(
            self.tables.edge4_corner_prune[self.edge4[move_count], self.corner[move_count]],
            self.tables.edge4_edge8_prune[self.edge4[move_count], self.edge8[move_count]],
        )

    def _phase_1_search(self, move_count, search_depth):
        if time.time() > self._timeout:
            # timeout exceeded
            return -2
        
        # check if current state is phase 2 ready
        elif self.min_moves_to_phase_2[move_count] == 0:
            return self._phase_2_init(move_count)
        
        # if heuristic is within search depth, search through tree
        elif self.min_moves_to_phase_2[move_count] <= search_depth:

            # search through each of the six faces
            for face_index in range(6):
                # avoid redundant moves e.g repeating or opposite moves 
                if move_count > 0 and self.axis[move_count - 1] in (face_index, face_index + 3):
                    continue
                    
                # try each possible turn for the face. 1=90, 2 = 180, 3 = -90
                for turn_count in range(1, 4):
                    self.axis[move_count] = face_index
                    self.power[move_count] = turn_count

                    # compute move_id to locate on move tables
                    move_id = 3 * face_index + turn_count - 1

                    # use move tables to get new state after move
                    self.twist[move_count + 1] = self.tables.twist_move[self.twist[move_count]][move_id]
                    self.flip[move_count + 1] = self.tables.flip_move[self.flip[move_count]][move_id]
                    self.udslice[move_count + 1] = self.tables.udslice_move[self.udslice[move_count]][move_id]

                    # find new heuristic estimate after this move
                    self.min_moves_to_phase_2[move_count + 1] = self._phase_1_cost(move_count + 1)

                    # search resursively from new state
                    next_search_res = self._phase_1_search(move_count + 1, search_depth - 1)

                    # found solution, return result
                    if next_search_res >= 0:
                        return next_search_res
                    
                    # exceeded time limit
                    if next_search_res == -2:
                        return -2
        # no solution found
        return -1

    def _phase_2_search(self, move_count, search_depth):
        # same as above
        if self.min_moves_to_solution[move_count] == 0:
            return move_count
        
        # same as above
        elif self.min_moves_to_solution[move_count] <= search_depth:
            for face_index in range(6):
                if move_count > 0 and self.axis[move_count - 1] in (face_index, face_index + 3):
                    continue
                # Only half turns 180deg for R, F, L, B (1, 2, 4, 5)
                for turn_count in range(1, 4):
                    if face_index in [1, 2, 4, 5] and turn_count != 2:
                        continue
                    # same as above
                    self.axis[move_count] = face_index
                    self.power[move_count] = turn_count

                    # same as above
                    move_id = 3 * face_index + turn_count - 1
        
                    # same as above but to update phase 2 coords
                    self.edge4[move_count + 1] = self.tables.edge4_move[self.edge4[move_count]][move_id]
                    self.edge8[move_count + 1] = self.tables.edge8_move[self.edge8[move_count]][move_id]
                    self.corner[move_count + 1] = self.tables.corner_move[self.corner[move_count]][move_id]

                    # same as above
                    self.min_moves_to_solution[move_count + 1] = self._phase_2_cost(move_count + 1)

                    # same as above
                    next_search_res = self._phase_2_search(move_count + 1, search_depth - 1)

                    # found solution
                    if next_search_res >= 0:
                        return next_search_res
        # no solution found
        return -1

    def _solution_to_string(self, move_count):
        def format_move(axis_power):
            # convert numerical axis_power value into standard notation
            axis, power = axis_power
            # convert numerical axis value to corresponding face character
            face_notation = Color(axis).name

            # append correct move notation
            if power == 1:
                return face_notation 
            if power == 2:
                return face_notation + "2" 
            if power == 3:
                return face_notation + "'" 
            
            # unexpected move values
            raise RuntimeError(f'Invalid move encoding: axis={axis}, power={power}')
        
        # get move sequence by converting each move into notation
        solution_moves = map(format_move, zip(self.axis[:move_count], self.power[:move_count]))

        # return solution
        return " ".join(solution_moves) 