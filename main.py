#!/usr/bin/env python

import sys
import argparse
import random
import time
from algo_manhatan import A_search_manhatan, A_search_manhatan_heap
from algo_linear_confilct import A_search_linear_confilct, A_search_linear_confilct_heap
from algo_patern_data import A_search_patern_data_heap
from interface import show_game
from utils import make_goal_snail, parse_input, parse_file, is_solvable_snail, calc_time

def make_puzzle(s, solvable, iterations):
    def swap_empty(p):
        idx = p.index(0)
        poss = []
        if idx % s > 0:
            poss.append(idx - 1)
        if idx % s < s - 1:
            poss.append(idx + 1)
        if idx // s > 0:
            poss.append(idx - s)
        if idx // s < s - 1:
            poss.append(idx + s)
        swi = random.choice(poss)
        p[idx] = p[swi]
        p[swi] = 0

    p = make_goal_snail(s)
    for i in range(iterations):
        swap_empty(p)

    if not solvable:
        if p[0] == 0 or p[1] == 0:
            p[-1], p[-2] = p[-2], p[-1]
        else:
            p[0], p[1] = p[1], p[0]

    return p

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be >3.")
    parser.add_argument("-s", "--solvable", action="store_true", default=False, help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")
    parser.add_argument("-m", "--method", type=str, default="Manhattan", help="Heuristic method to use (Manhattan - Pattern Database - Linear Conflict)")
    parser.add_argument("-pf", "--puzzle_in_file", type=str, default=False, help="Import a file (size of the puzzle then the puzzle)")
    parser.add_argument("-p", "--puzzle", type=str, default=False, help="Enter the puzzle, format: \"i i i i ...\"")
    parser.add_argument("-a", "--algorithm", type=str, choices=["astar", "uniform", "greedy"], default="astar", help="Choose search algorithm: 'astar' (default), 'uniform' (uniform-cost), or 'greedy'.")

    args = parser.parse_args()

    random.seed()

    if args.solvable and args.unsolvable:
        print("Can't be both solvable AND unsolvable, dummy!")
        sys.exit(1)

    if args.size < 3:
        print("Can't generate a puzzle with size lower than 2. It says so in the help. Dummy.")
        sys.exit(1)

    methods = ["manhattan", "pattern database", "linear conflict"]
    method_choice = args.method.lower()
    if method_choice not in methods:
        print("Not a valid method.\nValid method: Manhattan - Pattern Database - Linear Conflict")
        sys.exit(1)

    if not args.solvable and not args.unsolvable:
        solv = random.choice([True, False])
    elif args.solvable:
        solv = True
    elif args.unsolvable:
        solv = False

    if args.puzzle and args.puzzle_in_file:
        print("You have to choose can't make both puzzle (file and input)")
        sys.exit(1)

    if args.puzzle:
        print("Custom puzzle")
        s, puzzle = parse_input(args.puzzle)
        if not s:
            print("Error in puzzle input !")
            sys.exit(1)
        if not is_solvable_snail(puzzle, s):
            solv = False
    elif args.puzzle_in_file:
        print("Custom puzzle in file")
        try:
            with open(args.puzzle_in_file, "r") as file:
                s, puzzle = parse_file(file.read())
                if not s:
                    print("Error in puzzle input !")
                    sys.exit(1)
                if not is_solvable_snail(puzzle, s):
                    solv = False
        except Exception as e:
            print("Error while opening the file !")
            sys.exit(1)
    else:
        s = args.size
        puzzle = make_puzzle(s, solvable=solv, iterations=args.iterations)

    w = len(str(s * s))
    for y in range(s):
        print(" ".join(str(puzzle[x + y * s]).rjust(w) for x in range(s)))

    print("# This puzzle is %s" % ("solvable" if solv else "unsolvable"))
    if not solv:
        sys.exit(1)

    algo = args.algorithm
    chemin1 = False
    chemin2 = False
    goal = make_goal_snail(s)
    start = time.time()
    # Manhatan
    if method_choice == methods[0]:
        t1, chemin1 = calc_time(A_search_manhatan, puzzle, s, goal, algo)
        t2, chemin2 = calc_time(A_search_manhatan_heap, puzzle, s, goal, algo)
        print(f"{algo} - Normal manhatan {t1} Heap Manhatan {t2}")
        # t1, chemin1 = calc_time(A_search_manhatan, puzzle, s, goal, "greedy")
        # t2, chemin2 = calc_time(A_search_manhatan_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Normal manhatan {t1} Heap Manhatan {t2}")
        # t1, chemin1 = calc_time(A_search_manhatan, puzzle, s, goal, "uniform")
        # t2, chemin2 = calc_time(A_search_manhatan_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Normal manhatan {t1} Heap Manhatan {t2}")
    # Patern Data
    elif method_choice == methods[1]:
        t1, chemin1 = calc_time(A_search_patern_data_heap, puzzle, s, goal, algo)
        print(f"{algo} - Heap patern data {t1}")
        # t1, chemin1 = calc_time(A_search_patern_data_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Heap patern data {t1}")
        # t1, chemin1 = calc_time(A_search_patern_data_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Heap patern data {t1}")
    # linear conflict
    elif method_choice == methods[2]:
        t1, chemin1 = calc_time(A_search_linear_confilct, puzzle, s, goal, algo)
        t2, chemin2 = calc_time(A_search_linear_confilct_heap, puzzle, s, goal, algo)
        print(f"{algo} - Normal linear conflict {t1} Heap linear conflict {t2}")
        # t1, chemin1 = calc_time(A_search_linear_confilct, puzzle, s, goal, "greedy")
        # t2, chemin2 = calc_time(A_search_linear_confilct_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Normal linear conflict {t1} Heap linear conflict {t2}")
        # t1, chemin1 = calc_time(A_search_linear_confilct, puzzle, s, goal, "uniform")
        # t2, chemin2 = calc_time(A_search_linear_confilct_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Normal linear conflict {t1} Heap linear conflict {t2}")
    end = time.time()

    print("Total execution time :", round(end - start, 3), "secondes")

    if chemin1:
        for i in chemin1:
            print(i)
        if chemin2:
            print()
    if chemin2:
        for i in chemin2:
            print(i)
    if chemin1:
        show_game(s, puzzle, chemin1)
    elif chemin2:
        show_game(s, puzzle, chemin2)

