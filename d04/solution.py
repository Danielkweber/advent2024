from typing import List


def read_input():
    with open("./input.txt", "r") as f:
        return [list(line.strip()) for line in f]


def expand_x_cell(grid: List[List[str]], i: int, j: int, width: int, height: int):
    count = 0
    if j + 4 <= width:
        east_string = "".join([grid[i][j + num] for num in range(4)])
        count += east_string == "XMAS"
    if j - 3 >= 0:
        west_string = "".join([grid[i][j - num] for num in range(4)])
        count += west_string == "XMAS"
    if i + 4 <= height:
        south_string = "".join([grid[i + num][j] for num in range(4)])
        count += south_string == "XMAS"
    if i - 3 >= 0:
        north_string = "".join([grid[i - num][j] for num in range(4)])
        count += north_string == "XMAS"
    if j + 4 <= width and i + 4 <= height:
        se_string = "".join([grid[i + num][j + num] for num in range(4)])
        count += se_string == "XMAS"
    if j + 4 <= width and i - 3 >= 0:
        ne_string = "".join([grid[i - num][j + num] for num in range(4)])
        count += ne_string == "XMAS"
    if j - 3 >= 0 and i - 3 >= 0:
        nw_string = "".join([grid[i - num][j - num] for num in range(4)])
        count += nw_string == "XMAS"
    if j - 3 >= 0 and i + 4 <= height:
        sw_string = "".join([grid[i + num][j - num] for num in range(4)])
        count += sw_string == "XMAS"
    return count


def expand_a_cell(grid: List[List[str]], i: int, j: int, width: int, height: int):
    if i - 1 >= 0 and j - 1 >= 0 and j + 1 < width and i + 1 < height:
        slope_up = "".join([grid[i + num][j + num] for num in range(-1, 2)])
        slope_down = "".join([grid[i - num][j + num] for num in range(-1, 2)])
        return (slope_up == "MAS" or "".join(reversed(slope_up)) == "MAS") and (
            slope_down == "MAS" or "".join(reversed(slope_down)) == "MAS"
        )
    return 0


def solve(part2: bool):
    grid = read_input()
    width = len(grid[0])
    height = len(grid)
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not part2:
                if grid[i][j] != "X":
                    continue
                count += expand_x_cell(grid, i, j, width, height)
            else:
                if grid[i][j] != "A":
                    continue
                count += expand_a_cell(grid, i, j, width, height)

    return count


if __name__ == "__main__":
    print(solve(part2=True))
