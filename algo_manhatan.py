import sys
import heapq
from utils import make_goal, give_coordinate, possible_moves

def heuristic_manhattan(puzzle, puzzle_goal, size):
    def dist_manhattan(puzzle, puzzle_goal, nb, size):
        x1, y1 = give_coordinate(puzzle, nb, size)
        x2, y2 = give_coordinate(puzzle_goal, nb, size)
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist

    return sum(dist_manhattan(puzzle, puzzle_goal, nb, size) for nb in range(1, size * size))

def A_search_manhatan(puzzle, size):
    puzzle_goal = make_goal(size)
    if puzzle == puzzle_goal:
        print("Already solved !")
        return 0

    max_len_open = 0
    open_tab = []
    open_tab.append(puzzle)
    close_tab = set()
    g_values = {tuple(puzzle): 0}

    chemin = {}

    while len(open_tab) > 0:
        f_min = sys.maxsize
        for tab in open_tab:
            # f = g + h
            f = g_values[tuple(tab)] + heuristic_manhattan(tab, puzzle_goal, size)
            if f < f_min:
                f_min = f
                chosen_tab = tab

        if chosen_tab == puzzle_goal:
            print("Max len open_tab:", max_len_open)
            print("Evaluate state:", len(close_tab))
            path = [chosen_tab]
            while tuple(path[-1]) in chemin:
                path.append(chemin[tuple(path[-1])])
            path.reverse()
            return path

        open_tab.remove(chosen_tab)
        close_tab.add(tuple(chosen_tab))

        for pos_puzzle in possible_moves(chosen_tab, size):
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

def A_search_manhatan_heap(puzzle, size):
    puzzle_goal = make_goal(size)
    if puzzle == puzzle_goal:
        print("Already solved !")
        return None

    max_len_open = 0
    open_heap = []
    g_values = {tuple(puzzle): 0}
    chemin = {}
    close_tab = set()

    f_start = heuristic_manhattan(puzzle, puzzle_goal, size)
    heapq.heappush(open_heap, (f_start, puzzle))

    while open_heap:
        chosen_tab = heapq.heappop(open_heap)[1]
        t_chosen = tuple(chosen_tab)

        if t_chosen in close_tab:
            continue
        close_tab.add(t_chosen)

        if chosen_tab == puzzle_goal:
            print("Max len open_heap:", max_len_open)
            print("Evaluate state:", len(close_tab))
            path = [chosen_tab]
            while tuple(path[-1]) in chemin:
                path.append(chemin[tuple(path[-1])])
            path.reverse()
            return path

        for pos_puzzle in possible_moves(chosen_tab, size):
            if tuple(pos_puzzle) not in close_tab:
                g_next = g_values[t_chosen] + 1
                if tuple(pos_puzzle) not in g_values or g_next < g_values[tuple(pos_puzzle)]:
                    g_values[tuple(pos_puzzle)] = g_next
                    chemin[tuple(pos_puzzle)] = chosen_tab
                    f_next = g_next + heuristic_manhattan(pos_puzzle, puzzle_goal, size)
                    heapq.heappush(open_heap, (f_next, pos_puzzle))
                    if len(open_heap) > max_len_open:
                        max_len_open = len(open_heap)

    return None