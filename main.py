#!/usr/bin/env python

import sys
import argparse
import random
import time
from algo_manhatan import A_search_manhatan, A_search_manhatan_heap
from algo_linear_confilct import A_search_linear_confilct, A_search_linear_confilct_heap
from algo_patern_data import A_search_patern_data_heap
from interface import show_game
from interface_qt import show_game_qt
from utils import make_goal_snail, parse_input, parse_file, is_solvable_snail, calc_time
from puzzle import Puzzle

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

def parse_args():
    parser = argparse.ArgumentParser(description="N-Puzzle Solver")

    parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be > 3.")
    parser.add_argument("-s", "--solvable", action="store_true", help="Force generation of a solvable puzzle.")
    parser.add_argument("-u", "--unsolvable", action="store_true", help="Force generation of an unsolvable puzzle.")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of randomization iterations.")
    parser.add_argument("-m", "--method", choices=["manhattan", "pattern database", "linear conflict"], default="manhattan", help="Heuristic method to use.")
    parser.add_argument("-pf", "--puzzle_in_file", type=str, help="Load puzzle from file.")
    parser.add_argument("-p", "--puzzle", type=str, help="Provide puzzle directly: \"i i i i ...\"")
    parser.add_argument("-a", "--algorithm", choices=["astar", "uniform", "greedy"], default="astar", help="Search algorithm to use.")

    return parser.parse_args()

def resolve_solvability(args):
    if args.solvable and args.unsolvable:
        sys.exit("Can't be both solvable AND unsolvable, dummy!")

    if not args.solvable and not args.unsolvable:
        return random.choice([True, False])
    return args.solvable

def load_puzzle(args, solv):
    if args.puzzle and args.puzzle_in_file:
        sys.exit("Can't specify both a file and an input puzzle.")

    if args.puzzle:
        print("Custom puzzle")
        s, puzzle = parse_input(args.puzzle)
        if not is_solvable_snail(puzzle, s):
            solv = False
    elif args.puzzle_in_file:
        print("Loading puzzle from file")
        try:
            with open(args.puzzle_in_file, "r") as file:
                s, puzzle = parse_file(file.read())
        except Exception:
            sys.exit("Error while opening the file.")
        if not is_solvable_snail(puzzle, s):
            solv = False
    else:
        s = args.size
        puzzle = make_puzzle(s, solvable=solv, iterations=args.iterations)

    if not s:
        sys.exit("Invalid puzzle input.")
    if s > 5:
        print("A* cannot solve n-puzzles larger than 5x5")
        sys.exit(1)

    return s, puzzle, solv

def display_puzzle(puzzle, s, solv):
    w = len(str(s * s))
    for y in range(s):
        print(" ".join(str(puzzle[x + y * s]).rjust(w) for x in range(s)))
    print(f"# This puzzle is {'solvable' if solv else 'unsolvable'}")
    if not solv:
        sys.exit(1)

def run_algorithm(Npuzzle):
    start = time.time()
    chemin1, chemin2 = None, None

    methods = ["manhattan", "pattern database", "linear conflict"]

    if Npuzzle.method == methods[0]:
        t1, chemin1 = calc_time(A_search_manhatan, Npuzzle)
        t2, chemin2 = calc_time(A_search_manhatan_heap, Npuzzle)
        print(f"{Npuzzle.algo} - Normal manhatan {t1} Heap Manhatan {t2}")
        # t1, chemin1 = calc_time(A_search_manhatan, puzzle, s, goal, "greedy")
        # t2, chemin2 = calc_time(A_search_manhatan_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Normal manhatan {t1} Heap Manhatan {t2}")
        # t1, chemin1 = calc_time(A_search_manhatan, puzzle, s, goal, "uniform")
        # t2, chemin2 = calc_time(A_search_manhatan_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Normal manhatan {t1} Heap Manhatan {t2}")
    # Patern Data
    elif Npuzzle.method  == methods[1]:
        t1, chemin1 = calc_time(A_search_patern_data_heap, Npuzzle)
        print(f"{Npuzzle.algo} - Heap patern data {t1}")
        # t1, chemin1 = calc_time(A_search_patern_data_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Heap patern data {t1}")
        # t1, chemin1 = calc_time(A_search_patern_data_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Heap patern data {t1}")
    # linear conflict
    elif Npuzzle.method  == methods[2]:
        t1, chemin1 = calc_time(A_search_linear_confilct, Npuzzle)
        t2, chemin2 = calc_time(A_search_linear_confilct_heap, Npuzzle)
        print(f"{Npuzzle.algo} - Normal linear conflict {t1} Heap linear conflict {t2}")
        # t1, chemin1 = calc_time(A_search_linear_confilct, puzzle, s, goal, "greedy")
        # t2, chemin2 = calc_time(A_search_linear_confilct_heap, puzzle, s, goal, "greedy")
        # print(f"greedy - Normal linear conflict {t1} Heap linear conflict {t2}")
        # t1, chemin1 = calc_time(A_search_linear_confilct, puzzle, s, goal, "uniform")
        # t2, chemin2 = calc_time(A_search_linear_confilct_heap, puzzle, s, goal, "uniform")
        # print(f"uniform - Normal linear conflict {t1} Heap linear conflict {t2}")
    end = time.time()
    print("Total execution time:", round(end - start, 3), "seconds")
    return chemin1, chemin2

def main():
    args = parse_args()
    random.seed()

    if args.size < 3:
        sys.exit("Puzzle size must be at least 3.")

    solv = resolve_solvability(args)
    s, puzzle, solv = load_puzzle(args, solv)

    goal = make_goal_snail(s)

    Npuzzle = Puzzle(puzzle, s, goal, args.method, args.algorithm)
    Npuzzle.dysplay_puzzle()

    chemin1, chemin2 = run_algorithm(Npuzzle)

    if chemin1:
        for i in chemin1:
            print(i)
        if chemin2:
            print()
    if chemin2:
        for i in chemin2:
            print(i)

    # if chemin1:
    #     show_game(s, puzzle, chemin1)
    # elif chemin2:
    #     show_game(s, puzzle, chemin2)

    if chemin1:
        show_game_qt(s, chemin1)
    elif chemin2:
        show_game_qt(s, chemin2)


if __name__ == "__main__":
    main()