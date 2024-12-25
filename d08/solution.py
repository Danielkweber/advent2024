from typing import Dict, List, Tuple
from dataclasses import dataclass
from operator import add, sub


@dataclass
class Input:
    nodes_by_freq: Dict[str, List[Tuple[int, int]]]
    height: int
    width: int


def read_input(test: bool) -> Input:
    file_name = "./test_input.txt" if test else "./input.txt"
    pos_by_freq = {}
    with open(file_name, "r") as f:
        for i, line in enumerate(f):
            for j, let in enumerate(line.strip()):
                if let == ".":
                    continue
                freq_array = pos_by_freq.get(let, [])
                freq_array.append((j, i))
                pos_by_freq[let] = freq_array
    return Input(pos_by_freq, height=i, width=j)


def check_within_square(
    val: Tuple[int, int], a: Tuple[int, int], b: Tuple[int, int]
) -> bool:
    if val[0] <= max(a[0], b[0]) and val[0] >= min(a[0], b[0]):
        return val[1] <= max(a[1], b[1]) and val[1] >= min(a[1], b[1])
    return False


def calc_antinodes_for_freq(nodes: List[Tuple[int, int]]):
    antis_for_freq = []
    for i in range(len(nodes)):
        primary = nodes[i]
        for j in range(i + 1, len(nodes)):
            potential_antis = []
            secondary = nodes[j]
            slope_y = secondary[1] - primary[1]
            slope_x = secondary[0] - primary[0]
            slope = (slope_x, slope_y)
            potential_antis.append(tuple(map(add, primary, slope)))
            potential_antis.append(tuple(map(sub, primary, slope)))
            potential_antis.append(tuple(map(add, secondary, slope)))
            potential_antis.append(tuple(map(sub, secondary, slope)))
            for anti in potential_antis:
                if not check_within_square(anti, primary, secondary):
                    antis_for_freq.append(anti)
    return antis_for_freq


def calc_antinodes_for_freq2(nodes: List[Tuple[int, int]]):
    antis_for_freq = []
    for i in range(len(nodes)):
        primary = nodes[i]
        for j in range(i + 1, len(nodes)):
            secondary = nodes[j]
            slope_y = secondary[1] - primary[1]
            slope_x = secondary[0] - primary[0]
            for i in range(50):
                slope = (i * slope_x, i * slope_y)
                antis_for_freq.append(tuple(map(add, primary, slope)))
                antis_for_freq.append(tuple(map(sub, primary, slope)))
    return antis_for_freq


def solve(part1: bool):
    antinodes = set()
    input = read_input(test=False)
    for val in input.nodes_by_freq.values():
        antis = calc_antinodes_for_freq(val) if part1 else calc_antinodes_for_freq2(val)
        for anti in antis:
            if check_within_square(anti, (0, 0), (input.width, input.height)):
                antinodes.add(anti)
    return len(antinodes)


if __name__ == "__main__":
    print(solve(part1=True))
