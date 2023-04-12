import pandas as pd
import json

data = list(pd.read_csv("data/aoc - day13.csv").dummy)
#data = list(pd.read_csv("data/aoc - day13e.csv").dummy)
print(data[-1])

packet_pairs = {}


def are_lists_in_right_order(left, right):
    correct_order = "TIE"
    for idx, l_item in enumerate(left):

        # If right ends out of items first, lists are not in the right order
        if idx >= len(right):
            return False

        r_item = right[idx]
        if isinstance(l_item, int) and isinstance(r_item, int):
            if l_item < r_item:
                print(f"{l_item} < {r_item}")
                return True
            elif l_item > r_item:
                print(f"{l_item} > {r_item}")
                return False
            else:
                print(f"Tie between {l_item} and {r_item}")

        elif isinstance(l_item, list) and isinstance(r_item, list):

            correct_order = are_lists_in_right_order(l_item, r_item)

            if correct_order != "TIE":
                return correct_order

        else:
            print("Mixed types")
            if isinstance(l_item, int):
                l_item = [l_item]

            if isinstance(r_item, int):
                r_item = [r_item]

            correct_order = are_lists_in_right_order(l_item, r_item)

            if correct_order != "TIE":
                return correct_order

    # If we ran out of left items first, then it's the correct order
    if len(right) > len(left):
        print(f"Left has more")
        return True

    # print(f"Howd we make it here? left = {left} right = {right}")
    return correct_order


class Packet:

    value: list

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return are_lists_in_right_order(self.value, other.value)


all_packets = []

for idx, row in enumerate(data):

    if idx % 2 == 0:
        first_packet = json.loads(row)

    if idx % 2 == 1:
        second_packet = json.loads(row)

        packet_pairs[len(packet_pairs) + 1] = (first_packet, second_packet)

    all_packets.append(Packet(json.loads(row)))
print(packet_pairs)

all_packets.append(Packet([[2]]))
all_packets.append(Packet([[6]]))


all_packets.sort()


idx_1 = 0
idx_2 = 0

for idx, packet in enumerate(all_packets):
    if packet.value == [[2]]:
        print(idx)
        idx_1 = idx + 1

    if packet.value == [[6]]:
        print(idx)
        idx_2 = idx + 1

print(idx_1*idx_2)
"""
right_ordered_idx = []
for pair_index, pair in packet_pairs.items():
    left = pair[0]
    right = pair[1]

    print(
        f"Comparing pair_index {pair_index}; {left}   to   {right}")
    correct_order = are_lists_in_right_order(left, right)

    print(
        f"\t\tcorrect_order = {correct_order}")
    if correct_order:
        right_ordered_idx.append(pair_index)

    if correct_order == "TIE":
        print(f"Found a tie! ")
        quit()

    print()
print(right_ordered_idx)
print(sum(right_ordered_idx))
"""
