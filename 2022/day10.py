
from helpers import get_data

example = False

data = get_data(example)

x = 1
cycles = 0
total = 0

row = 0
row_str = ""

for step in data:
    splitted = step.split(" ")

    if len(splitted) == 1:
        num_cycles = 1
        x_delta = 0
    else:
        num_cycles = 2
        x_delta = int(splitted[1])

    for i in range(num_cycles):
        pixel = cycles % 40
        if pixel == 0:
            print(f"{row_str}")
            row_str = ""
            row += 1

        if abs(x-pixel) <= 1:
            row_str += "#"
        else:
            row_str += "."

        cycles += 1

        if (cycles - 20) % 40 == 0:
            sub_tot = x*cycles
            #print(f"cycle = {cycles}; x = {x}; sub_tot = {sub_tot}")

            total += sub_tot

    x += x_delta

print(row_str)
print(f"Part 1: {total}")
