import pandas as pd
from dataclasses import dataclass
from typing import Set


@dataclass
class Node:
    row: int
    col: int
    char: str
    out_arcs: list
    in_arcs: list

    def __post_init__(self):

        self.id = (self.row, self.col)
        self.label = 100000

    def __hash__(self):

        return hash(self.id)

    def __repr__(self):

        return f"Node({self.id}, {self.char}, {self.label})"


@dataclass
class Arc:
    from_node: Node
    to_node: Node
    weight: float


def can_traverse(from_node, to_node):
    from_char_ord = ord(from_node.char)
    to_char_ord = ord(to_node.char)
    #print(f"{from_char_ord} {to_char_ord}")
    if to_char_ord <= from_char_ord + 1:
        #print(f"can traverse")
        return True
    else:
        # print(f"Cannot")
        return False


def get_next_node(nodes, finalized):

    best_label = 1000000
    best_node = None
    for node in nodes.values():

        if node not in finalized and node.label < best_label:
            best_label = node.label
            best_node = node

    return best_node


data = list(pd.read_csv("data/aoc - day12.csv").dummy)
#data = list(pd.read_csv("data/aoc - day12e.csv").dummy)
print(data[-1])

nodes = {}

source_node = None
target_node = None

num_cols = 0

for r, row in enumerate(data):
    for c, char in enumerate(row):
        num_cols = len(row)

        node = Node(row=r, col=c, char=char, out_arcs=list(), in_arcs=list())
        nodes[(r, c)] = node

        if char == "E":
            node.char = "{"

        if char == "S":
            node.char = "`"

print(f"# rows, cols = {len(data)}, {num_cols}")


source_node = [node for node in nodes.values() if node.char == "{"][0]
target_node = [node for node in nodes.values() if node.char == "`"][0]

print(f"source = {source_node}")
print(f"target = {target_node}")

arc_count = 0
for node in nodes.values():
    row = node.row
    col = node.col

    #print(f"Looking for arcs out of {node}")

    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if r >= 0 and r < len(data) and c >= 0 and c < num_cols:
            if can_traverse(node, nodes[(r, c)]):
                arc = Arc(from_node=node, to_node=nodes[(r, c)], weight=1)
                node.out_arcs.append(arc)
                nodes[(r, c)].in_arcs.append(arc)

                arc_count += 1

for arc in source_node.in_arcs:
    print(arc)

print(f"# of arcs = {arc_count}")


best = 100000
source_node.label = 0

finalized = set()

while True:

    next_node = get_next_node(nodes, finalized)

    #print(f"next_node = {next_node}")
    for arc in next_node.in_arcs:
        if next_node.label + arc.weight < arc.from_node.label:
            arc.from_node.label = next_node.label + arc.weight

    finalized.add(next_node)
    if len(finalized) == len(nodes):
        break

if target_node.label < best:
    best = target_node.label

print(f"target node label = {target_node.label}")


print(best)


best_a = 100000
for node in nodes.values():

    if node.char == "a" and node.label < best_a:
        best_a = node.label

print(best_a)
