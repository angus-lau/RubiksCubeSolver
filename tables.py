import json
import os

from cubie import Cubie, MOVE_CUBE

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
        if not self._loaded_tables():
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
            self.e4c = Pruning(tables['e4c'], self.CORNER)
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

            self.e4e8_prune = self.make_edge4_edge8_prune()
            self.e4_corner_prune = self.make_edge4_corner_prune()

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
                'e4c': self.e4_corner_prune.table,
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
            for j, move in enumerate(MOVE_CUBE):
                # Each face move can be applied up to 3 times (quarter-turns) k = 0 -> apply move once (90), k=1 -> apply move again (180), k=2  -> apply move a 3rd time (270)
                for k in range(3):
                    a.corner_transformation(move)
                    # Store the resulting twist state in the table
                    tm[i][3 * j + k] = a.twist
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
            for j in range(6):
                # Apply the same face move 3 times over, and store each new flip state
                for k in range(3):
                    a.edge_transformation(MOVE_CUBE[j])
                    ft[i][3 * j + k] = a.flip
                # Reset flips after 3 times
                a.edge_transformation(MOVE_CUBE[j])
        return ft
    
    @classmethod
    def make_udslice_table(self):
        usm = [[0] * self.MOVES for _ in range(self.UDSLICE)]
        a = Cubie()
        for i in range(self.UDSLICE):
            a.udslice = i
            for j in range(6):
                for k in range(3):
                    a.edge_transformation(MOVE_CUBE[j])
                    usm[i][3 * j + k] = a.udslice
                a.edge_transformation(MOVE_CUBE[j])
        return usm
    
    @classmethod
    def make_edge4_table(self):
        e4 = [[0] * self.MOVES for _ in range(self.EDGE4)]
        a = Cubie()
        # Loop over all possible edges
        for i in range(self.EDGE4):
            # setting i so that we can track how it changes when moves are applied
            a.edge4 = i
            for j in range(6):
                for k in range(3):
                    a.edge_transformation(MOVE_CUBE[j])
                    e4[i][3 * j + k] = -1 if (k % 2 == 0 and j % 3 != 0) else a.edge4
                a.edge_transformation(MOVE_CUBE[j])
        return e4
    
    @classmethod
    def make_edge8_table(self):
        e8 = [[0] * self.MOVES for _ in range(self.EDGE8)]
        a = Cubie()

        for i in range(self.EDGE8):
            a.edge8 = i 
            for j in range(6):
                for k in range(3):
                    a.edge_transformation(MOVE_CUBE[j])
                    e8[i][3 * j + k] = -1 if (k % 2 == 0 and j % 3 != 0) else a.edge8
                a.edge_transformation(MOVE_CUBE[j])
        return e8

    @classmethod
    def make_corner_table(self):
        cm = [[0] * self.MOVES for _ in range(self.CORNER)]
        a = Cubie()
        for i in range(self.CORNER):
            a.corner = i
            for j in range(6):
                for k in range(3):
                    a.corner_transformation(MOVE_CUBE[j])
                    cm[i][3 * j + k] = -1 if (k % 2 == 0 and j % 3 != 0) else a.corner
                a.corner_transformation(MOVE_CUBE[j])
        return cm

    @classmethod
    def make_ust_prune(self):
        ust_prune = [-1] * (self.UDSLICE * self.TWIST)
        ust_prune[0] = [0]
        count, depth = 1, 0
        while count < self.UDSLICE * self.TWIST:
            for i in range(self.UDSLICE * self.TWIST):
                if ust_prune[i] == depth:
                    n = [
                        self.usm[i // self.TWIST][j] * self.TWIST
                        + self.tm[i % self.TWIST][j]
                        for j in range(18)
                    ]

                    for y in n:
                        if ust_prune[y] == -1:
                            count += 1
                            ust_prune[y] = depth + 1
            depth += 1
        return Pruning(ust_prune, self.TWIST)

    @classmethod
    def make_usf_prune(self):
        usf_prune = [-1] * (self.UDSLICE * self.FLIP)
        usf_prune[0] = 0
        count, depth = 1, 0
        while count < self.UDSLICE * self.FLIP:
            for i in range(self.UDSLICE * self.FLIP):
                if usf_prune[i] == depth:
                    n = [
                        self.usm[i // self.FLIP][j] * self.FLIP
                        + self.fm[i % self.FLIP][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if usf_prune[x] == -1:
                            count += 1
                            usf_prune[x] == depth + 1
            depth += 1
        return Pruning(usf_prune, self.FLIP)

    @classmethod
    def make_edge4_edge8_prune(self):
        e4e8_prune = [-1] * (self.EDGE4 * self.EDGE8)
        e4e8_prune[0] = 0
        count, depth = 1,0
        while count < self.EDGE4 * self.EDGE8:
            for i in range(self.EDGE4 * self.EDGE8):
                if e4e8_prune[i] == depth:
                    n = [
                        self.e4[i // self.EDGE8][j] * self.EDGE8
                        + self.e8[i % self.EDGE8][j]
                        for j in range(18)
                    ]
                    for x in n:
                        if e4e8_prune[x] == -1:
                            count += 1
                            e4e8_prune[x] = depth + 1
            depth += 1
        return Pruning(e4e8_prune, self.EDGE8)

    @classmethod
    def make_edge4_corner_prune(self):
        e4_corner_prune = [-1] * (self.EDGE4 * self.CORNER)
        e4_corner_prune[0] = 0
        count, depth = 1, 0
        while count < self.EDGE4 * self.CORNER:
            for i in range(self.EDGE4 * self.CORNER):
                if e4_corner_prune[i] == depth:
                    n = [
                        self.e4[i // self.CORNER][j] * self.CORNER
                        + self.cm[i % self.CORNER][j]
                        for j in range(18)
                    ]

                    for x in n:
                        if e4_corner_prune[x] == -1:
                            count += 1
                            e4_corner_prune[x] = depth + 1
            depth += 1
        return Pruning(e4_corner_prune, self.CORNER)