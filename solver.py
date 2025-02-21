# import video_capture as vc
import checker as check
import permutations as perm
from collections import deque
import copy

# current_state = vc.get_cube()

start_state = {
    'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
    'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
    'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['W', 'O', 'R']],
    'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
    'U': [['W', 'W', 'B'], ['R', 'W', 'W'], ['G', 'G', 'G']],
    'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
}

GOAL_STATE = {
    'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
    'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
    'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
    'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
}

ALLOWED_MOVES = ["T", "T'", "R", "R'", "F", "F'", "L", "L'", "B", "B'", "D", "D'", "T2", "R2", "F2", "L2", "B2", "D2"]

# Convert the cube state to a string
def get_cube_state_string(cube):
    faces = ['F', 'B', 'L', 'R', 'U', 'D']
    return ''.join([''.join(''.join(row) for row in cube[face]) for face in faces])

def states_are_similar(state1, state2):
    return state1 == state2  

def bidirectional_search(start_state, goal_state, allowed_moves, max_depth=10):    
    # Track current state, alongside moves taken to reach it
    forward_queue = deque([(start_state, [])])
    backward_queue = deque([(goal_state, [])])

    # Track visited, using dict for O(1) lookup
    forward_visited = {get_cube_state_string(start_state): []}
    backward_visited = {get_cube_state_string(goal_state): []}

    while forward_queue and backward_queue:
        # Search for steps while there are still elements in both queues
        print(f"[DEBUG] Forward queue size: {len(forward_queue)}, Backward queue size: {len(backward_queue)}")

        solution = search_step(forward_queue, forward_visited, backward_visited, allowed_moves, max_depth)
        if solution:
            return solution

        solution = search_step(backward_queue, backward_visited, forward_visited, allowed_moves, max_depth)
        if solution:    
            return solution

    print("[DEBUG] No solution found. Search ended.")
    return None

def search_step(queue, visited, opposite_visited, allowed_moves, max_depth):
    if not queue:
        print("[DEBUG] Queue is empty! No states to expand.")
        return None

    # fifo queue to move to next breadth
    state, moves = queue.popleft()

    if len(moves) >= max_depth:
        return None
    
    if is_white_cross_solved(state):
        print(f"[SUCCESS] White cross solved! Move sequence: {moves}")
        return moves
    
    # Applies every legal move
    for move in allowed_moves:
        if moves and is_reverse_move(moves[-1], move):
            continue
        new_state = apply_move(state, move)
        state_string = get_cube_state_string(new_state)

        # Skip if state has been visited
        if state_string in visited:
            continue
        # If not visited, add to visited dictionary with moves
        visited[state_string] = moves + [move]

        # Stop early if the two searches meet
        # for seen_state in opposite_visited:
        #     if state_string == seen_state:
        if state_string in opposite_visited:
            print(f"[SUCCESS] States match! Move sequence: {moves + [move] + list(reversed(opposite_visited[state_string]))}")
            return moves + [move] + list(reversed(opposite_visited[state_string]))

        # add new state into queue to explore its children 
        queue.append((new_state, moves + [move]))  

    return None

def is_reverse_move(last_move, new_move):
    reverse_moves = {
        "T": "T'", "T'": "T", "R": "R'", "R'": "R",
        "F": "F'", "F'": "F", "L": "L'", "L'": "L",
        "B": "B'", "B'": "B", "D": "D'", "D'": "D",
        "T2": "T2", "R2": "R2", "F2": "F2", "L2": "L2", "B2": "B2", "D2": "D2"
    }

    return reverse_moves.get(last_move) == new_move

def apply_move(cube, move):
    new_cube = copy.deepcopy(cube)

    move_base = move[0]
    move_type = move[1:] if len(move) > 1 else ""
    # prime notation - counter clockwise
    if move_type == "'":
        perm.rotate_face_counter_clockwise(move_base, new_cube)
    # double notation - 180 degree
    elif move_type == "2":
        perm.rotate_face_clockwise(move_base, new_cube)
        perm.rotate_face_clockwise(move_base, new_cube)
    # clockwise
    else:
        perm.rotate_face_clockwise(move_base, new_cube)

    return new_cube

