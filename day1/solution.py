from typing import List, Tuple
import re


def read_input() -> Tuple[List[int], List[int]]:
    left = []
    right = []
    with open("./input.txt", "r") as f:
        for line in f:
            vals = re.split("\s+", line)
            left.append(int(vals[0]))
            right.append(int(vals[1]))
    return (left, right)


def solution() -> int:
    left, right = read_input()
    left.sort()
    right.sort()
    dist = 0
    for i in range(len(right)):
        dist += abs(left[i] - right[i])

    return dist


def part_two() -> int:
    left, right = read_input()
    right_counts = {}
    for num in right:
        if num in right_counts:
            right_counts[num] += 1
        else:
            right_counts[num] = 1

    sim_score = 0
    for num in left:
        if num in right_counts:
            sim_score += num * right_counts[num]
    return sim_score


if __name__ == "__main__":
    print(part_two())
