from .cubie import Cubie
from ..tables import Tables

class Coord:
    def __init__(self, twist=0, flip=0, udslice=0, edge4=0, edge8=0, corner=0):
        # initialize coordinate representation of a cube. 
        self.tables = Tables()
        self.twist = twist
        self.flip = flip
        self.udslice = udslice
        self.edge4 = edge4
        self.edge8 = edge8
        self.corner = corner

    @classmethod
    def from_cubie(cls, cube):
        # Create coord version of cubie
        if not isinstance(cube, Cubie):
            raise TypeError('Expected argument of type Cubie')
        return cls (
            cube.twist,
            cube.flip,
            cube.udslice,
            cube.edge4,
            cube.edge8,
            cube.corner
        )

    def move(self, mv):
        # Update coordinates of the CoordCube after applying a move on the cube.
        # Pulls information from pre made move table. 
        # 0 - 5 represents U, R, F, D, L, B ... i
        # 0 - 2 represents 90, 180, -90 deg ... j
        # moves are represented by mv = 3 * i + j ... 0 - 17
        self.twist = self.tables.twist_move[self.twist][mv]
        self.flip = self.tables.flip_move[self.flip][mv]
        self.udslice = self.tables.udslice_move[self.udslice][mv]
        self.edge4 = self.tables.edge4_move[self.edge4][mv]
        self.edge8 = self.tables.edge8_move[self.edge8][mv]
        self.corner = self.tables.corner_move[self.corner][mv]

        