def is_white_cross_solved(cube):
    center_color = cube['U'][1][1]
    white_edges = [
        cube['D'][0][1], cube['D'][1][0], cube['D'][1][2], cube['D'][2][1]
    ]

    return all(color == center_color for color in white_edges)
    





# # Main function to solve white cross
# def solve_white_cross(cube):
#     while True:
#         white_edges = find_all_white_edges(cube)
#         if not white_edges:
#             break
#         for edge in white_edges:
#             face, i, j = edge
#             if face == 'D':
#                 align_bottom_white_edges(cube)
#             elif face == 'U':
#                 align_top_white_edges(cube, i, j)
#             else:
#                 align_side_white_edge(cube, face, i, j)

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
        ('F', 0, 1): ('U', 2, 1),  # Front top edge -> Top bottom edge
        ('F', 1, 0): ('L', 1, 2),  # Front left edge -> Left right edge
        ('F', 1, 2): ('R', 1, 0),  # Front right edge -> Right left edge
        ('F', 2, 1): ('D', 0, 1),  # Front bottom edge -> Down top edge
        
        # Back face edges
        ('B', 0, 1): ('U', 0, 1),  # Back top edge -> Top top edge
        ('B', 1, 0): ('R', 1, 2),  # Back left edge -> Right right edge
        ('B', 1, 2): ('L', 1, 0),  # Back right edge -> Left left edge
        ('B', 2, 1): ('D', 2, 1),  # Back bottom edge -> Down bottom edge
        
        # Left face edges
        ('L', 0, 1): ('U', 1, 0),  # Left top edge -> Top left edge
        ('L', 1, 0): ('B', 1, 2),  # Left left edge -> Back right edge
        ('L', 1, 2): ('F', 1, 0),  # Left right edge -> Front left edge
        ('L', 2, 1): ('D', 1, 0),  # Left bottom edge -> Down left edge
        
        # Right face edges
        ('R', 0, 1): ('U', 1, 2),  # Right top edge -> Top right edge
        ('R', 1, 0): ('F', 1, 2),  # Right left edge -> Front right edge
        ('R', 1, 2): ('B', 1, 0),  # Right right edge -> Back left edge
        ('R', 2, 1): ('D', 1, 2),  # Right bottom edge -> Down right edge
        
        # Top face edges
        ('U', 0, 1): ('B', 0, 1),  # Top top edge -> Back top edge
        ('U', 1, 0): ('L', 0, 1),  # Top left edge -> Left top edge
        ('U', 1, 2): ('R', 0, 1),  # Top right edge -> Right top edge
        ('U', 2, 1): ('F', 0, 1),  # Top bottom edge -> Front top edge
        
        # Down face edges
        ('D', 0, 1): ('F', 2, 1),  # Down top edge -> Front bottom edge
        ('D', 1, 0): ('L', 2, 1),  # Down left edge -> Left bottom edge
        ('D', 1, 2): ('R', 2, 1),  # Down right edge -> Right bottom edge
        ('D', 2, 1): ('B', 2, 1),  # Down bottom edge -> Back bottom edge   
    }
    # Get adjacent position
    adj_face, adj_i, adj_j = edge_map.get((face, i, j))
    # Return adjacent face and its color at that position
    return adj_face, adj_i, adj_j, cube[adj_face][adj_i][adj_j]
    # returns 'L', cube['L'][2][1]

def print_cube_state(cube):
    """Print the Rubik's Cube state with each face displayed in a grid format."""
    for face, grid in cube.items():
        print(f"{face} face:")
        for row in grid:
            print(" ".join(row))
        print()

