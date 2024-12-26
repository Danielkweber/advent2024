from dataclasses import dataclass
from typing import Set


@dataclass
class Cell:
    height: int
    nines_reachable: Set
    rating: int


def read_input(test: bool):
    file_name = "./test_input.txt" if test else "./input.txt"
    with open(file_name, "r") as f:
        grid = [
            [
                Cell(
                    height=int(let),
                    nines_reachable={(i, j)} if int(let) == 9 else set(),
                    rating=1 if int(let) == 9 else 0,
                )
                for j, let in enumerate(line.strip())
            ]
            for i, line in enumerate(f)
        ]
    return grid


def solve():
    grid = read_input(test=False)
    acc_part1 = 0
    acc_part2 = 0
    for k in reversed(range(9)):
        for i, line in enumerate(grid):
            for j, cell in enumerate(line):
                if cell.height == k:
                    if i + 1 < len(grid):
                        below = grid[i + 1][j]
                        if below.height == k + 1:
                            cell.nines_reachable |= below.nines_reachable
                            cell.rating += below.rating
                    if i >= 1:
                        above = grid[i - 1][j]
                        if above.height == k + 1:
                            cell.nines_reachable |= above.nines_reachable
                            cell.rating += above.rating
                    if j >= 1:
                        left = grid[i][j - 1]
                        if left.height == k + 1:
                            cell.nines_reachable |= left.nines_reachable
                            cell.rating += left.rating
                    if j + 1 < len(grid[0]):
                        right = grid[i][j + 1]
                        if right.height == k + 1:
                            cell.nines_reachable |= right.nines_reachable
                            cell.rating += right.rating
                    if k == 0:
                        acc_part1 += len(cell.nines_reachable)
                        acc_part2 += cell.rating
    return acc_part1, acc_part2


if __name__ == "__main__":
    p1, p2 = solve()
    print(f"Part 1 - {p1}")
    print(f"Part 2 - {p2}")
