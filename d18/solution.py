from dataclasses import dataclass
import heapq
from typing import List, Set, Tuple


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


def read_input():
    walls = []
    with open("./input.txt", "r") as f:
        for line in f:
            xy = [int(num.strip()) for num in line.split(",")]
            walls.append(Coord(i=xy[1], j=xy[0]))
    return walls


def expand_node(curr: Tuple[int, Coord], walls: Set[Coord], width: int, height: int):
    nodes_to_add = []
    dist, loc = curr
    if loc.i + 1 < height and Coord(i=loc.i + 1, j=loc.j) not in walls:
        nodes_to_add.append((dist + 1, Coord(i=loc.i + 1, j=loc.j)))

    if loc.i > 0 and Coord(i=loc.i - 1, j=loc.j) not in walls:
        nodes_to_add.append((dist + 1, Coord(i=loc.i - 1, j=loc.j)))

    if loc.j > 0 and Coord(i=loc.i, j=loc.j - 1) not in walls:
        nodes_to_add.append((dist + 1, Coord(i=loc.i, j=loc.j - 1)))

    if loc.j + 1 < width and Coord(i=loc.i, j=loc.j + 1) not in walls:
        nodes_to_add.append((dist + 1, Coord(i=loc.i, j=loc.j + 1)))
    return nodes_to_add


def find_shortest_path(walls: Set[Coord]):
    start = Coord(i=0, j=0)
    end = Coord(i=70, j=70)
    height = 71
    width = 71
    heap = [(0, start)]
    dist_map = {start: 0}
    while len(heap) > 0:
        curr = heapq.heappop(heap)
        for node in expand_node(curr=curr, walls=walls, width=width, height=height):
            if node[1] in dist_map:
                if node[0] < dist_map[node[1]]:
                    dist_map[node[1]] = node[0]
                    heapq.heappush(heap, node)
            else:
                dist_map[node[1]] = node[0]
                heapq.heappush(heap, node)
    return dist_map.get(end, -1)


def find_minimal_wall_set_index(walls: List[Coord]):
    low = 0
    high = len(walls)
    while low < high:
        mid = (low + high) // 2
        shortest = find_shortest_path(set(walls[:mid]))

        if shortest == -1:  # Unreachable
            high = mid - 1
        else:  # Reachable
            low = mid + 1
    return ((low + high) // 2) - 1


def solve():
    walls = read_input()
    i = find_minimal_wall_set_index(walls)
    print(f"Part 1 - {find_shortest_path(set(walls[:1024]))}")
    print(f"Part 2 - {walls[i]}")


if __name__ == "__main__":
    solve()
