# check if white cross is solved
def white_cross_check(dict):
    # # {
    #     #     'F': [['R', 'R', 'R'], 
    #                 ['R', 'R', 'R'], 
    #                 ['R', 'R', 'R']],

    #     #     'B': [['Y', 'Y', 'Y'], 
    #                 ['Y', 'Y', 'Y'], 
    #                 ['Y', 'Y', 'Y']],

    #     #     'L': [['G', 'G', 'G'], 
    #                 ['G', 'G', 'G'], 
    #                 ['G', 'G', 'G']],

    #     #     'R': [['B', 'B', 'B'], 
    #                 ['B', 'B', 'B'], 
    #                 ['B', 'B', 'B']],

    #     #     'T': [['W', 'W', 'W'], 
    #                 ['W', 'W', 'W'], 
    #                 ['W', 'W', 'W']],

    #     #     'D': [['O', 'O', 'O'], 
    #                 ['O', 'O', 'O'], 
    #                 ['O', 'O', 'O']]
    #     # }

    # check pieces around center piece on top side
    if dict['T'][0][1] == 'W' and dict['T'][1][0] == 'W' and dict['T'][1][2] == 'W' and dict['T'][2][1] == 'W':
        # check if adjacent sides match their center piece
        if dict['F'][0][1] == dict['F'][1][1]\
        and dict['R'][0][1] == dict['R'][1][1]\
        and dict['L'][0][1] == dict['L'][1][1]\
        and dict['B'][0][1] == dict['B'][1][1]:
           return True
    return False

# check if white corners are solved
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

