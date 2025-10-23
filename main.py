#!/usr/bin/env python

import sys
import argparse
import random
import time
from algo_manhatan import A_search_manhatan, A_search_manhatan_heap
from algo_linear_confilct import A_search_linear_confilct, A_search_linear_confilct_heap
from algo_patern_data import A_search_patern_data_heap
from interface import show_game
from utils import make_goal_snail

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
    # parser.add_argument("-g", "--goal", type=str, default="Snail", help="Goal to reach a the end (Snail - Row-major - Inverse Row-major)")

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

    s = args.size

    puzzle = make_puzzle(s, solvable=solv, iterations=args.iterations)

    w = len(str(s * s))
    print("# This puzzle is %s" % ("solvable" if solv else "unsolvable"))
    for y in range(s):
        print(" ".join(str(puzzle[x + y * s]).rjust(w) for x in range(s)))

    print(puzzle)

    chemin = None
    chemin2 = None
    goal = make_goal_snail(s)
    start = time.time()
    if method_choice == methods[0]:
        s1 = time.time()
        chemin = A_search_manhatan(puzzle, s, goal)
        e1 = time.time()
        s2 = time.time()
        chemin2 = A_search_manhatan_heap(puzzle, s, goal)
        e2 = time.time()
        print(f"Normal manhatan {round(e1 - s1, 3)} Heap Manhatan {round(e2 - s2, 3)}")
    elif method_choice == methods[1]:
        chemin = A_search_patern_data_heap(puzzle, s, goal)
    elif method_choice == methods[2]:
        s1 = time.time()
        chemin = A_search_linear_confilct(puzzle, s, goal)
        e1 = time.time()
        s2 = time.time()
        chemin2 = A_search_linear_confilct_heap(puzzle, s, goal)
        e2 = time.time()
        print(f"Normal linear conflict {round(e1 - s1, 3)} Heap linear conflict {round(e2 - s2, 3)}")
    end = time.time()

    print("Total execution time :", round(end - start, 3), "secondes")

    if chemin != None:
        for i in chemin:
            print(i)
        if chemin2 != None:
            print()
            for i in chemin2:
                print(i)

    show_game(s, puzzle, chemin)
