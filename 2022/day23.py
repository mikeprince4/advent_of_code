import pandas as pd
from dataclasses import dataclass
from typing import Set, Any, Tuple

data = list(open("data/day23.txt").readlines())


@dataclass
class Elf:
    row: int
    col: int
    proposed_loc: Tuple


print(data[-1])

elves = []
for r, row in enumerate(data):
    for c, char in enumerate(row):
        if char == '#':
            elves.append(Elf(r, c, (r, c)))


moves_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # NSWE

move_to_spaces = {(-1, 0): [(-1, -1), (-1, 0), (-1, 1)],
                  (1, 0): [(1, -1), (1, 0), (1, 1)],
                  (0, -1): [(-1, -1), (0, -1), (1, -1)],
                  (0, 1): [(-1, 1), (0, 1), (1, 1)]}

all_moves = [(-1, -1), (-1, 0), (-1, 1), (1, -1),
             (1, 0), (1, 1), (0, -1), (0, 1)]


def display(elves):
    curr_elf_locations = set([(elf.row, elf.col) for elf in elves])
    min_r = min([elf.row for elf in elves])
    max_r = max([elf.row for elf in elves])
    min_c = min([elf.col for elf in elves])
    max_c = max([elf.col for elf in elves])

    for r in range(min_r, max_r+1):
        str = ""
        for c in range(min_c, max_c+1):
            str += "." if (r, c) not in curr_elf_locations else "#"

        print(str)


print(f"Initial:")
display(elves)

for round in range(10000000):
    curr_elf_locations = set([(elf.row, elf.col) for elf in elves])
    proposed_loc_counts = {}

    # Find each elf's proposed move
    for elf in elves:
        elf.proposed_loc = None
        for proposed_move in moves_list:

            is_alone = True
            for space in all_moves:
                (r, c) = (elf.row + space[0], elf.col + space[1])
                if (r, c) in curr_elf_locations:
                    is_alone = False

            if not is_alone:
                can_move = True
                for space in move_to_spaces[proposed_move]:
                    (r, c) = (elf.row + space[0], elf.col + space[1])
                    if (r, c) in curr_elf_locations:
                        can_move = False
                        break

                if can_move:
                    elf.proposed_loc = (
                        elf.row + proposed_move[0], elf.col + proposed_move[1])
                    if elf.proposed_loc not in proposed_loc_counts:
                        proposed_loc_counts[elf.proposed_loc] = 1
                    else:
                        proposed_loc_counts[elf.proposed_loc] = proposed_loc_counts[elf.proposed_loc] + 1

                    break

    # Update locations if they can move
    # print(proposed_loc_counts)
    some_elf_moved = False
    for elf in elves:
        if elf.proposed_loc is not None and proposed_loc_counts[elf.proposed_loc] == 1:
            elf.row = elf.proposed_loc[0]
            elf.col = elf.proposed_loc[1]
            some_elf_moved = True

    if not some_elf_moved:
        print(f"no elves moved in round {round+1}")
        break

    # Move first move to the end
    first_move = moves_list[0]
    moves_list.remove(first_move)
    moves_list.append(first_move)

    # print()
    #print(f"End of round {round+1} first_move {first_move}")

    # display(elves)


min_r = min([elf.row for elf in elves])
max_r = max([elf.row for elf in elves])
min_c = min([elf.col for elf in elves])
max_c = max([elf.col for elf in elves])

print(min_r)
print(max_r)
print(min_c)
print(max_c)

print((max_r-min_r+1)*(max_c-min_c+1) - len(elves))
