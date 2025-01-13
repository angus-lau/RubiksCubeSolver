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
           rotate_face_clockwise(face, cube)
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
      cube['T'][0] = left_col[::-1]
      for i in range(3):
           cube['L'][i][0] = top_row[i]
      cube['D'][2] = right_col[::-1]
      for i in range(3):
           cube['R'][i][2] = bottom_row[i]
     


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
      # # Store original bottom row of left face
      # left_orig_bottom_row = cube['L'][2]

      # # Store original bottom row of right face
      # right_orig_bottom_row = cube['R'][2]

      # # Update bottom row of left face with bottom row of back face
      # cube['L'][2] = cube['B'][2]

      # # Update bottom row of right face with bottom row of front face
      # cube['R'][2] = cube['F'][2]

      # # Update bottom row of front face with original left bottom row
      # cube['F'][2] = left_orig_bottom_row

      # # Update bottom row of back face with original right bottom row
      # cube['B'][2] = right_orig_bottom_row

      # # Update bottom face by rotating array
      # cube['D'] = list(reversed(list(zip(*cube['D']))))

                  

def rotate_top_clockwise(cube):
      # Store original top row of left face
      left_orig_top_row = cube['L'][0]

      # Store original top row of right face
      right_orig_top_row = cube['R'][0]

      # Update top row of left face with top row of front face
      cube['L'][0] = cube['F'][0]

      # Update top row of right face with top row of back face
      cube['R'][0] = cube['B'][0]

      # Update top row of front face with original right top row
      cube['F'][0] = right_orig_top_row

      # Update top row of back face with original left top row
      cube['B'][0] = left_orig_top_row

      # Update top face by rotating array 
      cube['T'] = list(zip(*cube['T'][::-1]))

def rotate_top_counter_clockwise(cube):
      # Store original top row of left face
      left_orig_top_row = cube['L'][0]

      # Store original top row of right face
      right_orig_top_row = cube['R'][0]

      # Update top row of left face with top row of back face
      cube['L'][0] = cube['B'][0]

      # Update top row of right face with top row of front face
      cube['R'][0] = cube['F'][0]

      # Update top row of front face with original left top row
      cube['F'][0] = left_orig_top_row

      # Update top row of back face with original right top row
      cube['B'][0] = right_orig_top_row

      # Update top face by rotating array
      cube['T'] = list(reversed(list(zip(*cube['T']))))

def rotate_bottom_clockwise(cube):
      # Store original bottom row of left face
      left_orig_bottom_row = cube['L'][2]

      # Store original bottom row of right face
      right_orig_bottom_row = cube['R'][2]

      # Update bottom row of left face with bottom row of front face
      cube['L'][2] = cube['F'][2]

      # Update bottom row of right face with bottom row of back face
      cube['R'][2] = cube['B'][2]

      # Update bottom row of front face with original right bottom row
      cube['F'][2] = right_orig_bottom_row

      # Update bottom row of back face with original left bottom row
      cube['B'][2] = left_orig_bottom_row

      # Update bottom face by rotating array 
      cube['D'] = list(zip(*cube['D'][::-1]))

def rotate_bottom_counter_clockwise(cube):
      # Store original bottom row of left face
      left_orig_bottom_row = cube['L'][2]

      # Store original bottom row of right face
      right_orig_bottom_row = cube['R'][2]

      # Update bottom row of left face with bottom row of back face
      cube['L'][2] = cube['B'][2]

      # Update bottom row of right face with bottom row of front face
      cube['R'][2] = cube['F'][2]

      # Update bottom row of front face with original left bottom row
      cube['F'][2] = left_orig_bottom_row

      # Update bottom row of back face with original right bottom row
      cube['B'][2] = right_orig_bottom_row

      # Update bottom face by rotating array
      cube['D'] = list(reversed(list(zip(*cube['D']))))

def rotate_right_column_clockwise(cube):
      # Store original right column of top face
      top_orig_right_column = [cube['T'][i][2] for i in range(3)]

      # Store original right column of front face
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]

      # Store original right column of bottom face
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]

      # Store original right column of back face
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update right column of top face with right column of front face
      for i in range(3):
            cube['T'][i][2] = front_orig_right_column[i]

      # Update right column of front face with right column of bottom face
      for i in range(3):
            cube['F'][i][2] = bottom_orig_right_column[i]

      # Update right column of bottom face with right column of back face
      for i in range(3):
            cube['D'][i][2] = back_orig_right_column[i]

      # Update right column of back face with right column of top face
      for i in range(3):
            cube['B'][i][2] = top_orig_right_column[i]

      # Update right face by rotating array
      cube['R'] = list(zip(*cube['R'][::-1]))

def rotate_right_column_counter_clockwise(cube):
      # Store original right column of top face
      top_orig_right_column = [cube['T'][i][2] for i in range(3)]

      # Store original right column of front face
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]

      # Store original right column of bottom face
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]

      # Store original right column of back face
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update right column of top face with right column of back face
      for i in range(3):
            cube['T'][i][2] = back_orig_right_column[i]

      # Update right column of back face with right column of bottom face
      for i in range(3):
            cube['B'][i][2] = bottom_orig_right_column[i]

      # Update right column of bottom face with right column of front face
      for i in range(3):
            cube['D'][i][2] = front_orig_right_column[i]

      # Update right column of front face with right column of top face
      for i in range(3):
            cube['F'][i][2] = top_orig_right_column[i]

      # Update right face by rotating array
      cube['R'] = list(reversed(list(zip(*cube['R']))))

def rotate_left_column_clockwise(cube):
      # Store original left column of top face
      top_orig_left_column = [cube['T'][i][0] for i in range(3)]

      # Store original left column of front face
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]

      # Store original left column of bottom face
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]

      # Store original left column of back face
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update left column of top face with left column of back face
      for i in range(3):
            cube['T'][i][0] = back_orig_left_column[i]

      # Update left column of back face with left column of bottom face
      for i in range(3):
            cube['B'][i][0] = bottom_orig_left_column[i]

      # Update left column of bottom face with left column of front face
      for i in range(3):
            cube['D'][i][0] = front_orig_left_column[i]

      # Update left column of front face with left column of top face
      for i in range(3):
            cube['F'][i][0] = top_orig_left_column[i]

      # Update left face by rotating array
      cube['L'] = list(zip(*cube['L'][::-1]))

def rotate_left_column_counter_clockwise(cube):
      # Store original left column of top face
      top_orig_left_column = [cube['T'][i][0] for i in range(3)]

      # Store original left column of front face
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]

      # Store original left column of bottom face
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]

      # Store original left column of back face
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update left column of top face with left column of front face
      for i in range(3):
            cube['T'][i][0] = front_orig_left_column[i]

      # Update left column of front face with left column of bottom face
      for i in range(3):
            cube['F'][i][0] = bottom_orig_left_column[i]

      # Update left column of bottom face with left column of back face
      for i in range(3):
            cube['D'][i][0] = back_orig_left_column[i]

      # Update left column of back face with left column of top face
      for i in range(3):
            cube['B'][i][2] = top_orig_left_column[i]

      # Update left face by rotating array
      cube['L'] = list(reversed(list(zip(*cube['L']))))