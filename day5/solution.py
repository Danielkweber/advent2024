from functools import cmp_to_key, reduce
import re


def read_input():
    rules = {}
    printer_seqs = []
    with open("input.txt", "r") as f:
        for line in f:
            rule_match = re.search("(\d+)\|(\d+)", line)
            list_match = re.search("\d+,", line)
            if rule_match:
                after_num = int(rule_match.group(2))
                before_num = int(rule_match.group(1))
                if after_num in rules:
                    rules[after_num].append(before_num)
                else:
                    rules[after_num] = [before_num]
            elif list_match:
                seq = [int(num.strip()) for num in line.split(",")]
                printer_seqs.append(seq)
    return rules, printer_seqs


def sequence_is_valid(rules, seq):
    illegal_nums = set()
    for num in seq:
        if num in illegal_nums:
            return False
        illegal_nums |= set(rules[num])
    return True


def part_one():
    rules, printer_seqs = read_input()
    return reduce(
        lambda x, y: x + y[len(y) // 2] if sequence_is_valid(rules, y) else x,
        printer_seqs,
        0,
    )


def build_comparator(rules):
    def compare(x, y):
        if y in rules[x]:
            return 1
        if x in rules[y]:
            return -1
        return 0

    return compare


def part_two():
    rules, printer_seqs = read_input()
    sort_key = cmp_to_key(build_comparator(rules))
    return reduce(
        lambda x, y: (
            x + sorted(y, key=sort_key)[len(y) // 2]
            if not sequence_is_valid(rules, y)
            else x
        ),
        printer_seqs,
        0,
    )


if __name__ == "__main__":
    print(part_two())
