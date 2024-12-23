import re


def reduce_muls(reducer: int, data: str):
    matches = re.findall(pattern="mul\(\d+,\d+\)", string=data)
    for match in matches:
        nums = re.findall("\d+", match)
        reducer += int(nums[0]) * int(nums[1])
    return reducer


def part_one() -> int:
    reducer = 0
    with open("./input.txt", "r") as f:
        data = f.read()
        reducer = reduce_muls(reducer, data)
    return reducer


def part_two() -> int:
    reducer = 0
    place = 0
    with open("./input.txt", "r") as f:
        data = f.read()
        while True:
            # Find end of operable block
            first_dont = re.search("don't\(\)", data[place:])
            end_index = first_dont.start() if first_dont else len(data)
            working_substring = data[place : place + end_index]

            # Reduce
            reducer = reduce_muls(reducer, working_substring)

            # Move place to after the handled substring
            place += end_index

            # Find next operable block
            next_do = re.search("do\(\)", data[place:])
            if not next_do:
                break
            place += next_do.start()
    return reducer


if __name__ == "__main__":
    print(part_one())
