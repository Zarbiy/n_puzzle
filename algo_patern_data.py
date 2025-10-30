import heapq
import time
import os
import pickle
import gc
from utils import possible_moves, check_memory

def extract_patern(size):
    patern = []
    if size == 3:
        patern = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8]
        ]
    elif size == 4:
        patern = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15]
        ]
        # patern = [
        #     [1, 2, 3, 4, 5],
        #     [6, 7, 8, 9, 10],
        #     [11, 12, 13, 14],
        #     [15]
        # ]
    elif size == 5:
        patern = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24]
        ]

        # patern = [
        #     [1, 2, 3, 4, 5],
        #     [6, 11, 16, 21],
        #     [7, 8, 9, 10],
        #     [12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24]
        # ]
    return patern

def erase_element(p, puzzle_goal):
    goal = puzzle_goal[:]
    for i in range(len(goal)):
        if goal[i] not in p and goal[i] != 0:
            goal[i] = -1
    return goal

def heuristic_pattern_database(puzzle, tab_patern, patern_data, h_save):
    t_puzzle = tuple(puzzle)
    if t_puzzle in h_save:
        return h_save[t_puzzle]

    h_total = 0
    for i, patern in enumerate(tab_patern):
        current_pattern = erase_element(patern, puzzle)
        t_current = tuple(current_pattern)
        if i < len(patern_data) and t_current in patern_data[i]:
            h_total += patern_data[i][t_current]
    h_save[t_puzzle] = h_total
    return h_total

def BFS(puzzle_goal, patern, size):
    all_posibilities = []
    for p in patern:
        start_patern = erase_element(p, puzzle_goal)
        open_tab = []
        open_tab.append(start_patern)
        cost = {tuple(start_patern): 0}
        close_tab = set()
        while len(open_tab) > 0:
            check_memory()
            chosen_tab = open_tab.pop(0)
            close_tab.add(tuple(chosen_tab))
            for pos in possible_moves(chosen_tab, size):
                t_succ = tuple(pos)
                if t_succ in close_tab:
                    continue

                moved_tile = [x for x, y in zip(chosen_tab, pos) if x != y and x != 0 and x != -1]
                if moved_tile:
                    c = cost[tuple(chosen_tab)] + 1
                else:
                    c = cost[tuple(chosen_tab)]

                if t_succ not in cost or c < cost[t_succ]:
                    cost[t_succ] = c
                    open_tab.append(pos)

        # print(len(cost))
        all_posibilities.append(cost)
    return tuple(all_posibilities)

def A_search_patern_data_heap(Npuzzle):
    if Npuzzle.puzzle_resolve():
        print("Already solved !")
        return None

    max_len_open = 0
    open_heap = []
    g_values = {tuple(Npuzzle.puzzle): 0}
    h_save = {}

    tab_patern = extract_patern(Npuzzle.size)
    patern_data = {}
    filename = f"patern/patern_data_s{Npuzzle.size}"
    if os.path.exists(filename):
        print("Load patern")
        with open(filename, "rb") as f:
            patern_data = pickle.load(f)
    else:
        print("Buildind patern ...")
        start = time.time()
        patern_data = BFS(Npuzzle.goal, tab_patern, Npuzzle.size)
        end = time.time()
        print("Time to build pattern:", round(end - start, 3), "seconds")
        with open(filename, "wb") as f:
            pickle.dump(patern_data, f)
        print("Pattern save")

    f_init = heuristic_pattern_database(Npuzzle.puzzle, tab_patern, patern_data, h_save)
    heapq.heappush(open_heap, (f_init, Npuzzle.puzzle))

    chemin = {}
    close_tab = set()

    while open_heap:
        check_memory()
        _, chosen_tab = heapq.heappop(open_heap)
        t_chosen = tuple(chosen_tab)

        if t_chosen in close_tab:
            continue
        close_tab.add(t_chosen)

        if t_chosen == tuple(Npuzzle.goal):
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
            if tuple(pos_puzzle) in close_tab:
                continue

            g_next = g_values[t_chosen] + 1
            if tuple(pos_puzzle) not in g_values or g_next < g_values[tuple(pos_puzzle)]:
                g_values[tuple(pos_puzzle)] = g_next
                chemin[tuple(pos_puzzle)] = chosen_tab
                h_next = heuristic_pattern_database(pos_puzzle, tab_patern, patern_data, h_save)
                if Npuzzle.algo == "astar":
                    f_next = g_next + h_next
                elif Npuzzle.algo == "uniform":
                    f_next = g_next
                elif Npuzzle.algo == "greedy":
                    f_next = h_next
                heapq.heappush(open_heap, (f_next, pos_puzzle))
                if len(open_heap) > max_len_open:
                        max_len_open = len(open_heap)
        # if len(close_tab) % 5000 == 0:
        #     gc.collect()
    return None