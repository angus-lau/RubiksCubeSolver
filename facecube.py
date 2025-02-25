from pieces import Color, Facelet

# Map corner positions to facelet positions 

corner_facelet = (
    (Facelet.U9, Facelet.R1, Facelet.F3),
    (Facelet.U7, Facelet.F1, Facelet.L3),
    (Facelet.U1, Facelet.L1, Facelet.B3),
    (Facelet.U3, Facelet.B1, Facelet.R3),
    (Facelet.D3, Facelet.F9, Facelet.R7),
    (Facelet.D1, Facelet.L9, Facelet.F7),
    (Facelet.D7, Facelet.B9, Facelet.L7),
    (Facelet.D9, Facelet.R9, Facelet.B7)
)

# Map edge positions to facelet positions
edge_facelet = (
    (Facelet.U6, Facelet.R2),
    (Facelet.U8, Facelet.F2),
    (Facelet.U4, Facelet.L2),
    (Facelet.U2, Facelet.B2),
    (Facelet.D6, Facelet.R8),
    (Facelet.D2, Facelet.F8),
    (Facelet.D4, Facelet.L8),
    (Facelet.D8, Facelet.B8),
    (Facelet.F6, Facelet.R4),
    (Facelet.F4, Facelet.L6),
    (Facelet.B6, Facelet.L4),
    (Facelet.B4, Facelet.R6),
)

# Map corner positions to colours
corner_color = (
    (Color.U, Color.R, Color.F),
    (Color.U, Color.F, Color.L),
    (Color.U, Color.L, Color.B),
    (Color.U, Color.B, Color.R),
    (Color.D, Color.F, Color.R),
    (Color.D, Color.L, Color.F),
    (Color.D, Color.B, Color.L),
    (Color.D, Color.R, Color.B),
)

# Map edge positions to colours
edge_color = (
    (Color.U, Color.R),
    (Color.U, Color.F),
    (Color.U, Color.L),
    (Color.U, Color.B),
    (Color.D, Color.R),
    (Color.D, Color.F),
    (Color.D, Color.L),
    (Color.D, Color.B),
    (Color.F, Color.R),
    (Color.F, Color.L),
    (Color.B, Color.L),
    (Color.B, Color.R),
)

class FaceCube:

    # Initialize the cube, if given str then return enum values appended to list, else return new cube state
    def __init__(self, cube_str):
        if cube_str is not None:
            self.f = [Color[letter] for letter in cube_str]
        else:
            self.f = [Color.U] * 9 + [Color.R] * 9 + [Color.F] * 9 + [Color.D] * 9 + [Color.L] * 9 + [Color.B] * 9

    # Convert cube state to string
    def convert_to_string(self, cube):
        res = ''
        for color in cube:
            res += color.name
        return res
    
    # Convert FaceCube to Cubie e.g break down corner 
    def convert_to_cubie(self):
        cubie = cubiecube.CubieCube()
        # Loop through all 8 corners
        for i in range(8):
            # Loop through all 3 faces of a corner to see if U or D is present at i, x represents if corner piece is twisted or not. 1 = twisted clockwise, 2 = twisted x2
            for x in range(3):
                if self.f[corner_facelet[i][x]] in [Color.U, Color.D]:
                    break
            color1 = self.f[corner_facelet[i](x+1) % 3] # 0 = U, +1, +2 represent other sides, varies by corner
            color2 = self.f[corner_facelet[i](x+2) % 3]
            for j in range (8):
                if color1 == corner_color[j] and color2 == corner_color[j]:
                    cc.cp[i] = j
                    cc.co[i] = x
                    break

                    


