from dataclasses import dataclass
from typing import List


@dataclass
class TestEq:
    res: int
    operands: List[int]


def read_input():
    eqns: List[TestEq] = []
    with open("./input.txt", "r") as f:
        for line in f:
            sol_str, operand_str = line.split(":")
            sol = int(sol_str.strip())
            operands = [
                int(operand.strip()) for operand in operand_str.strip().split(" ")
            ]
            eqns.append(TestEq(sol, operands))
    return eqns


def eq_is_solvable(eq: TestEq, include_concat_op: bool):
    res, operands = eq.res, eq.operands
    if len(operands) == 1:
        return res == operands[0]
    cases_to_check = []
    add_prefix = operands[0] + operands[1]
    cases_to_check.append(add_prefix)
    mul_prefix = operands[0] * operands[1]
    cases_to_check.append(mul_prefix)
    if include_concat_op:
        concat_prefix = int(str(operands[0]) + str(operands[1]))
        cases_to_check.append(concat_prefix)
    return any(
        map(
            lambda x: eq_is_solvable(
                TestEq(res, [x] + operands[2:]), include_concat_op
            ),
            cases_to_check,
        )
    )


def solve():
    eqns = read_input()
    p1_acc = 0
    p2_acc = 0
    for eq in eqns:
        if eq_is_solvable(eq, include_concat_op=False):
            p1_acc += eq.res
            p2_acc += eq.res
        # A little slower than I'd like for p2 but whataya gonna do
        elif eq_is_solvable(eq, include_concat_op=True):
            p2_acc += eq.res
    return p1_acc, p2_acc


if __name__ == "__main__":
    p1, p2 = solve()
    print(f"Part 1 - Add and Mul: {p1}")
    print(f"Part 2 - Add, Mul, and Concat: {p2}")