def align_bottom_white_edges(cube):
    max_attempts = 5
    attempts = 0

    white_edges = find_white_edge_on_face(cube, 'D')

    while white_edges and attempts < max_attempts:
        print(f"--- Iteration {attempts + 1} ---")
        print(f"White edges found on 'D': {white_edges}") 

        if not white_edges:
            print("No more white edges on 'D'. Exiting.")
            break

        i, j = white_edges[0] 
        print(f"Processing white edge at position (D, {i}, {j})") 

        # Get the adjacent face and sticker
        adj_face, adj_i, adj_j, adj_sticker = get_adjacent_face_and_sticker(cube, 'D', i, j)
        print(f"Adjacent face: {adj_face}, Adjacent Position: {adj_i}, {adj_j}, Adjacent sticker: {adj_sticker}")

        # Check alignment
        if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
            print(f"Edge is aligned with center of {adj_face}. Rotating face clockwise twice.")  
            # Rotate the adjacent face clockwise twice
            perm.rotate_face_clockwise(adj_face, cube)
            perm.rotate_face_clockwise(adj_face, cube)
            # remove the edge from the list
            white_edges.pop(0)
        else:
            print(f"Edge is not aligned. Rotating the bottom face clockwise.")  
            # Rotate the bottom face to reattempt alignment
            perm.rotate_bottom_clockwise(cube)
       # Recalculate the white edges after each move
        white_edges = find_white_edge_on_face(cube, 'D')
        print(f"Updated white edges on 'D': {white_edges}")  
        print("Cube state after iteration:")
        print_cube_state(cube)  
        attempts += 1

    if attempts >= max_attempts:
        print("Reached maximum attempts.")  

def align_top_white_edges(cube, i, j):
    max_attempts = 5
    attempts = 0
    white_edges = find_white_edge_on_face(cube, 'U')
    while white_edges and attempts < max_attempts:
        print(f"--- Iteration {attempts + 1} ---")
        print(f"White edges found on 'D': {white_edges}") 
        if not white_edges:
                print("No more white edges on 'D'. Exiting.")
                break
        i, j = white_edges[0]
        print(f"Processing white edge at position (D, {i}, {j})") 
        adj_face, adj_i, adj_j, adj_sticker = get_adjacent_face_and_sticker(cube, 'U', i, j)
        print(f"Adjacent face: {adj_face}, Adjacent Position: {adj_i}, {adj_j}, Adjacent sticker: {adj_sticker}")

        if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
            white_edges.pop(0)
            if len(white_edges) > 0:
                #TODO: Rotate aligned edge down to prevent it from getting misaligned when working on the other edge(s)
                move_edge_down()
        else:
            perm.rotate_top_clockwise(cube)
            attempts += 1
        
        if attempts >= max_attempts:
            print("Reached maximum attempts.")
            break

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
        if cube['U'][2][j] == 'W' and not is_edge_aligned_with_center(cube, 2, j):
            return ('U', 2, j)
    return None

def find_white_edge_on_face(cube, face):
    # Check if there are any white edges on the face
    found = []
    for i, j in [(1,0), (1,2), (0,1), (2,1)]:  # middle-left, middle-right, top-middle, bottom-middle
        if cube[face][i][j] == 'W':
            found.append((i, j))
    return found

def is_edge_aligned_with_center(cube, adj_face, adj_sticker):
    return adj_sticker == cube[adj_face][1][1]

def align_side_white_edge(cube, face, i, j):
    adj_face, adj_sticker = get_adjacent_face_and_sticker(cube, face, i, j)
    attempts = 0
    while not is_edge_aligned_with_center(cube, adj_face, adj_sticker) and attempts < 4: 
        perm.rotate_face_clockwise(cube, face)
        attempts += 1
    if is_edge_aligned_with_center(cube, adj_face, adj_sticker):
        perm.rotate_face_clockwise(cube, adj_face)