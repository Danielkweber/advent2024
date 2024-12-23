from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


@dataclass
class Coord:
    i: int
    j: int

    def __eq__(self, value: object, /) -> bool:
        return (self.i, self.j) == value

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __gt__(self, value: object, /) -> bool:
        return True


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def read_input():
    grid = []
    with open("./input.txt", "r") as f:
        grid = [[let for let in line.strip()] for line in f]
    for i, row in enumerate(grid):
        for j, let in enumerate(row):
            if let == "^":
                return grid, Coord(i=i, j=j)
    raise Exception


# TODO: Generalize
def construct_memoized_grid_for_dir(grid: List[List[str]], dir: Direction):
    memo: List[List[Tuple[Coord | None, Set[Coord]] | None]] = [
        [None] * len(grid[0]) for _ in range(len(grid))
    ]
    height = len(grid)
    width = len(grid[0])
    match dir:
        case Direction.LEFT:
            for i in range(height):
                for j in range(width):
                    val = grid[i][j]
                    if val == "#":
                        memo[i][j] = (Coord(i, j + 1), set())
                    else:
                        if j == 0:
                            memo[i][j] = (None, set([Coord(i, j)]))
                            continue
                        prev_next, prev_set = memo[i][j - 1]
                        next_set = prev_set | set([Coord(i, j)])
                        memo[i][j] = (prev_next, next_set)
        case Direction.RIGHT:
            for i in range(height):
                for j in reversed(range(width)):
                    val = grid[i][j]
                    if val == "#":
                        memo[i][j] = (Coord(i, j - 1), set())
                    else:
                        if j == width - 1:
                            memo[i][j] = (None, set([Coord(i, j)]))
                            continue
                        prev_next, prev_set = memo[i][j + 1]
                        next_set = prev_set | set([Coord(i, j)])
                        memo[i][j] = (prev_next, next_set)
        # Love me some cache misses
        case Direction.UP:
            for j in range(width):
                for i in range(height):
                    val = grid[i][j]
                    if val == "#":
                        memo[i][j] = (Coord(i + 1, j), set())
                    else:
                        if i == 0:
                            memo[i][j] = (None, set([Coord(i, j)]))
                            continue
                        prev_next, prev_set = memo[i - 1][j]
                        next_set = prev_set | set([Coord(i, j)])
                        memo[i][j] = (prev_next, next_set)
        case Direction.DOWN:
            for j in range(width):
                for i in reversed(range(height)):
                    val = grid[i][j]
                    if val == "#":
                        memo[i][j] = (Coord(i - 1, j), set())
                    else:
                        if i == height - 1:
                            memo[i][j] = (None, set([Coord(i, j)]))
                            continue
                        prev_next, prev_set = memo[i + 1][j]
                        next_set = prev_set | set([Coord(i, j)])
                        memo[i][j] = (prev_next, next_set)

    return memo


def solve():
    grid, pos = read_input()
    dir = 0
    memos = []
    visit_set = set()
    for i in range(4):
        memos.append(construct_memoized_grid_for_dir(grid, Direction(i)))
    while pos:
        next, visits = memos[dir][pos.i][pos.j]
        pos = next
        visit_set |= visits
        dir = (dir + 1) % 4
    return len(visit_set)


if __name__ == "__main__":
    print(solve())
