import video_capture as vc
import checker as check
import permutations as perm

# current_state = vc.get_cube()

test_state = {
            'F': [['O', 'B', 'R'], ['R', 'G', 'R'], ['R', 'G', 'G']],
            'B': [['Y', 'W', 'B'], ['W', 'B', 'W'], ['W', 'Y', 'W']],
            'L': [['R', 'Y', 'G'], ['G', 'O', 'B'], ['G', 'Y', 'B']],
            'T': [['Y', 'O', 'O'], ['R', 'W', 'W'], ['Y', 'O', 'Y']],
            'D': [['W', 'O', 'R'], ['G', 'Y', 'Y'], ['O', 'B', 'O']]
        }


# Main function to solve white cross
def solve_white_cross(cube):
    while True:
        white_edges = find_all_white_edges(cube)
        if not white_edges:
            break
        for edge in white_edges:
            face, i, j = edge
            if face == 'D':
                align_bottom_white_edges(cube)
            elif face == 'T':
                align_top_white_edge(cube, i, j)
            else:
                align_side_white_edge(cube, face, i, j)

# Locate white edges
def find_all_white_edges(cube):
    white_edges = []
    for face, grid in cube.items():
        for row_index, row in enumerate(grid):
            for col_index, color in enumerate(row):
                if color == 'W':
                    white_edges.append((face, row_index, col_index))
    return white_edges

def get_adjacent_face_and_sticker(cube, face, i, j):
    edge_map = {
        # Front face edges
        ('F', 0, 1): ('T', 2, 1),  # Front top edge -> Top bottom edge
        ('F', 1, 0): ('L', 1, 2),  # Front left edge -> Left right edge
        ('F', 1, 2): ('R', 1, 0),  # Front right edge -> Right left edge
        ('F', 2, 1): ('D', 0, 1),  # Front bottom edge -> Down top edge
        
        # Back face edges
        ('B', 0, 1): ('T', 0, 1),  # Back top edge -> Top top edge
        ('B', 1, 0): ('R', 1, 2),  # Back left edge -> Right right edge
        ('B', 1, 2): ('L', 1, 0),  # Back right edge -> Left left edge
        ('B', 2, 1): ('D', 2, 1),  # Back bottom edge -> Down bottom edge
        
        # Left face edges
        ('L', 0, 1): ('T', 1, 0),  # Left top edge -> Top left edge
        ('L', 1, 0): ('B', 1, 2),  # Left left edge -> Back right edge
        ('L', 1, 2): ('F', 1, 0),  # Left right edge -> Front left edge
        ('L', 2, 1): ('D', 1, 0),  # Left bottom edge -> Down left edge
        
        # Right face edges
        ('R', 0, 1): ('T', 1, 2),  # Right top edge -> Top right edge
        ('R', 1, 0): ('F', 1, 2),  # Right left edge -> Front right edge
        ('R', 1, 2): ('B', 1, 0),  # Right right edge -> Back left edge
        ('R', 2, 1): ('D', 1, 2),  # Right bottom edge -> Down right edge
        
        # Top face edges
        ('T', 0, 1): ('B', 0, 1),  # Top top edge -> Back top edge
        ('T', 1, 0): ('L', 0, 1),  # Top left edge -> Left top edge
        ('T', 1, 2): ('R', 0, 1),  # Top right edge -> Right top edge
        ('T', 2, 1): ('F', 0, 1),  # Top bottom edge -> Front top edge
        
        # Down face edges
        ('D', 0, 1): ('F', 2, 1),  # Down top edge -> Front bottom edge
        ('D', 1, 0): ('L', 2, 1),  # Down left edge -> Left bottom edge
        ('D', 1, 2): ('R', 2, 1),  # Down right edge -> Right bottom edge
        ('D', 2, 1): ('B', 2, 1),  # Down bottom edge -> Back bottom edge   
    }
    # Get adjacent position
    adj_face, adj_i, adj_j = edge_map.get((face, i, j))
    # Return adjacent face and its color at that position
    return adj_face, cube[adj_face][adj_i][adj_j]
    # returns 'L', cube['L'][2][1]

def align_bottom_white_edges(cube):
    while True:
        white_edges = find_white_edge_on_face(cube, 'D')
        if not white_edges:
            break
        i,j = white_edges[0]
        adj_face, adj_sticker = get_adjacent_face_and_sticker(cube, 'D', i, j)  
        if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
            #rotate specific face clockwise
            perm.rotate_face_clockwise(cube, adj_face)
            perm.rotate_face_clockwise(cube, adj_face)
        else:
            perm.rotate_bottom_clockwise(cube)
    
# Find the next white edge that needs solving 
def find_next_unaligned_white_edge(cube):
    # Check all faces except top first
    for face in ['F', 'B', 'L', 'R', 'D']:
        # Edge pieces are always in these positions on a face:
        for i, j in [(1,0), (1,2), (0,1), (2,1)]:  # middle-left, middle-right, top-middle, bottom-middle
            if cube[face][i][j] == 'W':
                return (face, i, j)
    
    # If no edges found on other faces, check top face for misplaced edges
    for j in [1, 0, 2]:  # Check positions on top face
        if cube['T'][2][j] == 'W' and not is_edge_aligned_with_center(cube, 2, j):
            return ('T', 2, j)
    return None

def find_white_edge_on_face(cube, face):
    found = []
    for i, j in [(1,0), (1,2), (0,1), (2,1)]:  # middle-left, middle-right, top-middle, bottom-middle
        if cube[face][i][j] == 'W':
            found.append((i, j))
    return found

def is_edge_aligned_with_center(cube, adj_face, adj_sticker):
    return adj_sticker == cube[adj_face][1][1]

def align_top_white_edge(cube, i, j):
    attempts = 0
    while attempts < 4:
        adj_face, adj_sticker = get_adjacent_face_and_sticker(cube, 'T', i, j)
        if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
            perm.rotate_face_clockwise(cube, adj_face)
            return
        else:
            perm.rotate_top_clockwise(cube)
            attempts += 1

def align_side_white_edge(cube, face, i, j):
    adj_face, adj_sticker = get_adjacent_face_and_sticker(cube, face, i, j)
    attempts = 0
    while not is_edge_aligned_with_center(cube, adj_face, adj_sticker) and attempts < 4: 
        perm.rotate_face_clockwise(cube, face)
        attempts += 1
    if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
        perm.rotate_face_clockwise(cube, adj_face)