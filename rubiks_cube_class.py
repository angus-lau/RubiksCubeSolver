class RubiksCube:
    def __init__(self):
        self.faces = {
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        }

     # Get faces
    def get_faces(self):
        return self.faces

    # Update colors on specific face
    def update_face(self, face, colors):
        self.faces[face] = colors

    # Display cube
    def displayCube(self, face):
        print(f"Current state of {face}.")
        print(self.faces[face])