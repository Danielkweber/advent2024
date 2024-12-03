from typing import List, Never


def part_one():
    safe_count = 0
    with open("./input.txt", "r") as f:
        for line in f:
            vals = line.split(" ")
            int_vals = [int(val) for val in vals]
            if is_safe(int_vals):
                safe_count += 1
    return safe_count


def part_two():
    safe_count = 0
    with open("./input.txt", "r") as f:
        for line in f:
            vals = line.split(" ")
            int_vals = [int(val) for val in vals]
            if is_safe(int_vals):
                safe_count += 1
            else:
                for i in range(len(int_vals)):
                    if is_safe(int_vals[:i] + int_vals[i + 1 :]):
                        safe_count += 1
                        break

    return safe_count


def is_safe(nums: List[int]) -> bool:
    if nums[0] == nums[1]:
        return False

    if nums[0] > nums[1]:
        for i in range(1, len(nums)):
            dist = abs(nums[i - 1] - nums[i])
            if nums[i - 1] < nums[i] or dist < 1 or dist > 3:
                return False
        return True

    if nums[0] < nums[1]:
        for i in range(1, len(nums)):
            dist = abs(nums[i - 1] - nums[i])
            if nums[i - 1] > nums[i] or dist < 1 or dist > 3:
                return False
        return True
    return Never


if __name__ == "__main__":
    print(part_two())
