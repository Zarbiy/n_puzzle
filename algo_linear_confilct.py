import sys
import heapq
from utils import give_coordinate, possible_moves, check_memory

def heuristic_manhattan(puzzle, puzzle_goal, size):
    def dist_manhattan(puzzle, puzzle_goal, nb, size):
        x1, y1 = give_coordinate(puzzle, nb, size)
        x2, y2 = give_coordinate(puzzle_goal, nb, size)
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist

    return sum(dist_manhattan(puzzle, puzzle_goal, nb, size) for nb in range(1, size * size))

def nb_conflict(puzzle, puzzle_goal, size):
    nb = 0
    posi = {}
    for i in puzzle_goal:
        posi[i] = give_coordinate(puzzle_goal, i, size)

    for row in range(size):
        tiles_in_row = [puzzle[row * size + col] for col in range(size) if puzzle[row * size + col] != 0]
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                t1 = tiles_in_row[i]
                t2 = tiles_in_row[j]
                if posi[t1][0] == row and posi[t2][0] == row:
                    if posi[t1][1] > posi[t2][1]:
                        nb += 1

    for col in range(size):
        tiles_in_col = [puzzle[row * size + col] for row in range(size) if puzzle[row * size + col] != 0]
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                t1 = tiles_in_col[i]
                t2 = tiles_in_col[j]
                if posi[t1][1] == col and posi[t2][1] == col:
                    if posi[t1][0] > posi[t2][0]:
                        nb += 1
    return nb

def heuristic_linear_conflict(puzzle, puzzle_goal, size):
    return heuristic_manhattan(puzzle, puzzle_goal, size) + 2 * (nb_conflict(puzzle, puzzle_goal, size))

def A_search_linear_confilct(Npuzzle):
    if Npuzzle.size > 3:
        print("Method too slow for this size ! Pass")
        return None

    if Npuzzle.puzzle_resolve():
        print("Already solved !")
        return None

    max_len_open = 0
    open_tab = []
    open_tab.append(Npuzzle.puzzle)
    close_tab = set()
    g_values = {tuple(Npuzzle.puzzle): 0}

    chemin = {}

    while len(open_tab) > 0:
        check_memory()
        f_min = sys.maxsize
        for tab in open_tab:
            if Npuzzle.algo == "astar":
                f = g_values[tuple(tab)] + heuristic_linear_conflict(tab, Npuzzle.goal, Npuzzle.size)
            elif Npuzzle.algo == "uniform":
                f = g_values[tuple(tab)]
            elif Npuzzle.algo == "greedy":
                f = heuristic_linear_conflict(tab, Npuzzle.goal, Npuzzle.size)
            if f < f_min:
                f_min = f
                chosen_tab = tab
        if chosen_tab == Npuzzle.goal:
            check_memory(True)
            print("Max len open_tap:", max_len_open)
            print("Evaluate state:", len(close_tab))
            path = [chosen_tab]
            while tuple(path[-1]) in chemin:
                path.append(chemin[tuple(path[-1])])
            path.reverse()
            print("Nb move:", len(path))
            return path

        open_tab.remove(chosen_tab)
        close_tab.add(tuple(chosen_tab))

        for pos_puzzle in possible_moves(chosen_tab, Npuzzle.size):
            if tuple(pos_puzzle) not in close_tab:
                if tuple(pos_puzzle) not in g_values:
                    g_values[tuple(pos_puzzle)] = g_values[tuple(chosen_tab)] + 1
                    chemin[tuple(pos_puzzle)] = chosen_tab
                    open_tab.append(pos_puzzle)
                    if len(open_tab) > max_len_open:
                        max_len_open = len(open_tab)
                else:
                    if g_values[tuple(chosen_tab)] + 1 < g_values[tuple(pos_puzzle)]:
                        g_values[tuple(pos_puzzle)] = g_values[tuple(chosen_tab)] + 1
                        chemin[tuple(pos_puzzle)] = chosen_tab
    return None

def A_search_linear_confilct_heap(Npuzzle):
    if Npuzzle.puzzle_resolve():
        print("Already solved !")
        return None

    max_len_open = 0
    open_heap = []
    g_values = {tuple(Npuzzle.puzzle): 0}
    chemin = {}
    close_tab = set()

    f_start = heuristic_linear_conflict(Npuzzle.puzzle, Npuzzle.goal, Npuzzle.size)
    heapq.heappush(open_heap, (f_start, Npuzzle.puzzle))

    while open_heap:
        check_memory()
        _, chosen_tab = heapq.heappop(open_heap)
        t_chosen = tuple(chosen_tab)

        if t_chosen in close_tab:
            continue
        close_tab.add(t_chosen)

        if chosen_tab == Npuzzle.goal:
            check_memory(True)
            print("Max len open_heap:", max_len_open)
            print("Evaluate state:", len(close_tab))
            path = [chosen_tab]
            while tuple(path[-1]) in chemin:
                path.append(chemin[tuple(path[-1])])
            path.reverse()
            print("Nb move:", len(path))
            return path

        for pos_puzzle in possible_moves(chosen_tab, Npuzzle.size):
            if tuple(pos_puzzle) not in close_tab:
                g_next = g_values[t_chosen] + 1
                if tuple(pos_puzzle) not in g_values or g_next < g_values[tuple(pos_puzzle)]:
                    g_values[tuple(pos_puzzle)] = g_next
                    chemin[tuple(pos_puzzle)] = chosen_tab
                    if Npuzzle.algo == "astar":
                        f_next = g_next + heuristic_linear_conflict(pos_puzzle, Npuzzle.goal, Npuzzle.size)
                    elif Npuzzle.algo == "uniform":
                        f_next = g_next
                    elif Npuzzle.algo == "greedy":
                        f_next = heuristic_linear_conflict(pos_puzzle, Npuzzle.goal, Npuzzle.size)
                    heapq.heappush(open_heap, (f_next, pos_puzzle))
                    if len(open_heap) > max_len_open:
                        max_len_open = len(open_heap)

    return None