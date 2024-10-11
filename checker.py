# check if white cross is solved
def white_cross_check(dict):
    # check pieces around center piece on top side
    if dict['T'][0][1] == 'W' and dict['T'][1][0] == 'W' and dict['T'][1][2] == 'W' and dict['T'][2][1] == 'W':
        # check if adjacent sides match their center piece
        faces = ['F', 'L', 'R', 'B']
        for face in faces: 
            if dict[face][0][1] != dict[face][1][1]:
                return False
    return True

# Check if white corners are solved
def white_corners_check(dict):
    # bottom right corner
    if dict['T'][2][2] == 'W' and dict['F'][0][2] == dict['F'][1][1] and dict['R'][0][0] == dict['R'][1][1]:
        # bottom left corner
        if dict['T'][2][0] == 'W' and dict['F'][0][0] == dict['F'][1][1] and dict['L'][0][2] == dict['L'][1][1]:
            # top left corner
            if dict['T'][0][0] == 'W' and dict['L'][0][0] == dict['L'][1][1] and dict['B'][0][2] == dict['B'][1][1]:
                # top right corner
                if dict['T'][0][2] == 'W' and dict['B'][0][0] == dict['B'][1][1] and dict['R'][0][2] == dict['R'][1][1]:
                    return True
    return False

# Check if middle layer is solved
def middle_edge(dict):
    # middle F/L edge piece
    if dict['F'][1][0] == dict['F'][1][1] and dict['L'][1][2] == dict['L'][1][1]:
        # middle F/R edge piece
        if dict['F'][1][2] == dict['F'][1][1] and dict['R'][1][0] == dict['R'][1][1]:
            # middle B/R edge piece
            if dict['B'][1][0] == dict['B'][1][1] and dict['R'][1][2] == dict['R'][1][1]:
                # middle B/L edge piece
                if dict['B'][1][2] == dict['B'][1][1] and dict['L'][1][0] == dict['L'][1][1]:
                    return True
    return False

# Check which yellow pattern is present
def yellow_pattern_switch(dict):
    match True:
        case yellow_cross(dict):
            return 'Yellow Cross'
        case yellow_line(dict):
            return 'Yellow Line'
        case yellow_L(dict):
            return 'Yellow L'
        case yellow_dot(dict):
            return 'Yellow Dot'
        case _:
            return 'Invalid... no yellow pattern found'
        
# Check if yellow dot is present
def yellow_dot(dict):
    pos = [(0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2)]

    if dict['D'][1][1] == 'Y':
        for row, col in pos:
            if dict['D'][row][col] == 'Y':
                return False 
        return True 
    
    return False 

# Check if yellow L is present
def yellow_L(dict):
    if dict['D'][0][1] == 'Y' and dict['D'][1][0] == 'Y' and dict['D'][1][1] == 'Y':
        return True
    return False

# Check if yellow line is present
def yellow_line(dict):
    if dict['D'][1][0] == 'Y' and dict['D'][1][1] == 'Y' and dict['D'][1][2] == 'Y':
        return True
    return False

# Check if yellow cross is present
def yellow_cross(dict):
    if dict['D'][0][1] == 'Y' and dict['D'][1][0] == 'Y' and dict['D'][1][2] == 'Y' and dict['D'][2][1] == 'Y':
        return True
    return False

# Check adjacent yellow edge piece match
def yellow_edge(dict):
    faces = ['F', 'L', 'R', 'B']  
    for face in faces:
        if dict[face][2][1] != dict[face][1][1]: 
            return False
    return True

# Check if yellow corners are present
def yellow_corners(dict):
    # top F/L corner
    if {'Y', dict['L'][1][1], dict['F'][1][1]}.issubset({dict['D'][0][0], dict['L'][2][2], dict['F'][2][0]}):
        # top F/R corner
        if {'Y', dict['R'][1][1], dict['F'][1][1]}.issubset({dict['D'][0][2], dict['R'][2][0], dict['F'][2][0]}):
            # bottom B/L corner
            if {'Y', dict['L'][1][1], dict['B'][1][1]}.issubset({dict['D'][2][0], dict['L'][2][0], dict['B'][2][2]}):
                # bottom B/R corner
                if {'Y', dict['R'][1][1], dict['B'][1][1]}.issubset({dict['D'][2][2], dict['B'][2][0], dict['R'][2][2]}):
                    return True
    return False

# Check if yellow corners are solved
def yellow_corners_solved(dict):
    # top F/L corner
    if dict['D'][0][0] == 'Y' and dict['L'][2][2] == dict['L'][1][1] and dict['F'][2][0] == dict['F'][1][1]:
        # top F/R corner
        if dict['D'][0][2] == 'Y' and dict['R'][2][0] == dict['R'][1][1] and dict['F'][2][0] == dict['F'][1][1]:
            # bottom B/L corner
            if dict['D'][2][2] == 'Y' and dict['L'][2][0] == dict['L'][1][1] and dict['B'][2][2] == dict['B'][1][1]:
                # bottom B/R corner
                if dict['D'][2][2] == 'Y' and dict['B'][2][0] == dict['B'][1][1] and dict['R'][2][2] == dict['R'][1][1]:
                    return True
    return False