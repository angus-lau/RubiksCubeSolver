# import video_capture as vc
import checker as check
import permutations as perm
from collections import deque
import heapq

# current_state = vc.get_cube()

# start_state = {
#     'F': [['O', 'B', 'R'], ['R', 'G', 'R'], ['R', 'G', 'G']],
#     'B': [['Y', 'W', 'B'], ['W', 'B', 'W'], ['W', 'Y', 'W']],
#     'L': [['R', 'Y', 'G'], ['G', 'O', 'B'], ['G', 'Y', 'B']],
#     'T': [['Y', 'O', 'O'], ['R', 'W', 'W'], ['Y', 'O', 'Y']],
#     'D': [['W', 'O', 'R'], ['G', 'Y', 'Y'], ['O', 'B', 'O']]
# }

start_state = {
    'F': [['O', 'W', 'O'], ['G', 'G', 'R'], ['Y', 'Y', 'B']],
    'B': [['O', 'R', 'G'], ['O', 'B', 'G'], ['B', 'Y', 'B']],
    'L': [['R', 'Y', 'W'], ['R', 'O', 'O'], ['W', 'O', 'R']],
    'R': [['Y', 'O', 'Y'], ['B', 'R', 'B'], ['Y', 'B', 'W']],
    'T': [['W', 'W', 'B'], ['R', 'W', 'W'], ['G', 'G', 'G']],
    'D': [['G', 'B', 'R'], ['Y', 'Y', 'W'], ['O', 'G', 'R']]
}

goal_state = {
    'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
    'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
    'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
    'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
}

allowed_moves = ["T", "T'", "R", "R'", "F", "F'", "L", "L'", "B", "B'", "D", "D'", "T2", "R2", "F2", "L2", "B2", "D2"]

# test_state = {
#             'F': [['O', 'B', 'R'], ['R', 'G', 'R'], ['R', 'G', 'G']],
#             'B': [['Y', 'W', 'B'], ['W', 'B', 'W'], ['W', 'Y', 'W']],
#             'L': [['R', 'Y', 'G'], ['G', 'O', 'B'], ['G', 'Y', 'B']],
#             'T': [['Y', 'O', 'O'], ['R', 'W', 'W'], ['Y', 'O', 'Y']],
#             'D': [['W', 'O', 'R'], ['G', 'Y', 'Y'], ['O', 'B', 'O']]
#         }

def get_cube_state_string(cube):
    faces = ['F', 'B', 'L', 'R', 'T', 'D']
    return ''.join([''.join(''.join(row) for row in cube[face]) for face in faces])

def states_are_similar(state1, state2):
    return state1[:10] == state2[:10]  # Compare only the first 10 characters of the state

from collections import deque

def bidirectional_search(start_state, goal_state, allowed_moves):
    """Bidirectional search implementation with optimized pruning and early termination."""
    from collections import deque

    forward_queue = deque([(start_state, [])])
    backward_queue = deque([(goal_state, [])])

    forward_visited = {get_cube_state_string(start_state): []}  # Store move sequences
    backward_visited = {get_cube_state_string(goal_state): []}

    state_counter = 0  # Track expanded states

    while forward_queue and backward_queue:
        print(f"[DEBUG] Forward queue size: {len(forward_queue)}, Backward queue size: {len(backward_queue)}")

        solution = search_step(forward_queue, forward_visited, backward_visited, allowed_moves)
        if solution:
            return solution

        solution = search_step(backward_queue, backward_visited, forward_visited, allowed_moves)
        if solution:    
            return solution

        state_counter += 1
        if state_counter > 50_000:
            print("[ERROR] Too many states expanded. Stopping search.")
            return None

    print("[DEBUG] No solution found. Search ended.")
    return None

state_counter = 0  # Global counter for expanded states
MAX_DEPTH = 12  # Maximum depth for search

def search_step(queue, visited, opposite_visited, allowed_moves):
    """Expands one layer in the search tree with state pruning."""
    global state_counter

    if not queue:
        print("[DEBUG] Queue is empty! No states to expand.")
        return None

    state, moves = queue.popleft()  # Get next state (FIFO)

    if state_counter % 1000 == 0:
        print(f"[DEBUG] States expanded: {state_counter}, Queue size: {len(queue)}")

    # if len(moves) > 12:  # Limit depth
    #     print(f"[DEBUG] Reached max depth ({12}), stopping expansion for this branch.")
    #     return None

    priority_moves = ["T", "T'", "R", "R'"]  # Prioritize effective moves

    for move in allowed_moves:  # Prioritize good moves
        new_state = apply_move(state, move)
        state_string = get_cube_state_string(new_state)  # Convert to string

        if state_string in visited:
            continue  # Skip duplicate states
        visited[state_string] = moves + [move]  # Track move sequence

        # Stop early if the two searches meet
        for seen_state in opposite_visited:
            if state_string == seen_state:
            # if states_are_similar(state_string, seen_state):
                print(f"[SUCCESS] Similar states found! Move sequence: {moves + [move] + list(reversed(opposite_visited.get(seen_state, [])))}")
                return moves + [move] + list(reversed(opposite_visited.get(seen_state, [])))

        queue.append((new_state, moves + [move]))  # Add to queue (FIFO)

    state_counter += 1
    if state_counter > 1_000_000:
        print("[ERROR] Too many states! Breaking to avoid infinite loop.")
        return None

    return None

def apply_move(cube, move):
    new_cube = {face: [row[:] for row in cube[face]] for face in cube}

    move_base = move[0] 
    move_type = move[1:] if len(move) > 1 else ""
    if move_type == "'":
        perm.rotate_face_counter_clockwise(move_base, new_cube)
    elif move_type == "2":
        perm.rotate_face_clockwise(move_base, new_cube)
        perm.rotate_face_clockwise(move_base, new_cube)
    else:
        perm.rotate_face_clockwise(move_base, new_cube)

    return new_cube

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
                align_top_white_edges(cube, i, j)
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
    white_edges = find_white_edge_on_face(cube, 'T')
    while white_edges and attempts < max_attempts:
        print(f"--- Iteration {attempts + 1} ---")
        print(f"White edges found on 'D': {white_edges}") 
        if not white_edges:
                print("No more white edges on 'D'. Exiting.")
                break
        i, j = white_edges[0]
        print(f"Processing white edge at position (D, {i}, {j})") 
        adj_face, adj_i, adj_j, adj_sticker = get_adjacent_face_and_sticker(cube, 'T', i, j)
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
        if cube['T'][2][j] == 'W' and not is_edge_aligned_with_center(cube, 2, j):
            return ('T', 2, j)
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