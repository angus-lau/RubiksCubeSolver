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
    
    @property
    # Create ternary value to represent corner orientations. 
    def twist(self):
        twist_value = 0
        for i in range(7):
            twist_value = 3 * twist_value + self.co[i]
        return twist_value
    
    @twist.setter
    # Setter for twist, reverses ternary value that get_twist returns in order to set twist values for the scrambled cube
    def twist(self, twist):
        if not 0 <= twist < 3 ** 7:
            raise ValueError(f'{twist} is out of range for twist, has to between 0 and 2186.')
        self.co[:7] = [twist // (3 ** i) % 3 for i in reversed(range(7))]
        total = sum(self.co[:7])
        self.co[7] = (-total) % 3

    @property
    # Create binary value to represent edge orientations.
    def flip(self):
        flip_value = 0
        for i in range(11):
            flip_value = 2 * flip_value + self.edge_ori[i]
        return flip_value

    @flip.setter
    # Setter for flip, reverses binary value that get_flip return in order to set flip values for the scrambled cube
    def flip(self, flip):
        if not 0 <= 2 ** 11:
            raise ValueError(f'{flip} is out of range for flip, must be between 0 and 2047.')
        self.edge_ori[:11] = [flip // (2 ** i) % 2 for i in reversed(range(11))]
        total = sum(self.edge_ori[:11])
        self.edge_ori[11] = (-total) % 2

    @property
    # Determine if FR, FL, BL, and BR are in the middle layer. 
    # If all are, return 0, else return non-zero number, higher values means more out of placed vals
    def udslice(self):
        udslice, seen = 0, 0
        for j, edge in enumerate(self.edge_pos):
            if 8 <= edge < 12:
                seen += 1
            elif seen > 0:
                # Check how many ways the previously seen middle layer edges can be placed incorrectly.
                # j: total positions checked so far in self.edge_pos 0...11
                udslice += choose(j, seen - 1)
        return udslice
    
    @udslice.setter
    # Determine which positions the middle layer edgs should go based on udslice val.
    def udslice(self, udslice):
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

    @property
    # Check if edges are in correct order, assuming they are in correct positions. Returns coordinate within 0 ... 23 which represents which 
    # order it is in. There are 24 possible ways to order 4 distinct items.
    def edge4(self):
        edge4 = self.ep[8:]
        ret = sum(sum(1 for i in range(j) if edge4[i] > edge4[j]) * j
                  for j in range (3, 0, -1))
        return ret
    
    @edge4.setter
    # Updates edge_pos with the correct order of the 4 middle layer edges. 
    def edge4(self, edge4):
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

    @property
    # Return value between 0 and 8!-1 that represents the total # of ways to array the first 8 edges of the cube.
    # 8 edges being: UR, UF, UL, UB, DR, DF, DL, DB
    def edge8(self):
        # Return val depending on if edges are out of order based on if pos[i] > pos[j]. If so, increase count by 1 and multiply by j(weight)
        # to contribute to edge8
        e = 0
        for j in range(7, 0, -1):
            s = sum(1 for i in range(j) if self.edge_pos[i] > self.edge_pos[j])
            e = j * (e + s)
        return e
    
    @edge8.setter
    # Take edge8 val and update current cube. 
    def edge8(self, edge8):
        edges = list(range(8))
        pos = [0] * 8
        coeffs = [0] * 7
        for i in range(1,8):
            # Update coeffs list with the remainder each time which represent the order of the edges in the current state. 
            coeffs[i - 1] = edge8 % (i + 1)
            # Reduce edge8 to proceed onto next value
            edge8 //= i + 1
        for i in range(6, -1, -1):
            pos[i+1] = edges.pop(i + 1 - coeffs[i])
        pos[0] = edges[0]
        self.edge_pos[:8] = pos[:]

    @property
    # Return corner val which represents the position/order of the 8 corners.
    # Val ranging from 0 ... 8! - 1
    def corner(self):
        c = 0
        for j in range(7, 0, -1):
            s = sum(1 for i in range(j) if self.corner_pos[i] > self.corner_pos[j])
            c = j * (c + s)
        return c

    @corner.setter
    # Set corner values and update current cube.
    def corner(self, corner):
        corners = list(range(8))
        pos = [0] * 8
        coeffs = [0] * 7
        for i in range(1,8):
            # Obtain remainder when diving corner to determine which corner to place next 
            coeffs[i - 1] = corner % (i + 1)
            # Remove last digit (value) from corner to prepare for next corner selection
            corner //= i + 1
        for i in range(6, -1, -1):
            pos[i + 1] = corners.pop(i + 1 - coeffs[i])
        pos[0] = corners[0]
        self.corner_pos = pos[:]
    
    @property
    # Get coordinate for edge positions. Ranges from 0 ... 12! - 1.
    def edge(self):
        e = 0
        for j in range (11, 0, -1):
            s = sum(1 for i in range(j) if self.edge_pos[i] > self.edge_pos[j])
            e = j * (e + s)
        return e
    
    @edge.sett
    # Break down val from get_edge and update cube state for edge position 
    def edge(self, edge):
        edges = list(range(12))
        pos = [0] * 12
        coeffs = []

        for i in range(1, 12):
            coeffs.append(edge % (i + 1))
            edge /= i + 1

        for i in range (10, -1, -1):
            pos[i + 1] = edges.pop(i + 1 - coeffs[i])
        pos[0] = edges[0]

        self.edge_pos = pos[:]
    
    # Is current cube solvable?
    def verify(self):
        total = 0
        # Check if any edge appears more than once. 
        edge_count = [0 for i in range(12)]
        for e in range(12):
            edge_count[self.edge_pos[e]] += 1
        for i in range(12):
            if edge_count[i] != 1:
                return -2
        # Check if # of flipped edges are even or odd, if odd, unsolvable.
        for i in range(12):
            total += self.edge_ori[i]
        if total % 2 != 0:
            return -3
        
        # Check if each corner appears exactly once, if not, unsolvable. 
        corner_count = [0] * 8
        for c in range(8):
            corner_count[self.corner_pos[c]] += 1
        for i in range(8):
            if corner_count[i] != 1:
                return -4
        
        # Check that the total twist of corners are divisible by 3, if not, unsolvable. 
        total = 0
        for i in range(8):
            total += self.corner_ori[i]
        if total % 3 != 0:
            return -5
        
        # Check if edge and corner are equal, if not, unsolvable. 
        if self.edge_check != self.corner_check:
            return -6
        return 0

# six possible clockwise 1/4 turn moves is stored in the following array
MOVE_CUBE = [Cubie() for i in range(6)]

MOVE_CUBE[0].cp = _cpU
MOVE_CUBE[0].co = _coU
MOVE_CUBE[0].ep = _epU
MOVE_CUBE[0].eo = _eoU

MOVE_CUBE[1].cp = _cpR
MOVE_CUBE[1].co = _coR
MOVE_CUBE[1].ep = _epR
MOVE_CUBE[1].eo = _eoR

MOVE_CUBE[2].cp = _cpF
MOVE_CUBE[2].co = _coF
MOVE_CUBE[2].ep = _epF
MOVE_CUBE[2].eo = _eoF

MOVE_CUBE[3].cp = _cpD
MOVE_CUBE[3].co = _coD
MOVE_CUBE[3].ep = _epD
MOVE_CUBE[3].eo = _eoD

MOVE_CUBE[4].cp = _cpL
MOVE_CUBE[4].co = _coL
MOVE_CUBE[4].ep = _epL
MOVE_CUBE[4].eo = _eoL

MOVE_CUBE[5].cp = _cpB
MOVE_CUBE[5].co = _coB
MOVE_CUBE[5].ep = _epB
MOVE_CUBE[5].eo = _eoB



        


        





