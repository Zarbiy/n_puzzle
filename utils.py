import math

def make_goal_snail(s):
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
        new_state = current_state[:]
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

def parse_input(input):
    values = input.split()
    size = math.sqrt(len(values))
    if not size.is_integer() or int(size) < 3:
        print("Wrong number of input")
        return False, False
    for i in range(len(values)):
        if not values[i].isdigit():
            return False, False
        values[i] = int(values[i])
    cpy_value = values[:]
    values.sort()
    find_zero = False, False
    for i in range(len(values) - 1):
        if values[i] == 0:
            find_zero = True
        if values[i] + 1 != values[i + 1]:
            return False, False
    if not find_zero:
        print("Missing zero")
        return False, False

    return int(size), cpy_value

def count_permutation(start, goal):
    start_no_zero = [x for x in start if x != 0]
    goal_no_zero = [x for x in goal if x != 0]

    goal_index = {value: idx for idx, value in enumerate(goal_no_zero)}

    perm = [goal_index[val] for val in start_no_zero]
    
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inv += 1
    return inv % 2

def is_solvable_snail(puzzle, size):
    goal = make_goal_snail(size)
    
    p_parity = count_permutation(puzzle, goal)
    g_parity = count_permutation(goal, goal)
    
    return p_parity == g_parity