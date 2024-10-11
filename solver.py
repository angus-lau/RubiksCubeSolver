import rubiks_cube_class as rc
import checker

#TODO adjust neighbour faces as well
# Rotate face clockwise
def rotate_face_clockwise(face, cube):
    # Get current cube state
    curr_cube = rc.get_faces()
    # Get colors of the face
    curr_face = rc.get_faces()[face]
    # rotate clockwise
    rotated_face = list(zip(*curr_face[::-1]))
    # Update face colors
    cube.update_face(face, rotated_face)

#TODO adjust neighbour faces as well
# Rotate face counter clockwise
def rotate_face_counter_clockwise(face, cube):
    # Get current cube state
    curr_cube = rc.get_faces()
    # Get colors of the face
    curr_face = rc.get_faces()[face]
    # rotate counter clockwise
    rotated_face = list(reversed(list(zip(*curr_face))))
    # Update face colors
    cube.update_face(face, rotated_face)

#TODO rotate top row clockwise
#TODO rotate top row counter clockwise
#TODO rotate bottom row clockwise
#TODO rotate bottom row counter clockwise
#TODO rotate right column clockwise
#TODO rotate right column counter clockwise 
#TODO rotate left column clockwise
#TODO rotate left column counter clockwise