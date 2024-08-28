class RubiksCube:
    def __init__(self):
        self.faces = {
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'T': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]
        }

    #update colors on specific face
    def update_face(self, face, colors):
        self.faces[face] = colors

    #display cube
    def displayCube(self):
        print("Current state of the Rubik's Cube:")
        for face, colors in self.faces.items():
            print(f"{face}:")
            for row in colors:
                print(row)
            print()