from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass
from copy import deepcopy
import heapq


class CellType(Enum):
    SPACE = 0
    WALL = 1
    START = 2
    GOAL = 3

    def __str__(self):
        if self.value == 0:
            return "."
        if self.value == 1:
            return "#"
        if self.value == 2:
            return "S"
        if self.value == 3:
            return "E"
        return "."

    def __repr__(self) -> str:
        if self.value == 0:
            return "."
        if self.value == 1:
            return "#"
        if self.value == 2:
            return "S"
        if self.value == 3:
            return "E"
        return "."


class Direction(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

    def __gt__(self, value: object, /) -> bool:
        return True


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


@dataclass
class Puzzle:
    maze: List[List[CellType]]
    goal: Coord
    start: Coord

    def print(self):
        print_copy = deepcopy(self.maze)
        print_copy[self.start.i][self.start.j] = CellType.START
        print_copy[self.goal.i][self.goal.j] = CellType.GOAL
        for line in print_copy:
            print("".join([str(let) for let in line]))


def calc_turns(dir: Direction, curr: Direction):
    diff = abs(dir.value - curr.value)
    return min(diff, 4 - diff)


def expand_node(puzzle: Puzzle, node: Tuple[int, Coord, Direction]):
    dist, curr_coord, dir = node
    nodes_to_add = []
    if (
        curr_coord.i + 1 < len(puzzle.maze)
        and puzzle.maze[curr_coord.i + 1][curr_coord.j] != CellType.WALL
    ):
        turns = calc_turns(dir=Direction.SOUTH, curr=dir)
        nodes_to_add.append(
            (
                dist + turns * 1000 + 1,
                Coord(curr_coord.i + 1, curr_coord.j),
                Direction.SOUTH,
            )
        )
    if (
        curr_coord.i - 1 >= 0
        and puzzle.maze[curr_coord.i - 1][curr_coord.j] != CellType.WALL
    ):
        turns = calc_turns(dir=Direction.NORTH, curr=dir)
        nodes_to_add.append(
            (
                dist + turns * 1000 + 1,
                Coord(curr_coord.i - 1, curr_coord.j),
                Direction.NORTH,
            )
        )
    if (
        curr_coord.j - 1 >= 0
        and puzzle.maze[curr_coord.i][curr_coord.j - 1] != CellType.WALL
    ):
        turns = calc_turns(dir=Direction.WEST, curr=dir)
        nodes_to_add.append(
            (
                dist + turns * 1000 + 1,
                Coord(curr_coord.i, curr_coord.j - 1),
                Direction.WEST,
            )
        )
    if (
        curr_coord.j + 1 < len(puzzle.maze[0])
        and puzzle.maze[curr_coord.i][curr_coord.j + 1] != CellType.WALL
    ):
        turns = calc_turns(dir=Direction.EAST, curr=dir)
        nodes_to_add.append(
            (
                dist + turns * 1000 + 1,
                Coord(curr_coord.i, curr_coord.j + 1),
                Direction.EAST,
            )
        )
    return nodes_to_add


def read_input() -> Puzzle:
    with open("./input.txt", "r") as f:
        maze = [
            [CellType.WALL if let == "#" else CellType.SPACE for let in line.strip()]
            for line in f
        ]
        height, width = len(maze), len(maze[0])
        goal = Coord(j=width - 2, i=1)
        start = Coord(j=1, i=height - 2)
        return Puzzle(maze=maze, goal=goal, start=start)


# Counts nodes for part 2
def recurse(glob_set, node, prev, dist):
    glob_set.add(node[0])
    if len(prev[node]) == 0:
        return len(glob_set)
    return max(
        [recurse(glob_set, child, prev, dist) for child in prev[node]] + [len(glob_set)]
    )


def count_trace(node, prev, dist):
    glob_set = set()
    return recurse(glob_set, node, prev, dist)


# Gonna do Dijkstra's for this
def solve():
    puzzle = read_input()
    heap = [(0, puzzle.start, Direction.EAST)]
    dist_map = {(puzzle.start, Direction.EAST): 0}
    prev = {(puzzle.start, Direction.EAST): []}
    while len(heap) > 0:
        curr = heapq.heappop(heap)
        for node in expand_node(puzzle=puzzle, node=curr):
            if (node[1], node[2]) in dist_map:
                if node[0] < dist_map[(node[1], node[2])]:
                    dist_map[(node[1], node[2])] = node[0]
                    prev[(node[1], node[2])] = [(curr[1], curr[2])]
                    heapq.heappush(heap, node)
                elif node[0] == dist_map[(node[1], node[2])]:
                    prev[(node[1], node[2])].append((curr[1], curr[2]))
            else:
                dist_map[(node[1], node[2])] = node[0]
                prev[(node[1], node[2])] = [(curr[1], curr[2])]
                heapq.heappush(heap, node)
    min_cost = min(
        [dist_map.get((puzzle.goal, Direction(i)), float("inf")) for i in range(4)]
    )
    print(f"Part 1 - Min Cost Path: {min_cost}")
    print(
        f"Part 2 - Nice Nodes: {count_trace((puzzle.goal, Direction.NORTH), prev, dist_map)}"
    )


if __name__ == "__main__":
    solve()
