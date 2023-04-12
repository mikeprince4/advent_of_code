
from mip import Model, minimize, BINARY, CONTINUOUS, INTEGER, maximize, xsum
import pandas as pd
from dataclasses import dataclass
from typing import Set


data = list(pd.read_csv("data/aoc - day20.csv").dummy)
print(f"list length = {len(data)}; # unique values = {len(set(data))}")

print(max(data))
print(min(data))
# quit()

#data = [1, 2, -3, 3, -2, 0, 4]


@dataclass
class Element:
    initial_idx: int
    val: int
    orig_val: int
    orig_val_multiplied: int


multiplier = 811589153
num_rounds = 10

data = [Element(idx, n*multiplier, n, n*multiplier)
        for idx, n in enumerate(data)]


idx_to_ele = {data.index(ele): ele for ele in data}

data_copy = data.copy()

print_details = False

for j in range(0, num_rounds):
    for i in range(0, len(data)):
        ele = idx_to_ele[i]

        current_idx = data_copy.index(ele)
        data_copy.remove(ele)
        new_idx = (current_idx + ele.val) % len(data_copy)
        data_copy.insert(new_idx, ele)

        if print_details:
            print(
                f"moved {ele.val} from {current_idx} to {new_idx}; new list = {[ele.orig_val_multiplied for ele in data_copy]}")

    #print(f"Round {j}: new list = {[ele.orig_val_multiplied for ele in data_copy]}")

element_with_val_0 = [ele for ele in data_copy if ele.val == 0]

print(element_with_val_0)


start_idx = data_copy.index(element_with_val_0[0])

print(f"index of element 0 = {start_idx}")

idx_1000 = (start_idx+1000) % len(data_copy)
idx_2000 = (start_idx+2000) % len(data_copy)
idx_3000 = (start_idx+3000) % len(data_copy)
print(f"idx_1000 = {idx_1000} num =  {data_copy[idx_1000]}")
print(f"idx_2000 = {idx_2000} num =  {data_copy[idx_2000]}")
print(f"idx_3000 = {idx_3000} num =  {data_copy[idx_3000]}")


data = [ele.val for ele in data_copy]

# print(data)

print(
    f"sum = {multiplier*(data_copy[idx_1000].orig_val+data_copy[idx_2000].orig_val+data_copy[idx_3000].orig_val)}")
