from typing import List
import numpy as np
from numpy.typing import NDArray
from functools import reduce
import operator

HEIGHT = 103
WIDTH = 101
TEST_HEIGHT = 7
TEST_WIDTH = 11


def extract_nums(s: str):
    num_str = s.split("=")[1]
    pos_nums = num_str.split(",")
    nums = np.array([int(pos_nums[0]), int(pos_nums[1])])
    return nums


# p=56,68 v=1,-12
def read_input():
    robots = []
    with open("./input.txt", "r") as f:
        for line in f:
            pos_string, vel_string, *_ = line.split(" ")
            pos = extract_nums(pos_string)
            vel = extract_nums(vel_string)
            robots.append([pos, vel])
    return robots


def simulate_robot(robot: List[NDArray[np.int32]], steps: int, width: int, height: int):
    pos, vel = robot
    simulated_pos = pos + steps * vel
    simulated_pos[0] %= width
    simulated_pos[1] %= height
    return simulated_pos


def determine_quadrant(pos: NDArray[np.int32], width: int, height: int):
    mid_width = width // 2
    mid_height = height // 2
    # Wish I had a match statement here lol
    if pos[0] < mid_width and pos[1] < mid_height:
        return 1
    if pos[0] > mid_width and pos[1] < mid_height:
        return 2
    if pos[0] > mid_width and pos[1] > mid_height:
        return 3
    if pos[0] < mid_width and pos[1] > mid_height:
        return 4
    return 0


def part_one():
    robots = read_input()
    quadrant_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        simulated_pos = simulate_robot(robot, 100, WIDTH, HEIGHT)
        simulated_quadrant = determine_quadrant(simulated_pos, WIDTH, HEIGHT)
        if simulated_quadrant == 0:
            continue
        quadrant_counts[simulated_quadrant] += 1
    quadrant_prod = reduce(operator.mul, quadrant_counts.values(), 1)
    return quadrant_prod


def print_buffer(robot_pos: List[NDArray[np.int32]], width: int, height: int, buffer):
    position_counts = {}
    for pos in robot_pos:
        position_counts[(pos[0], pos[1])] = position_counts.get((pos[0], pos[1]), 0) + 1
    for j in range(height):
        for i in range(width):
            pos = (i, j)
            if pos in position_counts:
                print(position_counts[pos], end="", file=buffer)
            else:
                print(".", end="", file=buffer)
        print("", file=buffer)


def part_two():
    robots = read_input()
    with open("out.txt", "w") as f:
        for i in range(129, 10000, 101):
            simulated_robots = [
                simulate_robot(robot, i, WIDTH, HEIGHT) for robot in robots
            ]
            print(f"Iteration: {i}", file=f)
            print_buffer(simulated_robots, WIDTH, HEIGHT, f)
            print("\n", file=f)
        return


if __name__ == "__main__":
    pos = np.array([2, 4])
    vel = np.array([2, -3])
    part_two()
