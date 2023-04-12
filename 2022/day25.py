from dataclasses import dataclass
from typing import Set, Any, Tuple

data = list(open("data/day25.txt").readlines())

tot = 0


def get_val(num):

    val = 0
    for idx, char in enumerate(num):
        pos = len(num) - idx - 1
        if char == '2':
            val += 2*5**pos
        elif char == '1':
            val += 5**pos
        elif char == '-':
            val += -5**pos
        elif char == '=':
            val += -2*5**pos

    return val


run_it = True

if run_it:
    for num in data:
        num = num[0:len(num)-1]
        this_tot = get_val(num)
        print(f"n_chars = {len(num)}; num = {num}; this_tot = {this_tot}")
        tot += this_tot
        # break
    print(tot)


#tot = 33007619991752


my_num = "2"
while True:

    if get_val(my_num) > tot:
        break

    my_num = my_num + "0"

print(f"Found a number larger than tot: {my_num}")

for idx, char in enumerate(my_num):

    best_diff = tot
    best_char = None
    for c in ["2", "1", "0", "-", "="]:

        other_num = my_num[0:idx] + c + my_num[idx+1:]

        val = get_val(other_num)

        diff = abs(val-tot)

        if diff < best_diff:
            best_diff = diff
            best_char = c

        print(
            f"other_num: {other_num}; val = {val}: tot = {tot} less than? {val < tot} diff = {diff}")

    my_num = my_num[0:idx] + best_char + my_num[idx+1:]


print(f"my_num = {my_num} val = {get_val(my_num)}; tot = {tot}")
