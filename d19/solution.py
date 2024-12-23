from functools import reduce
from typing import Set


def read_input():
    with open("./input.txt", "r") as f:
        towel_str, seq_str = f.read().split("\n\n")
        towels = [towel.strip() for towel in towel_str.split(",")]
        seqs = [seq.strip() for seq in seq_str.split("\n")]
    return towels, seqs[:-1]


def solve():
    towels, seqs = read_input()
    max_towel_length = max([len(towel) for towel in towels])
    towel_set = set(towels)
    check_memo = {}
    seq_checks = [
        check_seq(seq, towel_set, max_towel_length, False, check_memo) for seq in seqs
    ]
    count_memo = {}
    seq_counts = [
        check_seq(seq, towel_set, max_towel_length, True, count_memo) for seq in seqs
    ]
    valids = reduce(lambda x, y: x + y, seq_checks, 0)
    count_ways = reduce(lambda x, y: x + y, seq_counts, 0)
    print(f"Part 1 - Valid Sequences: {valids}")
    print(f"Part 2 - Valid Sequences: {count_ways}")


def check_seq(seq: str, towels: Set[str], max_length: int, count: bool, memo) -> int:
    if seq in memo:
        return memo[seq]
    if len(seq) == 0:
        return 1
    check = [seq[:i] in towels and i <= len(seq) for i in range(1, max_length + 1)]
    recs = [
        (
            f"check_seq(seq[{i + 1}:], towels, max_length, {count},  memo)"
            if val
            else "0"
        )
        for i, val in enumerate(check)
    ]
    # Add if we're counting way to construct a sequence else use or
    op = " + " if count else " | "
    stmt = op.join(recs)
    memo[seq] = eval(stmt)
    return memo[seq]


if __name__ == "__main__":
    solve()
