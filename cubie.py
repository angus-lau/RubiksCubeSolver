from functools import reduce
from pieces import Corner, Edge
from . import facecube


# Table that shows position of cubies after an U rotation and so forth
_cpU = (
    Corner.UBR,
    Corner.URF,
    Corner.UFL,
    Corner.ULB,
    Corner.DFR,
    Corner.DLF,
    Corner.DBL,
    Corner.DRB,
)
_coU = (0, 0, 0, 0, 0, 0, 0, 0)
_epU = (
    Edge.UB,
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.DR,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.FR,
    Edge.FL,
    Edge.BL,
    Edge.BR,
)
_eoU = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpR = (
    Corner.DFR,
    Corner.UFL,
    Corner.ULB,
    Corner.URF,
    Corner.DRB,
    Corner.DLF,
    Corner.DBL,
    Corner.UBR,
)
_coR = (2, 0, 0, 1, 1, 0, 0, 2)
_epR = (
    Edge.FR,
    Edge.UF,
    Edge.UL,
    Edge.UB,
    Edge.BR,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.DR,
    Edge.FL,
    Edge.BL,
    Edge.UR,
)
_eoR = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpF = (
    Corner.UFL,
    Corner.DLF,
    Corner.ULB,
    Corner.UBR,
    Corner.URF,
    Corner.DFR,
    Corner.DBL,
    Corner.DRB,
)
_coF = (1, 2, 0, 0, 2, 1, 0, 0)
_epF = (
    Edge.UR,
    Edge.FL,
    Edge.UL,
    Edge.UB,
    Edge.DR,
    Edge.FR,
    Edge.DL,
    Edge.DB,
    Edge.UF,
    Edge.DF,
    Edge.BL,
    Edge.BR,
)
_eoF = (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0)

_cpD = (
    Corner.URF,
    Corner.UFL,
    Corner.ULB,
    Corner.UBR,
    Corner.DLF,
    Corner.DBL,
    Corner.DRB,
    Corner.DFR,
)
_coD = (0, 0, 0, 0, 0, 0, 0, 0)
_epD = (
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.UB,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.DR,
    Edge.FR,
    Edge.FL,
    Edge.BL,
    Edge.BR,
)
_eoD = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpL = (
    Corner.URF,
    Corner.ULB,
    Corner.DBL,
    Corner.UBR,
    Corner.DFR,
    Corner.UFL,
    Corner.DLF,
    Corner.DRB,
)
_coL = (0, 1, 2, 0, 0, 2, 1, 0)
_epL = (
    Edge.UR,
    Edge.UF,
    Edge.BL,
    Edge.UB,
    Edge.DR,
    Edge.DF,
    Edge.FL,
    Edge.DB,
    Edge.FR,
    Edge.UL,
    Edge.DL,
    Edge.BR,
)
_eoL = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpB = (
    Corner.URF,
    Corner.UFL,
    Corner.UBR,
    Corner.DRB,
    Corner.DFR,
    Corner.DLF,
    Corner.ULB,
    Corner.DBL,
)
_coB = (0, 0, 1, 2, 0, 0, 2, 1)
_epB = (
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.BR,
    Edge.DR,
    Edge.DF,
    Edge.DL,
    Edge.BL,
    Edge.FR,
    Edge.FL,
    Edge.UB,
    Edge.DB,
)
_eoB = (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)

class Cubie:
    def __init__(self, corner_pos = None, corner_ori = None, edge_pos = None, edge_ori = None):
        # If inputs are not empty, update cube to have given values
        if corner_pos and corner_ori and edge_pos and edge_ori:
            self.corner_pos = corner_pos[:]
            self.corner_ori = corner_ori[:]
            self.edge_pos = edge_pos[:]
            self.edge_ori = edge_ori[:]
        
        else:
            # No inputs provided, initialize clean cube with correct edges and corners
            self.corner_pos = [
                Corner.URF,
                Corner.UFL,
                Corner.ULB,
                Corner.UBR,
                Corner.DBL,
                Corner.DFR,
                Corner.DLF,
                Corner.DRB
            ]
            self.corner_ori = [0] * 8

            self.edge_pos = [
                Edge.UR,
                Edge.UF,
                Edge.UL,
                Edge.UB,
                Edge.DR,
                Edge.DF,
                Edge.DL,
                Edge.DB,
                Edge.FR,
                Edge.FL,
                Edge.BL,
                Edge.BR
            ]

            self.edge_ori = [0] * 12

    # Apply move b and update corner orientation and corner position
    # b returns its effect, then we see how that impacts orig corner_pos list 
    def corner_transformation(self, b):
        c_pos = []
        c_ori = []
        for i in range(8):
            c_pos.append(self.corner_pos[b.corner_pos[i]])
            c_ori.append((self.corner_ori[b.corner_pos][i] + b.corner_ori[i]) % 3)
        
        self.corner_ori = c_ori[:]
        self.corner_pos = c_pos[:]
    
    # Similar to corner_transformation, applies b and updates edge position and orientation. 
    def edge_transformation(self, b):
        e_pos = []
        e_ori = []
        for i in range(12):
            e_pos.append(self.edge_pos[b.edge_pos[i]])
            e_ori.append((self.edge_ori[b.edge_pos[i]] + b.edge_ori[i]) % 2)
        
        self.edge_ori = e_ori[:]
        self.edge_pos = e_pos[:]

    # Group transformation of corner and edges of cube
    def transform(self, b):
        self.corner_transformation(b)
        self.edge_transformation(b)

    def move(self, i):
        self.transform(MOVE_CUBE[i])

    # return inverse of cube 
    def inverse_cube(self):
        cube = Cubie()
        for i in range(8):
            # self.corner_pos returns where the current corner is sitting at e.g returns 0, cube.corner_pos will 
            cube.corner_pos[self.corner_pos[i]] = i
            ori = cube.corner_ori[self.corner_ori[i]]
            cube.corner_ori[i] = (-ori) % 3
        for i in range(12):
            cube.edge_pos[self.edge_pos[i]] = i
            cube.edge_ori[i] = self.edge_ori[cube.edge_ori[i]]
        
        return cube





