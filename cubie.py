from functools import reduce
from pieces import Corner, Edge
from . import facecube

def choose(n, k):
    if 0 <= k <= n:
        num = 1
        den = 1
        for i in range(1, min(k, n - k) + 1):
            num *= n
            den *= i
            n -= 1
        return num // den
    else:
        return 0


# Table that shows position of cubies after a U rotation and so forth
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
    
    # Convert cubie to faceCube ... useful for vis generation as well
    # Self being scrambled cube state
    def to_facecube(self):
        face = facecube.FaceCube()
        # Return location and orientation of each corner
        for i in range(8):
            location = self.corner_pos[i]
            ori = self.corner_ori[i]
            for o in range(3):
                face.f[facecube.corner_facelet[i][(o+ori) % 3]] = facecube.corner_color[location][o]
        # Return location and orientation of each corner 
        for x in range(12):
            e = self.edge_pos[x]
            ori = self.edge_ori[x]
            for o in range(2):
                facelet = facecube.edge_facelet[x][(o+ori) % 2]
                face.f[facelet] = facecube.edge_color[e][o]
        
        return face
    
    # Check how many corners have been swapped. When compared to edge check, determine if solvable or not. 
    def corner_check(self):
        swaps = 0
        for i in range(7,0,-1):
            for j in range(i-1, -1, -1):
                if self.cp[j] > self.cp[i]:
                    s +=1
        return s % 2
    
    # Check how many edges have been swapped. When compared to corner check, determine if solvable or not.  
    def edge_check(self):
        swaps = 0
        for i in range (11, 0, -1):
            for j in range (i - 1, -1, -1):
                if self.ep[j] > self.ej[i]:
                    s+=1
        return s % 2
    
    # Create ternary value to represent corner orientations. 
    def get_twist(self):
        twist_value = 0
        for i in range(7):
            twist_value = 3 * twist_value + self.co[i]
        return twist_value
    
    # Setter for twist, reverses ternary value that get_twist returns in order to set twist values for the scrambled cube
    def set_twist(self, twist):
        if not 0 <= twist < 3 ** 7:
            raise ValueError(f'{twist} is out of range for twist, has to between 0 and 2186.')
        self.co[:7] = [twist // (3 ** i) % 3 for i in reversed(range(7))]
        total = sum(self.co[:7])
        self.co[7] = (-total) % 3

    # Create binary value to represent edge orientations.
    def get_flip(self):
        flip_value = 0
        for i in range(11):
            flip_value = 2 * flip_value + self.edge_ori[i]
        return flip_value

    # Setter for flip, reverses binary value that get_flip return in order to set flip values for the scrambled cube
    def set_flip(self, flip):
        if not 0 <= 2 ** 11:
            raise ValueError(f'{flip} is out of range for flip, must be between 0 and 2047.')
        self.edge_ori[:11] = [flip // (2 ** i) % 2 for i in reversed(range(11))]
        total = sum(self.edge_ori[:11])
        self.edge_ori[11] = (-total) % 2

    # Determine if FR, FL, BL, and BR are in the middle layer. 
    # If all are, return 0, else return non-zero number, higher values means more out of placed vals
    def get_udslice(self):
        udslice, seen = 0, 0
        for j, edge in enumerate(self.edge_pos):
            if 8 <= edge < 12:
                seen += 1
            elif seen > 0:
                # Check how many ways the previously seen middle layer edges can be placed incorrectly.
                # j: total positions checked so far in self.edge_pos 0...11
                udslice += choose(j, seen - 1)
        return udslice

    # Determine which positions the middle layer edgs should go based on udslice val.
    def set_udslice(self, udslice):
        udslice_edge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        other_edge = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB]
        # Set edges to DB, easier to organize
        self.edge_pos = [Edge.DB] * 12
        # Start placing middle layer edges based on udslice 
        seen = 3
        for j in reversed(range(12)):
            comb = choose(j, seen)
            # Udslice represents value of how far edges are from correct spots, and gets reduced as we place edges.
            # if True, place edge at ep[j], if False, we can skip placing an edge at this spot. 
            # Udslice represents how many ways per last func, comb is how much each one costs. 
            if udslice < comb:
                self.edge_pos[j] = udslice_edge[seen]
                seen -= 1
            else:
                udslice -= comb
        # Fill remaining edges 
        remaining_edges = iter(other_edge)
        self.edge_pos = [next(remaining_edges) if edge == Edge.DB else edge for edge in self.edge_pos]

    # Check if edges are in correct order, assuming they are in correct positions. Returns coordinate within 0 ... 23 which represents which 
    # order it is in. There are 24 possible ways to order 4 distinct items.
    def get_edge4(self):
        edge4 = self.ep[8:]
        
        ret = sum(sum(1 for i in range(j) if edge4[i] > edge4[j]) * j
                  for j in range (3, 0, -1))
        return ret
    # Updates edge_pos with the correct order of the 4 middle layer edges. 
    def set_edge4(self, edge4):
        if not 0 <= edge4 < 24:
            raise ValueError(f"{edge4} is out of range for edge4, must be between 0 and 23")
        slice_edge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        pos = []

        for i in reversed(range(4)):
            # Return position of the next edge, i + 1 to ensure remaining spots is accounted for correctly
            # e.g determining who goes first in a race of 4, first has 4 spots to choose 
            coeff = edge4 % (i + 1)
            # Reduce edge4 for next coeff
            edge4 //= i + 1
            # Remove
            pos.insert(0, slice_edge.pop(coeff))
        # Update last four elements to pos
        self.edge_pos[8:] = pos

    def get_edge8(self):
        



        


        





