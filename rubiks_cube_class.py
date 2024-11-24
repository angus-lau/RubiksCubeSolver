class RubiksCube:
    def __init__(self):
        self.faces = {
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

     # Get faces
    def get_cube(self):
        return self.faces

    # Update colors on specific face
    def update_face(self, face, colors):
        self.faces[face] = colors

    # Display cube
    def display_cube_face(self, face):
        print(f"Current state of {face}.")
        print(self.faces[face])