# check if white cross is solved
def white_cross_check(cube):
    # check pieces around center piece on top side
    if cube['U'][0][1] == 'W' and cube['U'][1][0] == 'W' and cube['U'][1][2] == 'W' and cube['U'][2][1] == 'W': 
        # check if adjacent sides match their center piece
        faces = ['F', 'L', 'R', 'B']
        for face in faces: 
            if cube[face][0][1] != cube[face][1][1]:
                return False
        return True
    return False
 
# Check if white corners are solved
def white_corners_check(cube):
    # Bottom right corner
    if cube['U'][2][2] == 'W' and cube['F'][0][2] == cube['F'][1][1] and cube['R'][0][0] == cube['R'][1][1]:
        # bottom left corner
        if cube['U'][2][0] == 'W' and cube['F'][0][0] == cube['F'][1][1] and cube['L'][0][2] == cube['L'][1][1]:
            # top left corner
            if cube['U'][0][0] == 'W' and cube['L'][0][0] == cube['L'][1][1] and cube['B'][0][2] == cube['B'][1][1]:
                # top right corner
                if cube['U'][0][2] == 'W' and cube['B'][0][0] == cube['B'][1][1] and cube['R'][0][2] == cube['R'][1][1]:
                    return True
    return False

# Check if middle layer is solved
def middle_edge(cube):
    edges = [
        ('F', 'L'), ('F', 'R'),
        ('B', 'R'), ('B', 'L')
    ]
    for f1, f2 in edges:
        if cube[f1][1][0] != cube[f1][1][1] or cube[f2][1][2] != cube[f2][1][1]:
            return False
    return True

def yellow_pattern_switch(cube):
    patterns = {
        yellow_cross: 'Yellow Cross',
        yellow_line: 'Yellow Line',
        yellow_L: 'Yellow L',
        yellow_dot: 'Yellow Dot'
    }
    for pattern_func, pattern_name in patterns.items():
        if pattern_func(cube): 
            return pattern_name
        
# Check if yellow dot is present
def yellow_dot(cube):
    pos = [(0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2)]

    if cube['D'][1][1] == 'Y':
        for row, col in pos:
            if cube['D'][row][col] == 'Y':
                return False 
        return True 
    
    return False 

# Check if yellow L is present
# TODO: think about orientation of L 
def yellow_L(cube):
    if cube['D'][2][1] == 'Y' and cube['D'][1][2] == 'Y' and cube['D'][1][1] == 'Y':
        return True
    return False

# Check if yellow line is present
def yellow_line(cube):
    if cube['D'][1][0] == 'Y' and cube['D'][1][1] == 'Y' and cube['D'][1][2] == 'Y':
        return True
    return False

# Check if yellow cross is present
def yellow_cross(cube):
    if cube['D'][0][1] == 'Y' and cube['D'][1][0] == 'Y' and cube['D'][1][2] == 'Y' and cube['D'][2][1] == 'Y' and cube['D'][1][1] == 'Y':
       if yellow_all_edge(cube):
           return True
    return False

# Check adjacent yellow edge piece match
def yellow_all_edge(cube):
    faces = ['F', 'L', 'R', 'B']  
    for face in faces:
        if cube[face][2][1] != cube[face][1][1]: 
            return False
    return True

# Check if yellow opposite edge pieces are in the right position
def yellow_opposite_edge(cube):
    if cube['F'][2][1] == cube['F'][1][1] and cube['B'][2][1] == cube['B'][1][1]:
        return True
    
    if cube['L'][2][1] == cube['L'][1][1] and cube['R'][2][1] == cube['R'][1][1]:
        return True
    
    return False

#TODO
# Check if 2 adjacent yellow edges are in the right position
def yellow_adjacent_edge(cube):
    pairs = [('F', 'L'), ('F', 'R'), ('R', 'B'), ('R', 'L')]
    for face1, face2 in pairs:
        if cube[face1][2][1] == cube[face1][1][1] and cube[face2][2][1] == cube[face2][1][1]:
            return True
    return False

# Check if yellow corners are in the right corner
def yellow_corners(cube):
    # top F/L corner
    if {'Y', cube['L'][1][1], cube['F'][1][1]}.issubset({cube['D'][0][0], cube['L'][2][2], cube['F'][2][0]}):
        # top F/R corner
        if {'Y', cube['R'][1][1], cube['F'][1][1]}.issubset({cube['D'][0][2], cube['R'][2][0], cube['F'][2][2]}):
            # bottom B/L corner
            if {'Y', cube['L'][1][1], cube['B'][1][1]}.issubset({cube['D'][2][0], cube['L'][2][0], cube['B'][2][2]}):
                # bottom B/R corner
                if {'Y', cube['R'][1][1], cube['B'][1][1]}.issubset({cube['D'][2][2], cube['B'][2][0], cube['R'][2][2]}):
                    return True
    return False

# Check if yellow corners are solved
def yellow_corners_solved(cube):
    # top F/L corner
    if cube['D'][0][0] == 'Y' and cube['L'][2][2] == cube['L'][1][1] and cube['F'][2][0] == cube['F'][1][1]:
        # top F/R corner
        if cube['D'][0][2] == 'Y' and cube['R'][2][0] == cube['R'][1][1] and cube['F'][2][2] == cube['F'][1][1]:
            # bottom B/L corner
            if cube['D'][2][0] == 'Y' and cube['L'][2][0] == cube['L'][1][1] and cube['B'][2][2] == cube['B'][1][1]:
                # bottom B/R corner
                if cube['D'][2][2] == 'Y' and cube['B'][2][0] == cube['B'][1][1] and cube['R'][2][2] == cube['R'][1][1]:
                    return True
    return False