import rubiks_cube_class as rc

def rotate_face_clockwise(face, cube):
    cube[face] = [list(row) for row in zip(*cube[face][::-1])]
    update_adjacent_faces(face, cube)


def update_adjacent_faces(face, cube):
    if face == 'F':
        top_row = cube['T'][2]
        right_col = [cube['R'][i][0] for i in range(3)]
        bottom_row = cube['D'][0]
        left_col = [cube['L'][i][2] for i in range(3)]

        # Perform clockwise rotation of adjacent edges
        cube['T'][2] = left_col[::-1]
        for i in range(3):
            cube['R'][i][0] = top_row[i]
        cube['D'][0] = right_col[::-1]
        for i in range(3):
            cube['L'][i][2] = bottom_row[i]

    elif face == 'B':
        top_row = cube['T'][0]
        left_col = [cube['L'][i][0] for i in range(3)]
        bottom_row = cube['D'][2]
        right_col = [cube['R'][i][2] for i in range(3)]

        # Perform clockwise rotation of adjacent edges
        cube['T'][0] = right_col
        for i in range(3):
            cube['L'][i][0] = bottom_row[i]
        cube['D'][2] = left_col[::-1]
        for i in range(3):
            cube['R'][i][2] = top_row[i]

def rotate_face_counter_clockwise(face, cube):
      if face == 'B':
           cube[face] = [list(row) for row in zip(*cube[face][::-1])]
           update_adjacent_faces_counterclockwise(face, cube)
      else:
            cube[face] = [list(row) for row in reversed(list(zip(*cube[face])))]
            update_adjacent_faces_counterclockwise(face, cube)

def update_adjacent_faces_counterclockwise(face, cube):
    if face == 'F':
        rotate_front_counter_clockwise(cube)

    elif face == 'B':
        rotate_back_counter_clockwise(cube)

def rotate_front_counter_clockwise(cube):
      top_row = cube['T'][2]
      right_col = [cube['R'][i][0] for i in range(3)]
      bottom_row = cube['D'][0]
      left_col = [cube['L'][i][2] for i in range(3)]

      # Perform counterclockwise rotation of adjacent edges
      cube['T'][2] = right_col
      for i in range(3):
            cube['R'][i][0] = bottom_row[::-1][i]
      cube['D'][0] = left_col
      for i in range(3):
           cube['L'][i][2] = top_row[::-1][i]

def rotate_back_counter_clockwise(cube):
      top_row = cube['T'][0]
      left_col = [cube['L'][i][0] for i in range(3)]
      bottom_row = cube['D'][2]
      right_col = [cube['R'][i][2] for i in range(3)]

      # Perform counterclockwise rotation of adjacent edges
      cube['T'][0] = right_col
      for i in range(3):
           cube['L'][i][0] = top_row[i]
      cube['D'][2] = left_col
      for i in range(3):
           cube['R'][i][2] = bottom_row[::-1][i]
     


def rotate_bottom_counter_clockwise(cube):
      top_bottom_row = cube['T'][0]
      left_first_col = [cube['L'][i][0] for i in range(3)]
      bottom_last_row = cube['D'][2]
      right_last_col = [cube['R'][i][2] for i in range(3)]

      cube['T'][0] = right_last_col
      for i in range(3):
            cube['L'][i][0] = bottom_last_row[i]
      cube['D'][2] = left_first_col
      for i in range(3):
            cube['R'][i][2] = top_bottom_row[i]

def rotate_top_clockwise(cube):
      # Store original values
      left_orig_top_row = cube['L'][0]
      right_orig_top_row = cube['R'][0]
      front_orig_top_row = cube['F'][0]
      back_orig_top_row = cube['B'][0]

      # Update values
      cube['L'][0] = front_orig_top_row
      cube['R'][0] = back_orig_top_row
      cube['F'][0] = right_orig_top_row
      cube['B'][0] = left_orig_top_row

      # Update top face by rotating array 
      cube['T'] = [list(row) for row in zip(*cube['T'][::-1])]

