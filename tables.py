import json
import os

from .cubes.cubie import Cubie, MOVE_CUBE

class Pruning():
    # initialize pruning table
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns
    # Access elements in pruning with 2D-style indexing
    def __getitem__(self, x):
        return self.table[x[0] * self.columns + x[1]]
    
class Tables:
    # CONSTANTS
    _loaded_tables = False
    TWIST = 2187
    FLIP = 2048
    UDSLICE = 495
    EDGE4 = 24
    EDGE8 = 40320
    CORNER = 40320
    EDGE = 479001600
    MOVES = 18

    def __init__(self):
        if not self._loaded_tables:
            self.load_tables()
    
    @classmethod
    def load_tables(self):
        if os.path.isfile('tables.json'):
            with open('tables.json', 'r') as f:
                tables = json.load(f)
            self.tm = tables['tm']
            self.fm = tables['fm']
            self.usm = tables['usm']
            self.e4 = tables['e4']
            self.e8 = tables['e8']
            self.cm = tables['cm']
            self.ust_prune = Pruning(tables['ust'], self.TWIST)
            self.usf_prune = Pruning(tables['usf'], self.FLIP)
            self.e4e8_prune = Pruning(tables['e4e8'], self.EDGE8)
            self.e4c_prune = Pruning(tables['e4c'], self.CORNER)
        else:
            # Move tables
            self.tm = self.make_twist_table()
            self.fm = self.make_flip_table()
            self.usm = self.make_udslice_table()

            self.e4 = self.make_edge4_table()
            self.e8 = self.make_edge8_table()
            self.cm = self.make_corner_table()

            # Pruning tables
            self.ust_prune = self.make_ust_prune()
            self.usf_prune = self.make_usf_prune()

            self.e4e8_prune = self.make_e4e8_prune()
            self.e4c_prune = self.make_e4c_prune()

            tables = {
                'tm': self.tm,
                'fm': self.fm,
                'usm': self.usm,
                'e4': self.e4,
                'e8': self.e8,
                'cm': self.cm,
                'ust_prune': self.ust_prune.table,
                'usf_prune': self.usf_prune.table,
                'e4e8': self.e4e8_prune.table,
                'e4c': self.e4c_prune.table,
            }
            with open('tables.json', 'w') as f:
                json.dump(tables, f)
        self._loaded_tables_ = True

    @classmethod
    def make_twist_table(self):
        # Create 2D list initialized with zeros. Outer list has self.TWIST rows (one for each twist state). Each row has cls.MOVES columns (one for each move in the move set). Fill table with twist
        # state after each move. 
        # TS|M0|M1|M2 ...
        # ------------
        # self.MOVES represents the total # of moves, self.FLIP represents the total # of possible edge states
        tm = [[0] * self.MOVES for _ in range(self.TWIST)]
        a = Cubie()

        # Loop over all possible twist states, and set the cube's current state to i, so we can track how moves affect it. 
        for i in range(self.TWIST):
            a.twist = i
            # Loop over MOVE_CUBE list, where each move is a predefined face turn. Enumerate gives index of move, move is the actual move used 
            for face_index, move in enumerate(MOVE_CUBE):
                # Each face move can be applied up to 3 times (quarter-turns) k = 0 -> apply move once (90), k=1 -> apply move again (180), k=2  -> apply move a 3rd time (270)
                for rotation_count in range(3):
                    a.corner_transformation(move)
                    # Store the resulting twist state in the table
                    tm[i][3 * face_index + rotation_count] = a.twist
                # Reset move after 3 times. 
                a.corner_transformation(move)
        return tm

    @classmethod
    def make_flip_table(self):
        ft = [[0] * self.MOVES for _ in range(self.FLIP)]
        a = Cubie()

        for i in range(self.FLIP):
            a.flip = i
            # Loop over 6 possible face moves
            for face_index in range(6):
                # Apply the same face move 3 times over, and store each new flip state
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    ft[i][3 * face_index + rotation_count] = a.flip
                # Reset flips after 3 times
                a.edge_transformation(MOVE_CUBE[face_index])
        return ft
    
    @classmethod
    def make_udslice_table(self):
        usm = [[0] * self.MOVES for _ in range(self.UDSLICE)]
        a = Cubie()
        for i in range(self.UDSLICE):
            a.udslice = i
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    usm[i][3 * face_index + rotation_count] = a.udslice
                a.edge_transformation(MOVE_CUBE[face_index])
        return usm
    
    @classmethod
    def make_edge4_table(self):
        e4 = [[0] * self.MOVES for _ in range(self.EDGE4)]
        a = Cubie()
        # Loop over all possible edges
        for i in range(self.EDGE4):
            # setting i so that we can track how it changes when moves are applied
            a.edge4 = i
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    e4[i][3 * face_index + rotation_count] = -1 if (rotation_count % 2 == 0 
                                                                    and face_index % 3 != 0) else a.edge4
                a.edge_transformation(MOVE_CUBE[face_index])
        return e4
    
    @classmethod
    def make_edge8_table(self):
        e8 = [[0] * self.MOVES for _ in range(self.EDGE8)]
        a = Cubie()

        for i in range(self.EDGE8):
            a.edge8 = i 
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    # Determine what value to store in the lookup table.
                    # If the move is applied an even # of times (1st or 3rd move)
                    # AND the face index is not a multiple of 3 (excluding U and F moves),
                    # store -1 to show invalid state transition
                    # otherwise, store the updated e4 state in lookup table
                    e8[i][3 * face_index + rotation_count] = -1 if (rotation_count % 2 == 0
                                                                    and face_index % 3 != 0) else a.edge8
                # apply move one more time to return cube back to original state
                a.edge_transformation(MOVE_CUBE[face_index])
        return e8

    @classmethod
    def make_corner_table(self):
        cm = [[0] * self.MOVES for _ in range(self.CORNER)]
        a = Cubie()
        for i in range(self.CORNER):
            a.corner = i
            for face_index in range(6):
                for rotation_count in range(3):
                    a.corner_transformation(MOVE_CUBE[face_index])
                    cm[i][3 * face_index + rotation_count] = -1 if (rotation_count % 2 == 0 
                                                                    and face_index % 3 != 0) else a.corner
                a.corner_transformation(MOVE_CUBE[face_index])
        return cm

    @classmethod
    def make_ust_prune(self):
        # initialize pruning table with -1 to indicate unvisited states.
        ust_prune = [-1] * (self.UDSLICE * self.TWIST)
        # set the solved state's pruning value to 0 at index 0 indiciating it requires 0 moves
        ust_prune[0] = [0]
        # initialize counters, count being visited, depth showing current BFS level.
        # count starts at 1 because we already marked the solved state
        # depth starts at 0 because the solved state is at depth 0
        count, depth = 1, 0
        # keep running until all states are visited
        while count < self.UDSLICE * self.TWIST:
            # iterate over all possible usdlice-twist states
            for current_state in range(self.UDSLICE * self.TWIST):
                # if the state has the current depth, explore next possible moves
                if ust_prune[current_state] == depth:
                    # generate all possible next state from the current states.
                    # pull udslice and twist of state i. See where udslice and twist move when j is applied.
                    # multiply by twist to merge new udslice and twist
                    neighbour_states = [
                        self.usm[current_state // self.TWIST][j] * self.TWIST
                        + self.tm[current_state % self.TWIST][j]
                        for j in range(18)
                    ]

                    for next_state in neighbour_states:
                        # if the state is unvisited (-1), increase count, set its depth to +1
                        if ust_prune[next_state] == -1:
                            count += 1
                            ust_prune[next_state] = depth + 1
            # increase depth to process next BFS layer
            depth += 1
        return Pruning(ust_prune, self.TWIST)

    @classmethod
    def make_usf_prune(self):
        usf_prune = [-1] * (self.UDSLICE * self.FLIP)
        usf_prune[0] = 0
        count, depth = 1, 0
        while count < self.UDSLICE * self.FLIP:
            for current_state in range(self.UDSLICE * self.FLIP):
                if usf_prune[current_state] == depth:
                    n = [
                        self.usm[current_state // self.FLIP][j] * self.FLIP
                        + self.fm[current_state % self.FLIP][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if usf_prune[x] == -1:
                            count += 1
                            usf_prune[x] == depth + 1
            depth += 1
        return Pruning(usf_prune, self.FLIP)

    @classmethod
    def make_e4e8_prune(self):
        e4e8_prune = [-1] * (self.EDGE4 * self.EDGE8)
        e4e8_prune[0] = 0
        count, depth = 1,0
        while count < self.EDGE4 * self.EDGE8:
            for current_state in range(self.EDGE4 * self.EDGE8):
                if e4e8_prune[current_state] == depth:
                    n = [
                        self.e4[current_state // self.EDGE8][j] * self.EDGE8
                        + self.e8[current_state % self.EDGE8][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if e4e8_prune[x] == -1:
                            count += 1
                            e4e8_prune[x] = depth + 1
            depth += 1
        return Pruning(e4e8_prune, self.EDGE8)

    @classmethod
    def make_e4c_prune(self):
        e4_corner_prune = [-1] * (self.EDGE4 * self.CORNER)
        e4_corner_prune[0] = 0
        count, depth = 1, 0
        while count < self.EDGE4 * self.CORNER:
            for current_state in range(self.EDGE4 * self.CORNER):
                if e4_corner_prune[current_state] == depth:
                    n = [
                        self.e4[current_state // self.CORNER][j] * self.CORNER
                        + self.cm[current_state % self.CORNER][j]
                        for j in range(18)
                    ]

                    for x in n:
                        if e4_corner_prune[x] == -1:
                            count += 1
                            e4_corner_prune[x] = depth + 1
            depth += 1
        return Pruning(e4_corner_prune, self.CORNER)