import numpy as np


def extract_step(s: str):
    xy_string = s.split(",")
    x_step = int(xy_string[0].split("+")[1])
    y_step = int(xy_string[1].split("+")[1])
    return np.array([x_step, y_step], dtype=int)


def extract_goal(s: str):
    xy_string = s.split(",")
    x_step = int(xy_string[0].split("=")[1])
    y_step = int(xy_string[1].split("=")[1])
    return np.array([x_step, y_step], dtype=int)


def read_input():
    cases = []
    with open("./input.txt", "r") as f:
        unparsed_cases = f.read().split("\n\n")
        for case in unparsed_cases:
            stmts = case.split("\n")
            a_step = extract_step(stmts[0])
            b_step = extract_step(stmts[1])
            goal = extract_goal(stmts[2])
            cases.append((a_step, b_step, goal))
    return cases


# O (n log n) where n is the value of the goal
def solve_system(a_step, b_step, goal, cost_a: int, cost_b: int):
    MAX_COST = cost_a * cost_b * 200
    best_cost = MAX_COST
    max_presses = goal // a_step
    for num_a in range(int(np.max(max_presses))):
        if num_a % 1000000 == 0:
            pass
        max_b_presses = goal // b_step
        num_b = binary_search(
            start=a_step * num_a,
            goal=goal,
            step=b_step,
            max_count=int(np.max(max_b_presses)),
        )
        if num_b != -1:
            cost = num_a * cost_a + num_b * cost_b
            best_cost = min(cost, best_cost)

    return best_cost if best_cost != MAX_COST else 0


# It's funny that I thought I was so clever with this
# binaray search when in the true solution is way simpler
# and more elegant
def binary_search(start, goal, step, max_count: int):
    # start: np.array
    # goal: np.array
    # step: np.array
    small = 0
    large = max_count
    # print("MAXB:")
    # print(max_count)
    while small <= large:
        mid = (small + large) // 2
        curr = start + mid * step
        if np.all(np.equal(curr, goal)):
            return mid

        if np.all(np.greater(goal, curr)):
            small = mid + 1
        elif np.all(np.less(goal, curr)):
            large = mid - 1
        else:
            return -1
    return -1


def part_one():
    running_cost = 0
    cases = read_input()
    for case in cases:
        running_cost += solve_system(
            a_step=case[0], b_step=case[1], goal=case[2], cost_a=3, cost_b=1
        )
    return running_cost


def solve_system_linalg(a_step, b_step, goal, cost_a: int, cost_b: int):
    mat = np.array([a_step, b_step]).transpose()
    inv = np.linalg.inv(mat)
    step_counts = inv @ goal[:, np.newaxis]
    distance_from_int = np.abs(step_counts - np.round(step_counts))
    if np.all(distance_from_int < 0.001):
        squeezed = np.squeeze(step_counts, 1)
        return int(cost_a * np.round(squeezed[0]) + cost_b * np.round(squeezed[1]))
    return 0


def part_two():
    running_cost = 0
    cases = read_input()
    for case in cases:
        goal = case[2] + np.ones(2, dtype=int) * 10000000000000
        running_cost += solve_system_linalg(
            a_step=case[0], b_step=case[1], goal=goal, cost_a=3, cost_b=1
        )
    return running_cost


if __name__ == "__main__":
    print(part_two())
