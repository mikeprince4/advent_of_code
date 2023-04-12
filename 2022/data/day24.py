from dataclasses import dataclass
from typing import Set, Any, Tuple

data = list(open("data/day24.txt").readlines())

num_cols = len(data[0]) - 1
num_rows = len(data)


print(f"num_rows = {num_rows}; num_cols = {num_cols}")

blizzards = {}


def calc_lcm(n1, n2):

    for i in range(1, n1*n2+1):

        if i % n1 == 0 and i % n2 == 0:
            return i


lcm = calc_lcm(num_rows-2, num_cols-2)


@dataclass
class Blizzard:
    id: int
    dir: int
    start_row: int
    start_col: int
    time_to_loc_dict: dict

    def get_loc_at_time(self, time):

        if self.dir == ">":
            row = self.start_row
            col = (self.start_col + time) % (num_cols - 2)
        elif self.dir == "<":
            row = self.start_row
            col = (self.start_col - time) % (num_cols - 2)
        elif self.dir == "v":
            row = (self.start_row + time) % (num_rows - 2)
            col = self.start_col
        else:
            row = (self.start_row - time) % (num_rows - 2)
            col = self.start_col

        return (row, col)


for r, row in enumerate(data):

    for c, char in enumerate(row):
        if char not in ["#", ".", "\n"]:
            b_id = len(blizzards)
            blizzards[b_id] = Blizzard(b_id, char, r-1, c-1, {})

print(blizzards)


def print_board_at_time(time):

    matrix = {}
    for r in range(num_rows):
        matrix[r] = {}
        for c in range(num_cols):
            matrix[r][c] = "."

    for b in blizzards.values():
        row, col = b.get_loc_at_time(time)

        matrix[row][col] = b.dir

    for r in range(num_rows-2):
        str = "#"
        for c in range(num_cols-2):
            str += matrix[r][c]

        str += "#"
        print(str)


print_board_at_time(0)


my_loc = (-1, 0)
dest = (num_rows-2, num_cols-3)
start_time = 551

#my_loc = (num_rows-2, num_cols-3)
#dest = (-1, 0)
#start_time = 271

print(f"my_loc = {my_loc}; dest = {dest}")

init = (0, my_loc[0], my_loc[1])

time_locs = {}
time_locs[init] = None


finalized = {}
finalized[init] = None

print(time_locs)

blocked = set()

max_t = 1000


for t in range(max_t):
    for b in blizzards.values():
        r, c = b.get_loc_at_time(t)
        blocked.add((t-start_time, r, c))
print(f"Generated the blocked list")


def get_next(time_locs):

    best_v = 100000
    best_loc = None
    for loc, prev in time_locs.items():
        if loc[0] < best_v:
            # if loc[1] + loc[2] > best_v:
            best_v = loc[0]  # = loc[1] + loc[2]
            best_loc = loc
            best_prev = prev

    del time_locs[best_loc]
    return best_loc, best_prev


remainders = set()
while True:

    curr, prev = get_next(time_locs)

    #print(f"processing {curr}; prev = {prev}")

    t, row, col = curr

    for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
        r, c = row+direction[0], col + direction[1]

        if (r == my_loc[0] and c == my_loc[1]) or (r == dest[0] and c == dest[1]) or (0 <= r <= num_rows-3 and 0 <= c <= num_cols-3):
            time_loc = (t+1, row+direction[0], col+direction[1])
            if time_loc not in blocked and time_loc not in finalized:

                remaindered = (t+1) % lcm
                other = (remaindered, r, c)
                #print(f"for {time_loc} the remaindered version is {other}")
                if other not in remainders:
                    remainders.add(other)
                    time_locs[time_loc] = curr

    finalized[curr] = prev

    if len(time_locs) == 0:
        break


min_t = 10000
for t, r, c in finalized:
    if r == dest[0] and c == dest[1] and t < min_t:
        min_t = t

curr = (min_t, dest[0], dest[1])
path = list()
print(f"Here's the path from {init} to {dest}:")
while True:

    prev = finalized[curr]

    path.insert(0, curr)

    curr = prev

    if curr == None:
        break


for node in path:
    print(node)
