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
        tm = [[0] * self.MOVES for i in range(self.TWIST)]
        