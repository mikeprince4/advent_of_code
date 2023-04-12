import pandas as pd
from dataclasses import dataclass
from typing import Set, Any

data = list(open("data/day22.txt").readlines())


path = data.pop(-1)
data.pop(-1)

print(path)

num_rows = len(data)
num_cols = max(len(row)-1 for row in data)

print(f"# rows, columns = {num_rows}, {num_cols} ")


matrix = {}

for r_idx, row in enumerate(data):
    matrix[r_idx] = {c_idx: " " for c_idx in range(num_cols)}
    for c_idx, c in enumerate(row):
        if c != '\n':
            matrix[r_idx][c_idx] = c


curr = (min(c for c, v in matrix[0].items() if v != " "), 1, ">")

print(curr)

split_1 = path.split("R")

instructions = []
for idx_1, sub in enumerate(split_1):

    split_2 = sub.split("L")

    for idx_2, sub_2 in enumerate(split_2):
        instructions.append(int(sub_2))
        if idx_2 < len(split_2) - 1:
            instructions.append("L")

    if idx_1 < len(split_1) - 1:
        instructions.append("R")


min_col_in_row = {r: min(
    [c for c in range(0, num_cols) if matrix[r][c] != " "]) for r in range(0, num_rows)}
max_col_in_row = {r: max(
    [c for c in range(0, num_cols) if matrix[r][c] != " "]) for r in range(0, num_rows)}
min_row_in_col = {c: min(
    [r for r in range(0, num_rows) if matrix[r][c] != " "]) for c in range(0, num_cols)}
max_row_in_col = {c: max(
    [r for r in range(0, num_rows) if matrix[r][c] != " "]) for c in range(0, num_cols)}


print(min_col_in_row)
print(max_col_in_row)
print(min_row_in_col)
print(max_row_in_col)


x = len([i for i in matrix[0] if i == ' '])
y = 0
d = ">"


def is_off_map(x, y):
    return y < 0 or x < 0 or y >= len(matrix) or x >= len(matrix[y]) or matrix[y][x] == ' '


def step(curr):
    x, y, d = curr
    prev_x, prev_y, prev_d = x, y, d
    if d == ">":
        x += 1
        if is_off_map(x, y):
            if 0 <= y < 50:
                x = 99
                y = 149 - y
                d = "<"
            elif 50 <= y < 100:
                x = 100 + (y - 50)
                y = 49
                d = "^"
            elif 100 <= y < 150:
                x = 149
                y = 149 - y
                d = "<"
            elif 150 <= y < 200:
                x = 50 + (y - 150)
                y = 149
                d = "^"
    elif d == "<":
        x -= 1
        if is_off_map(x, y):
            if 0 <= y < 50:
                x = 0
                y = 149 - y
                d = ">"
            elif 50 <= y < 100:
                x = y - 50
                y = 100
                d = "v"
            elif 100 <= y < 150:
                x = 50
                y = 149 - y
                d = ">"
            elif 150 <= y < 200:
                x = 50 + (y - 150)
                y = 0
                d = "v"
    elif d == "v":
        y += 1
        if is_off_map(x, y):
            if 0 <= x < 50:
                x = x + 100
                y = 0
                d = "v"
            elif 50 <= x < 100:
                y = 150 + (x - 50)
                x = 49
                d = "<"
            elif 100 <= x < 150:
                y = 50 + (x - 100)
                x = 99
                d = "<"
    elif d == "^":
        y -= 1
        if is_off_map(x, y):
            if 0 <= x < 50:
                y = 50 + x
                x = 50
                d = ">"
            elif 50 <= x < 100:
                y = 150 + (x - 50)
                x = 0
                d = ">"
            elif 100 <= x < 150:
                x = x - 100
                y = 199
                d = "^"
    if matrix[y][x] == '#':
        x, y, d = prev_x, prev_y, prev_d

    return (x, y, d)


print(x, y, d)
for instruction in instructions:
    if instruction == "R":
        if d == ">":
            d = "v"
        elif d == "v":
            d = "<"
        elif d == "<":
            d = "^"
        else:
            d = ">"

    elif instruction == "L":
        if d == ">":
            d = "^"
        elif d == "v":
            d = ">"
        elif d == "<":
            d = "v"
        else:
            d = "<"
    else:
        for j in range(instruction):
            curr = step(curr)

            (x, y, d) = curr

    curr = (x, y, d)
    print(curr)


def get_val_from_dir(d):
    if d == ">":
        return 0
    elif d == "v":
        return 1
    elif d == "<":
        return 2
    else:
        return 3


print(1000 * (y+1) + 4 * (x+1) + get_val_from_dir(d))
