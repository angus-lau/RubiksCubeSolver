import old.rubiks_cube_class as rc

def rotate_face_clockwise(face, cube):
      if face not in ('B', 'D'):
            #clockwise
            cube[face] = [list(row) for row in zip(*cube[face][::-1])]
            update_adjacent_faces(face, cube)
      else:
            #counterclockwise
            cube[face] = [list(row) for row in reversed(list(zip(*cube[face])))]
            update_adjacent_faces(face, cube)

def rotate_face_counter_clockwise(face, cube):
      if face not in ('B', 'D'):
            cube[face] = [list(row) for row in reversed(list(zip(*cube[face])))]
            update_adjacent_faces_counterclockwise(face, cube)
      else:
            cube[face] = [list(row) for row in zip(*cube[face][::-1])]
            update_adjacent_faces_counterclockwise(face, cube)

def update_adjacent_faces(face, cube):
      if face == 'F':
            adjacent_front_clockwise(cube)
      elif face == 'B':
            adjacent_back_clockwise(cube)
      elif face == 'U':
            adjacent_top_clockwise(cube)
      elif face == 'D':
            adjacent_bottom_clockwise(cube)
      elif face == 'R':
            adjacent_right_column_clockwise(cube)
      elif face == 'L':
            adjacent_left_column_clockwise(cube)

def update_adjacent_faces_counterclockwise(face, cube):
      if face == 'F':
            adjacent_front_counter_clockwise(cube)
      elif face == 'B':
            adjacent_back_counter_clockwise(cube)
      elif face == 'U':
            adjacent_top_counter_clockwise(cube)
      elif face == 'D':
            adjacent_bottom_counter_clockwise(cube)
      elif face == 'R':
            adjacent_right_column_counter_clockwise(cube)
      elif face == 'L':
            adjacent_left_column_counter_clockwise(cube)
    
def adjacent_front_clockwise(cube):
      top_row = cube['U'][2]
      right_col = [cube['R'][i][0] for i in range(3)]
      bottom_row = cube['D'][0]
      left_col = [cube['L'][i][2] for i in range(3)]

      # Perform clockwise rotation of adjacent edges
      cube['U'][2] = left_col[::-1]
      for i in range(3):
            cube['R'][i][0] = top_row[i]
      cube['D'][0] = right_col[::-1]
      for i in range(3):
            cube['L'][i][2] = bottom_row[i]

def adjacent_front_counter_clockwise(cube):
      top_row = cube['U'][2]
      right_col = [cube['R'][i][0] for i in range(3)]
      bottom_row = cube['D'][0]
      left_col = [cube['L'][i][2] for i in range(3)]

      # Perform counterclockwise rotation of adjacent edges
      cube['U'][2] = right_col
      for i in range(3):
            cube['R'][i][0] = bottom_row[::-1][i]
      cube['D'][0] = left_col
      for i in range(3):
           cube['L'][i][2] = top_row[::-1][i]

def adjacent_back_clockwise(cube):
      top_row = cube['U'][0]
      left_col = [cube['L'][i][0] for i in range(3)]
      bottom_row = cube['D'][2]
      right_col = [cube['R'][i][2] for i in range(3)]

      # Perform clockwise rotation of adjacent edges
      cube['U'][0] = left_col[::-1]
      for i in range(3):
            cube['L'][i][0] = bottom_row[i]
      cube['D'][2] = right_col
      for i in range(3):
            cube['R'][i][2] = top_row[i]

def adjacent_back_counter_clockwise(cube):
      top_row = cube['U'][0]
      left_col = [cube['L'][i][0] for i in range(3)]
      bottom_row = cube['D'][2]
      right_col = [cube['R'][i][2] for i in range(3)]

      # Perform counterclockwise rotation of adjacent edges
      cube['U'][0] = right_col
      for i in range(3):
           cube['L'][i][0] = top_row[2-i]
      cube['D'][2] = left_col
      for i in range(3):
           cube['R'][i][2] = bottom_row[::-1][i]

def adjacent_bottom_counter_clockwise(cube):
      front_bottom_row = cube['F'][2]
      right_bottom_row = cube['R'][2]
      back_bottom_row = cube['B'][2]
      left_bottom_row = cube['L'][2]

      cube['F'][2] = left_bottom_row
      cube['R'][2] = front_bottom_row
      cube['B'][2] = right_bottom_row
      cube['L'][2] = back_bottom_row

def adjacent_top_clockwise(cube):
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

def adjacent_top_counter_clockwise(cube):
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

def adjacent_bottom_clockwise(cube):
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

def adjacent_right_column_clockwise(cube):
      # Store original values
      top_orig_right_column = [cube['U'][i][2] for i in range(3)]
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update values
      for i in range(3):
            cube['U'][i][2] = front_orig_right_column[i]
            cube['F'][i][2] = bottom_orig_right_column[i]
            cube['D'][i][2] = back_orig_right_column[2-i]
            cube['B'][i][0] = top_orig_right_column[2-i]

def adjacent_right_column_counter_clockwise(cube):
      # Store original values
      top_orig_right_column = [cube['U'][i][2] for i in range(3)]
      front_orig_right_column = [cube['F'][i][2] for i in range(3)]
      bottom_orig_right_column = [cube['D'][i][2] for i in range(3)]
      back_orig_right_column = [cube['B'][i][0] for i in range(3)]

      # Update right column of top face with right column of back face
      for i in range(3):
            cube['U'][i][2] = back_orig_right_column[2-i]
            cube['F'][i][2] = top_orig_right_column[i]
            cube['B'][i][0] = bottom_orig_right_column[2-i]
            cube['D'][i][2] = front_orig_right_column[i]

def adjacent_left_column_clockwise(cube):
      # Store original values
      top_orig_left_column = [cube['U'][i][0] for i in range(3)]
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update values
      for i in range(3):
            cube['U'][i][0] = back_orig_left_column[2 - i]
            cube['F'][i][0] = top_orig_left_column[i]
            cube['D'][i][0] = front_orig_left_column[i]
            cube['B'][i][2] = bottom_orig_left_column[2 - i]

def adjacent_left_column_counter_clockwise(cube):
      # Store original values
      top_orig_left_column = [cube['U'][i][0] for i in range(3)]
      front_orig_left_column = [cube['F'][i][0] for i in range(3)]
      bottom_orig_left_column = [cube['D'][i][0] for i in range(3)]
      back_orig_left_column = [cube['B'][i][2] for i in range(3)]

      # Update values
      for i in range(3):
            cube['U'][i][0] = front_orig_left_column[i]            
            cube['F'][i][0] = bottom_orig_left_column[i]           
            cube['D'][i][0] = back_orig_left_column[2 - i]         
            cube['B'][i][2] = top_orig_left_column[2 - i]          