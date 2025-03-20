from functools import reduce
from ..pieces import Corner, Edge
from . import face

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
    def __init__(self, cp = None, co = None, ep = None, eo = None):
        # If inputs are not empty, update cube to have given values
        if cp and co and ep and eo:
            self.cp = cp[:]
            self.co = co[:]
            self.ep = ep[:]
            self.eo = eo[:]
        else:
            # No inputs provided, initialize clean cube with correct edges and corners
            self.cp = [
                Corner.URF,
                Corner.UFL,
                Corner.ULB,
                Corner.UBR,
                Corner.DFR,
                Corner.DLF,
                Corner.DBL,
                Corner.DRB
            ]
            self.co = [0] * 8

            self.ep = [
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

            self.eo = [0] * 12

    # Apply move b and update corner orientation and corner position
    # b returns its effect, then we see how that impacts orig corner_pos list 
    def corner_transformation(self, b):
        corner_pos = [self.cp[b.cp[i]] for i in range(8)]
        corner_ori = [(self.co[b.cp[i]] + b.co[i]) % 3 for i in range(8)]
        
        self.co = corner_ori[:]
        self.cp = corner_pos[:]
    
    # Similar to corner_transformation, applies b and updates edge position and orientation. 
    def edge_transformation(self, b):
        edge_pos = [self.ep[b.ep[i]] for i in range(12)]
        edge_ori = [(self.eo[b.ep[i]] + b.eo[i]) % 2 for i in range(12)]
        
        self.eo = edge_ori[:]
        self.ep = edge_pos[:]

    # Group transformation of corner and edges of cube
    def transform(self, b):
        self.corner_transformation(b)
        self.edge_transformation(b)

    def move(self, i):
        self.transform(MOVE_CUBE[i])

    # return inverse of cube 
    def inverse_cube(self):
        cube = Cubie()
        for x in range(12):
            cube.ep[self.ep[x]] = x
            cube.eo[x] = self.eo[cube.eo[x]]
        for y in range(8):
            # self.corner_pos returns where the current corner is sitting at e.g returns 0, cube.corner_pos will 
            cube.cp[self.cp[y]] = y
            ori = cube.co[self.co[y]]
            cube.co[y] = (-ori) % 3
        return cube
    
    # Convert cubie to faceCube ... useful for vis generation as well
    def to_facecube(self):
        ret = face.Face()
        # Return location and orientation of each corner
        for i in range(8):
            location = self.cp[i]
            ori = self.co[i]
            for o in range(3):
                ret.f[face.corner_facelet[i][(o+ori) % 3]] = face.corner_color[location][o]
        # Return location and orientation of each corner 
        for x in range(12):
            e = self.ep[x]
            ori = self.eo[x]
            for o in range(2):
                facelet = face.edge_facelet[x][(o+ori) % 2]
                ret.f[facelet] = face.edge_color[e][o]
        
        return ret
    
    @property
    # Check how many corners have been swapped. When compared to edge check, determine if solvable or not. 
    def corner_check(self):
        swaps = 0
        for i in range(7, 0, -1):
            for j in range(i - 1, -1, -1):
                if self.cp[j] > self.cp[i]:
                    swaps +=1
        return swaps % 2
    
    @property
    # Check how many edges have been swapped. When compared to corner check, determine if solvable or not.  
    def edge_check(self):
        swaps = 0
        for i in range (11, 0, -1):
            for j in range (i - 1, -1, -1):
                if self.ep[j] > self.ep[i]:
                    swaps += 1
        return swaps % 2
    
    @property
    # Create ternary value to represent corner orientations. 
    def twist(self):
        return reduce(lambda x, y: 3 * x + y, self.co[:7])
    
    @twist.setter
    # Setter for twist, reverses ternary value that get_twist returns in order to set twist values for the scrambled cube
    def twist(self, twist):
        if not 0 <= twist < 3 ** 7:
            raise ValueError(f'{twist} is out of range for twist, has to between 0 and 2186.')
        
        total = 0 
        for i in range(7):
            x = twist % 3
            self.co[6 - i] = x
            total += x
            twist //= 3
        self.co[7] = (-total) % 3

    @property
    # Create binary value to represent edge orientations.
    def flip(self):
        return reduce(lambda x, y: 2 * x + y, self.eo[:11])

    @flip.setter
    # Setter for flip, reverses binary value that get_flip return in order to set flip values for the scrambled cube
    def flip(self, flip):
        if not 0 <= 2 ** 11:
            raise ValueError(f'{flip} is out of range for flip, must be between 0 and 2047.')
        total = 0
        for i in range(11):
            x = flip % 2
            self.eo[10 - i] = x
            total += x
            flip //= 2
        self.eo[11] = (-total) % 2

    @property
    # Determine if FR, FL, BL, and BR are in the middle layer. 
    # If all are, return 0, else return non-zero number, higher values means more out of placed vals
    def udslice(self):
        udslice, seen = 0, 0
        for j in range(12):
                if 8 <= self.ep[j] < 12:
                    seen += 1
                elif seen >= 1:
                # Check how many ways the previously seen middle layer edges can be placed incorrectly.
                # j: total positions checked so far in self.edge_pos 0...11
                    udslice += choose(j, seen - 1)
        return udslice
    
    @udslice.setter
    # Determine which positions the middle layer edgs should go based on udslice val.
    def udslice(self, udslice):
        if not 0 <= udslice < choose(12, 4):
            raise ValueError(f'{udslice} is out of range for udslice, must take in values between 0 and 494.')
        udslice_edge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        other_edge = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB]
        # Set edges to DB, easier to organize
        self.ep = [Edge.DB] * 12
        # Start placing middle layer edges based on udslice 
        seen = 3
        for j in range(11, -1, -1):
            if udslice - choose(j, seen) < 0:
            # Udslice represents value of how far edges are from correct spots, and gets reduced as we place edges.
            # if True, place edge at ep[j], if False, we can skip placing an edge at this spot. 
            # Udslice represents how many ways per last func, comb is how much each one costs. 
                self.ep[j] = udslice_edge[seen]
                seen -= 1
            else:
                udslice -= choose(j, seen)
        # Fill remaining edges
        x = 0
        for j in range(12):
            if self.ep[j] == Edge.DB:
                self.ep[j] = other_edge[x]
                x += 1 

    @property
    # Check if edges are in correct order, assuming they are in correct positions. Returns coordinate within 0 ... 23 which represents which 
    # order it is in. There are 24 possible ways to order 4 distinct items.
    def edge4(self):
        edge4 = self.ep[8:]
        ret = 0
        for j in range(3, 0, -1):
            s = 0
            for i in range(j):
                if edge4[i] > edge4[j]:
                    s += 1
            ret = j * (ret + s)
        return ret
    
    @edge4.setter
    # Updates edge_pos with the correct order of the 4 middle layer edges. 
    def edge4(self, edge4):
        if not 0 <= edge4 < 24:
            raise ValueError(f"{edge4} is out of range for edge4, must be between 0 and 23")
        sliceedge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        coeffs = [0] * 3
        for i in range(1, 4):
            # Return position of the next edge, i + 1 to ensure remaining spots is accounted for correctly
            # e.g determining who goes first in a race of 4, first has 4 spots to choose 
            coeffs[i-1] = edge4 % (i + 1)
            # Reduce edge4 for next coeff
            edge4 //= i + 1
            # Remove
        perm = [0] * 4
        for i in range(2, -1, -1):
            perm[i + 1] = sliceedge.pop(i + 1 - coeffs[i])
        # Update last four elements to pos
        perm[0] = sliceedge[0]
        self.ep[8:] = perm[:]

    @property
    # Return value between 0 and 8!-1 that represents the total # of ways to array the first 8 edges of the cube.
    # 8 edges being: UR, UF, UL, UB, DR, DF, DL, DB
    def edge8(self):
        # Return val depending on if edges are out of order based on if pos[i] > pos[j]. If so, increase count by 1 and multiply by j(weight)
        # to contribute to edge8
        e8 = 0
        for j in range(7, 0, -1):
            s = 0
            for i in range(j):
                if self.ep[i] > self.ep[j]:
                    s += 1
            e8 = j * (e8 + s)
        return e8
    
    @edge8.setter
    # Take edge8 val and update current cube. 
    def edge8(self, edge8):
        edges = list(range(8))
        perm = [0] * 8
        coeffs = [0] * 7
        for i in range(1, 8):
            # Update coeffs list with the remainder each time which represent the order of the edges in the current state. 
            coeffs[i - 1] = edge8 % (i + 1)
            # Reduce edge8 to proceed onto next value
            edge8 //= i + 1
        for i in range(6, -1, -1):
            perm[i + 1] = edges.pop(i + 1 - coeffs[i])
        perm[0] = edges[0]
        self.ep[:8] = perm[:]

    @property
    # Return corner val which represents the position/order of the 8 corners.
    # Val ranging from 0 ... 8! - 1
    def corner(self):
        c = 0
        for j in range(7, 0, -1):
            s = 0
            for i in range(j):
                if self.cp[i] > self.cp[j]:
                    s += 1
            c = j * (c + s)
        return c

    @corner.setter
    # Set corner values and update current cube.
    def corner(self, corn):
        corners = list(range(8))
        perm = [0] * 8
        coeffs = [0] * 7
        for i in range(1, 8):
            # Obtain remainder when diving corner to determine which corner to place next 
            coeffs[i - 1] = corn % (i + 1)
            # Remove last digit (value) from corner to prepare for next corner selection
            corn //= i + 1
        for i in range(6, -1, -1):
            perm[i + 1] = corners.pop(i + 1 - coeffs[i])
        perm[0] = corners[0]
        self.cp = perm[:]
    
    @property
    # Get coordinate for edge positions. Ranges from 0 ... 12! - 1.
    def edge(self):
        e = 0
        for j in range (11, 0, -1):
            s = 0
            for i in range(j):
                if self.ep[i] > self.ep[j]:
                    s += 1
            e = j * (e + s)
        return e
    
    @edge.setter
    # Break down val from get_edge and update cube state for edge position 
    def edge(self, edge):
        edges = list(range(12))
        perm = [0] * 12
        coeffs = [0] * 11
        for i in range(1, 12):
            coeffs[i - 1] = (edge % (i + 1))
            edge //= i + 1

        for i in range (10, -1, -1):
            perm[i + 1] = edges.pop(i + 1 - coeffs[i])
        perm[0] = edges[0]
        self.ep = perm[:]
    
    # Is current cube solvable?
    def verify(self):
        total = 0
        # Check if any edge appears more than once. 
        edge_count = [0 for _ in range(12)]
        for e in range(12):
            edge_count[self.ep[e]] += 1
        for i in range(12):
            if edge_count[i] != 1:
                return -2
            
        # Check if # of flipped edges are even or odd, if odd, unsolvable.
        for i in range(12):
            total += self.eo[i]
        if total % 2 != 0:
            return -3
        
        # Check if each corner appears exactly once, if not, unsolvable. 
        corner_count = [0] * 8
        for c in range(8):
            corner_count[self.cp[c]] += 1
        for i in range(8):
            if corner_count[i] != 1:
                return -4
        
        # Check that the total twist of corners are divisible by 3, if not, unsolvable. 
        total = 0
        for i in range(8):
            total += self.co[i]
        if total % 3 != 0:
            return -5
        
        # Check if edge and corner are equal, if not, unsolvable. 
        if self.edge_check != self.corner_check:
            return -6
        return 0

# six possible clockwise 1/4 turn moves is stored in the following array
MOVE_CUBE = [Cubie() for _ in range(6)]

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



        


        





