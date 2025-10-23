def make_goal(s):
    ts = s * s
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y * s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s * s:
            cur = 0
    return puzzle

def give_coordinate(puzzle, nb, size):
    for index in range(len(puzzle)):
        if puzzle[index] == nb:
            x = index // size
            y = index % size
            return (x, y)
    return None

def possible_moves(current_state, size):
    x0, y0 = give_coordinate(current_state, 0, size)

    move_pos = []
    if x0 > 0:
        new_state = current_state[:] # make a copy
        new_index = (x0 - 1)*size + y0
        new_state[x0*size + y0], new_state[new_index] = new_state[new_index], new_state[x0*size + y0]
        move_pos.append(new_state)
    if x0 < size - 1: 
        new_state = current_state[:]
        new_index = (x0 + 1)*size + y0
        new_state[x0*size + y0], new_state[new_index] = new_state[new_index], new_state[x0*size + y0]
        move_pos.append(new_state)
    if y0 > 0:
        new_state = current_state[:]
        new_index = (x0)*size + y0 - 1
        new_state[x0*size + y0], new_state[new_index] = new_state[new_index], new_state[x0*size + y0]
        move_pos.append(new_state)
    if y0 < size - 1: 
        new_state = current_state[:]
        new_index = (x0)*size + y0 + 1
        new_state[x0*size + y0], new_state[new_index] = new_state[new_index], new_state[x0*size + y0]
        move_pos.append(new_state)
    return move_pos