def rotate_top_counter_clockwise(cube):
      # Store original values
      left_orig_top_row = cube['L'][0]
      right_orig_top_row = cube['R'][0]
      front_orig_top_row = cube['F'][0]
      back_orig_top_row = cube['B'][0]

      # Update values
      cube['L'][0] = back_orig_top_row
      cube['R'][0] = front_orig_top_row
      cube['F'][0] = left_orig_top_row
      cube['B'][0] = right_orig_top_row

      # Update top face by rotating array
      cube['T'] = [list(row) for row in reversed(list(zip(*cube['T'])))]

def rotate_bottom_clockwise(cube):
      # Store original values
      left_orig_bot_row = cube['L'][2]
      right_orig_bot_row = cube['R'][2]
      front_orig_bot_row = cube['F'][2]
      back_orig_bot_row = cube['B'][2]

      # Update values
      cube['L'][2] = front_orig_bot_row
      cube['R'][2] = back_orig_bot_row
      cube['F'][2] = right_orig_bot_row
      cube['B'][2] = left_orig_bot_row

      # Update bottom face by rotating array 
      cube['D'] = [list(row) for row in reversed(list(zip(*cube['D'])))]

def rotate_bottom_counter_clockwise(cube):
      # Store original values
      left_orig_bot_row = cube['L'][2]
      right_orig_bot_row = cube['R'][2]
      front_orig_bot_row = cube['F'][2]
      back_orig_bot_row = cube['B'][2]

      cube['L'][2] = back_orig_bot_row
      cube['R'][2] = front_orig_bot_row
      cube['F'][2] = left_orig_bot_row
      cube['B'][2] = right_orig_bot_row

      # Update bottom face by rotating array
      cube['D'] = [list(row) for row in list(zip(*cube['D'][::-1]))]

def rotate_right_column_clockwise(cube):
      # Store original values
      top_orig_right_column = [cube['T'][i][2] for i in range(3)]
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update values
      for i in range(3):
            cube['T'][i][2] = front_orig_right_column[i]
            cube['F'][i][2] = bottom_orig_right_column[i]
            cube['D'][i][2] = back_orig_right_column[2-i]
            cube['B'][i][0] = top_orig_right_column[2-i]

      # Update right face by rotating array
      cube['R'] = [list(row) for row in zip(*cube['R'][::-1])]

def rotate_right_column_counter_clockwise(cube):
      # Store original values
      top_orig_right_column = [cube['T'][i][2] for i in range(3)]
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update right column of top face with right column of back face
      for i in range(3):
            cube['T'][i][2] = back_orig_right_column[2-i]
            cube['F'][i][2] = top_orig_right_column[i]
            cube['B'][i][0] = bottom_orig_right_column[2-i]
            cube['D'][i][2] = front_orig_right_column[i]

      # Update right face by rotating array
      cube['R'] = [list(row) for row in reversed(list(zip(*cube['R'])))]

def rotate_left_column_clockwise(cube):
      # Store original values
      top_orig_left_column = [cube['T'][i][0] for i in range(3)]
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update values
      for i in range(3):
            cube['T'][i][0] = back_orig_left_column[2 - i]
            cube['F'][i][0] = top_orig_left_column[i]
            cube['D'][i][0] = front_orig_left_column[i]
            cube['B'][i][2] = bottom_orig_left_column[2 - i]

      # Update left face by rotating array
      cube['L'] = [list(row) for row in zip(*cube['L'][::-1])]

def rotate_left_column_counter_clockwise(cube):
      # Store original values
      top_orig_left_column = [cube['T'][i][0] for i in range(3)]
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update values
      for i in range(3):
            cube['T'][i][0] = front_orig_left_column[i]            
            cube['F'][i][0] = bottom_orig_left_column[i]           
            cube['D'][i][0] = back_orig_left_column[2 - i]         
            cube['B'][i][2] = top_orig_left_column[2 - i]          

      # Update left face by rotating array counterclockwise
      cube['L'] = [list(row) for row in zip(*cube['L'])][::-1]