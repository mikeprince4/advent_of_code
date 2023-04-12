import pandas as pd
from dataclasses import dataclass
from typing import Set


data = list(pd.read_csv("data/aoc - day14.csv").dummy)
#data = list(pd.read_csv("data/aoc - day14e.csv").dummy)
print(data[-1])

grid = {}
max_y = 0

for path in data:
    pts = path.split("->")

    prev_x = None
    prev_y = None
    for pt in pts:
        x, y = pt.split(",")
        x = int(x.strip())
        y = int(y.strip())

        if y > max_y:
            max_y = y
        if x not in grid:
            grid[x] = {}
        print(x)
        print(y)
        if prev_x is not None:

            if prev_x == x:
                for ybar in range(min(y, prev_y), max(y, prev_y) + 1):
                    grid[x][ybar] = "#"
            else:
                for xbar in range(min(x, prev_x), max(x, prev_x) + 1):
                    if xbar not in grid:
                        grid[xbar] = {}
                    grid[xbar][y] = "#"

        prev_x = x
        prev_y = y

print(f"min_x = {min(grid.keys())}")
print(f"max_x = {max(grid.keys())}")
print(f"max_y = {max_y}")

for x in range(min(grid.keys())-1000, max(grid.keys())+100):
    if x not in grid:
        grid[x] = {}

    for y in range(0, max_y + 2):
        if y not in grid[x]:
            grid[x][y] = '.'


for x in range(min(grid.keys()), max(grid.keys())):
    print(x)
    print(y)
    grid[x][max_y+2] = "#"

print(grid)
counter = 0
fallen = False
while not fallen:

    curr = (500, 0)
    stopped = False
    while not stopped:

        x = curr[0]
        y = curr[1]
        next_y = y + 1

        if next_y == max_y+3:
            fallen = True
            print(f"FALL")
            break
        #print(f"x = {x}; y = {y}; next_y = {next_y}")
        if grid[x][next_y] == '.':
            curr = (x, next_y)
        elif grid[x-1][next_y] == '.':
            curr = (x-1, next_y)
        elif grid[x+1][next_y] == '.':
            curr = (x+1, next_y)
        else:
            grid[x][y] = "o"

            counter += 1
            stopped = True
            if x == 500 and y == 0:
                print(counter)
                quit()

        #print(f"counter = {counter}; fallen = {fallen}; stopped = {stopped}; curr = {curr}")


print(counter)
