import json
import os

from .cubes.cubie import Cubie, MOVE_CUBE

class Pruning:
    # initialize pruning table
    def __init__(self, table, columns):
        self.table = table
        self.columns = columns
    # Access elements in pruning with 2D-style indexing
    def __getitem__(self, x):
        return self.table[x[0] * self.columns + x[1]]
    
class Tables: 
    # Class to hold moving and pruning tables in memory.
    # Move tables are used for updating coordinates of a cube when a move is appled
    # Pruning tables are used to obtain the lwoer bounds for the number of moves required to reach a solution when
    # given a pair of coordinates
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
    def load_tables(cls):
        if os.path.isfile('tables.json'):
            with open('tables.json', 'r') as f:
                tables = json.load(f)
            cls.twist_move = tables['twist_move']
            cls.flip_move = tables['flip_move']
            cls.udslice_move = tables['udslice_move']
            cls.edge4_move = tables['edge4_move']
            cls.edge8_move = tables['edge8_move']
            cls.corner_move = tables['corner_move']
            cls.udslice_twist_prune = Pruning(tables['udslice_twist_prune'], cls.TWIST)
            cls.udslice_flip_prune = Pruning(tables['udslice_flip_prune'], cls.FLIP)
            cls.edge4_edge8_prune = Pruning(tables['edge4_edge8_prune'], cls.EDGE8)
            cls.edge8_corner_prune = Pruning(tables['edge4_corner_prune'], cls.CORNER)
        else:
            # Move tables
            cls.twist_move = cls.make_twist_table()
            cls.flip_move = cls.make_flip_table()
            cls.udslice_move = cls.make_udslice_table()

            cls.edge4_move = cls.make_edge4_table()
            cls.edge8_move = cls.make_edge8_table()
            cls.corner_move = cls.make_corner_table()

            # Pruning tables
            cls.udslice_twist_prune = cls.make_udslice_twist_prune()
            cls.udslice_flip_prune = cls.make_udslice_flip_prune()

            cls.edge4_edge8_prune = cls.make_edge4_edge8_prune()
            cls.edge4_corner_prune = cls.make_edge4_corner_prune()

            tables = {
                "twist_move": cls.twist_move,
                "flip_move": cls.flip_move,
                "udslice_move": cls.udslice_move,
                "edge4_move": cls.edge4_move,
                "edge8_move": cls.edge8_move,
                "corner_move": cls.corner_move,
                "udslice_twist_prune": cls.udslice_twist_prune.table,
                "udslice_flip_prune": cls.udslice_flip_prune.table,
                "edge4_edge8_prune": cls.edge4_edge8_prune.table,
                "edge4_corner_prune": cls.edge4_corner_prune.table,
            }
            with open('tables.json', 'w') as f:
                json.dump(tables, f)
        cls._loaded_tables_ = True

    @classmethod
    def make_twist_table(cls):
        # Create 2D list initialized with zeros. Outer list has self.TWIST rows (one for each twist state). Each row has cls.MOVES columns (one for each move in the move set). Fill table with twist
        # state after each move. 
        # TS|M0|M1|M2 ...
        # ------------
        # self.MOVES represents the total # of moves, self.FLIP represents the total # of possible edge states
        tm = [[0] * cls.MOVES for _ in range(cls.TWIST)]
        a = Cubie()

        # Loop over all possible twist states, and set the cube's current state to i, so we can track how moves affect it. 
        for i in range(cls.TWIST):
            a.twist = i
            # Loop over MOVE_CUBE list, where each move is a predefined face turn. Enumerate gives index of move, move is the actual move used 
            for face_index in range(6):
                # Each face move can be applied up to 3 times (quarter-turns) k = 0 -> apply move once (90), k=1 -> apply move again (180), k=2  -> apply move a 3rd time (270)
                for rotation_count in range(3):
                    a.corner_transformation(MOVE_CUBE[face_index])
                    # Store the resulting twist state in the table
                    tm[i][3 * face_index + rotation_count] = a.twist
                # Reset move after 3 times. 
                a.corner_transformation(MOVE_CUBE[face_index])
        return tm

    @classmethod
    def make_flip_table(cls):
        fm = [[0] * cls.MOVES for _ in range(cls.FLIP)]
        a = Cubie()

        for i in range(cls.FLIP):
            a.flip = i
            # Loop over 6 possible face moves
            for face_index in range(6):
                # Apply the same face move 3 times over, and store each new flip state
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    fm[i][3 * face_index + rotation_count] = a.flip
                # Reset flips after 3 times
                a.edge_transformation(MOVE_CUBE[face_index])
        return fm
    
    @classmethod
    def make_udslice_table(cls):
        usm = [[0] * cls.MOVES for _ in range(cls.UDSLICE)]
        a = Cubie()
        for i in range(cls.UDSLICE):
            a.udslice = i
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    usm[i][3 * face_index + rotation_count] = a.udslice
                a.edge_transformation(MOVE_CUBE[face_index])
        return usm
    
    @classmethod
    def make_edge4_table(cls):
        e4 = [[0] * cls.MOVES for _ in range(cls.EDGE4)]
        a = Cubie()
        # Loop over all possible edges
        for i in range(cls.EDGE4):
            # setting i so that we can track how it changes when moves are applied
            a.edge4 = i
            for face_index in range(6):
                for rotation_count in range(3):
                    if rotation_count % 2 == 0 and face_index % 3 != 0:
                        e4[i][3 * face_index + rotation_count] = -1
                    else:
                        e4[i][3 * face_index + rotation_count] = a.edge4
                a.edge_transformation(MOVE_CUBE[face_index])
        return e4
    
    @classmethod
    def make_edge8_table(cls):
        e8 = [[0] * cls.MOVES for _ in range(cls.EDGE8)]
        a = Cubie()

        for i in range(cls.EDGE8):
            a.edge8 = i 
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    # Determine what value to store in the lookup table.
                    # If the move is applied an even # of times (1st or 3rd move)
                    # AND the face index is not a multiple of 3 (excluding U and F moves),
                    # store -1 to show invalid state transition
                    # otherwise, store the updated e4 state in lookup table
                    if rotation_count % 2 == 0 and face_index % 3 != 0:
                        e8[i][3 * face_index + rotation_count] = -1
                    else:
                        e8[i][3 * face_index + rotation_count] = a.edge8
                # apply move one more time to return cube back to original state
                a.edge_transformation(MOVE_CUBE[face_index])
        return e8

    @classmethod
    def make_corner_table(cls):
        cm = [[0] * cls.MOVES for _ in range(cls.CORNER)]
        a = Cubie()
        for i in range(cls.CORNER):
            a.corner = i
            for face_index in range(6):
                for rotation_count in range(3):
                    a.edge_transformation(MOVE_CUBE[face_index])
                    if rotation_count % 2 == 0 and face_index % 3 != 0:
                        cm[i][3 * face_index + rotation_count] = -1
                    else:
                        cm[i][3 * face_index + rotation_count] = a.corner
                a.corner_transformation(MOVE_CUBE[face_index])
        return cm

    @classmethod
    def make_udslice_twist_prune(cls):
        # initialize pruning table with -1 to indicate unvisited states.
        udslice_twist_prune = [-1] * (cls.UDSLICE * cls.TWIST)
        # set the solved state's pruning value to 0 at index 0 indiciating it requires 0 moves
        udslice_twist_prune[0] = 0
        # initialize counters, count being visited, depth showing current BFS level.
        # count starts at 1 because we already marked the solved state
        # depth starts at 0 because the solved state is at depth 0
        count, depth = 1, 0
        # keep running until all states are visited
        while count < cls.UDSLICE * cls.TWIST:
            # iterate over all possible usdlice-twist states
            for current_state in range(cls.UDSLICE * cls.TWIST):
                # if the state has the current depth, explore next possible moves
                if udslice_twist_prune[current_state] == depth:
                    # generate all possible next state from the current states.
                    # pull udslice and twist of state i. See where udslice and twist move when j is applied.
                    # multiply by twist to merge new udslice and twist
                    neighbour_states = [
                        cls.udslice_move[current_state // cls.TWIST][j] * cls.TWIST
                        + cls.twist_move[current_state % cls.TWIST][j]
                        for j in range(18)
                    ]

                    for next_state in neighbour_states:
                        # if the state is unvisited (-1), increase count, set its depth to +1
                        if udslice_twist_prune[next_state] == -1:
                            count += 1
                            udslice_twist_prune[next_state] = depth + 1
            # increase depth to process next BFS layer
            depth += 1
        return Pruning(udslice_twist_prune, cls.TWIST)

    @classmethod
    def make_udslice_flip_prune(cls):
        udslice_flip_prune = [-1] * (cls.UDSLICE * cls.FLIP)
        udslice_flip_prune[0] = 0
        count, depth = 1, 0
        while count < cls.UDSLICE * cls.FLIP:
            for current_state in range(cls.UDSLICE * cls.FLIP):
                if udslice_flip_prune[current_state] == depth:
                    n = [
                        cls.udslice_move[current_state // cls.FLIP][j] * cls.FLIP
                        + cls.flip_move[current_state % cls.FLIP][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if udslice_flip_prune[x] == -1:
                            count += 1
                            udslice_flip_prune[x] = depth + 1
            depth += 1
        return Pruning(udslice_flip_prune, cls.FLIP)

    @classmethod
    def make_edge4_edge8_prune(cls):
        edge4_edge8_prune = [-1] * (cls.EDGE4 * cls.EDGE8)
        edge4_edge8_prune[0] = 0
        count, depth = 1, 0
        while count < cls.EDGE4 * cls.EDGE8:
            for current_state in range(cls.EDGE4 * cls.EDGE8):
                if edge4_edge8_prune[current_state] == depth:
                    n = [
                        cls.edge4_move[current_state // cls.EDGE8][j] * cls.EDGE8
                        + cls.edge8_move[current_state % cls.EDGE8][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if edge4_edge8_prune[x] == -1:
                            count += 1
                            edge4_edge8_prune[x] = depth + 1
            depth += 1
        return Pruning(edge4_edge8_prune, cls.EDGE8)

    @classmethod
    def make_edge4_corner_prune(cls):
        edge4_corner_prune = [-1] * (cls.EDGE4 * cls.CORNER)
        edge4_corner_prune[0] = 0
        count, depth = 1, 0
        while count < cls.EDGE4 * cls.CORNER:
            for current_state in range(cls.EDGE4 * cls.CORNER):
                if edge4_corner_prune[current_state] == depth:
                    n = [
                        cls.edge4_move[current_state // cls.CORNER][j] * cls.CORNER
                        + cls.corner_move[current_state % cls.CORNER][j]
                        for j in range(18)
                    ]

                    for x in n:
                        if edge4_corner_prune[x] == -1:
                            count += 1
                            edge4_corner_prune[x] = depth + 1
            depth += 1
        return Pruning(edge4_corner_prune, cls.CORNER)