class Puzzle():
    def __init__(self, puzzle, size, goal, method, algo):
        self.puzzle = puzzle
        self.size = size
        self.goal = goal
        self.method = method
        self.algo = algo

    def dysplay_puzzle(self):
        w = len(str(self.size * self.size))
        for y in range(self.size):
            print(" ".join(str(self.puzzle[x + y * self.size]).rjust(w) for x in range(self.size)))

    def puzzle_resolve(self):
        if self.puzzle == self.goal:
            return True
        return False