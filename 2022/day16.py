from mip import Model, minimize, BINARY, CONTINUOUS, maximize, xsum
import pandas as pd
from dataclasses import dataclass
from typing import Set
from dataclasses import dataclass


data = list(pd.read_csv("data/aoc - day16.csv").dummy)
#data = list(pd.read_csv("data/aoc - day16e.csv").dummy)
print(data[-1])


@dataclass
class Valve:
    idx: str
    valve_id: str
    flow_rate: int
    reachable_valves: list
    is_open: bool


valves = {}
for idx, row in enumerate(data):
    splt = row.split()
    valve_id = splt[1]
    flow_rate = int(splt[4].split("=")[1].replace(";", ""))

    reachable_valves = [splt[i].replace(",", "") for i in range(9, len(splt))]

    valves[valve_id] = Valve(idx, valve_id, flow_rate,
                             reachable_valves, is_open=False)

    print(valves[valve_id])

num_periods = 26

T = [t for t in range(0, num_periods+1)]

m = Model("AOC Day 16")

total_flow = m.add_var(var_type=CONTINUOUS)

V = [valve.idx for valve in valves.values()]

P = [0, 1]

print(V)
print(T)


x = [[m.add_var(var_type=BINARY) for t in T] for v in V]
y = [[[[m.add_var(var_type=BINARY) for t in T]
      for v in valves.keys()] for v in V] for p in P]  # y is the arc with time cost of 1 but no opening
z = [[[[m.add_var(var_type=BINARY) for t in T]
      for v in valves.keys()] for v in V] for p in P]  # z is the arc with time cost of 2 but it does open

m += total_flow == xsum(v.flow_rate*x[v.idx][t]
                        for v in valves.values() for t in T if t > 0)


for valve in valves.values():
    for t in T:

        if t > 0:

            inbound_valves = [v.idx for v in valves.values(
            ) if valve.valve_id in v.reachable_valves]

            print(f"t = {t} inbound_valves = {inbound_valves} for {valve}")

            # x can only be active if one of the z-arcs was active for 2 periods prior or earlier
            m += x[valve.idx][t] <= xsum(z[p][ib_v][valve.idx][tprime]
                                         for p in P for ib_v in inbound_valves for tprime in range(1, t-1))

            for p in P:

                # Inflow = outflow
                outbound_valves = [
                    valves[v].idx for v in valve.reachable_valves]

                left_hand_side = 1 if valve.valve_id == "AA" and t == 1 else 0
                if t > 1:
                    left_hand_side += xsum(y[p][ib_v][valve.idx][t-1]
                                           for ib_v in inbound_valves)
                if t > 2:
                    left_hand_side += xsum(z[p][ib_v][valve.idx][t-2]
                                           for ib_v in inbound_valves)

                constr = left_hand_side == \
                    xsum(y[p][valve.idx][ob_v][t] for ob_v in outbound_valves) + \
                    xsum(z[p][valve.idx][ob_v][t] for ob_v in outbound_valves)

                m += constr


m.objective = maximize(total_flow)

m.write("model.lp")
print(m.objective)
status = m.optimize()

total = 0
print_x = True
if print_x:
    for t in T:
        tot = 0
        for valve in valves.values():
            tot += valve.flow_rate*x[valve.idx][t].x

        print(f"t = {t}; tot = {tot}")
        total += tot

print(f"total = {total}")

print_y = True
if print_y:
    for p in P:
        for t in T:
            for v1 in valves.values():
                for v2 in valves.values():

                    y_val = y[p][v1.idx][v2.idx][t].x
                    z_val = z[p][v1.idx][v2.idx][t].x

                    if (y_val + z_val > 0):

                        print(
                            f"t={t}; arc({p},{v1.valve_id}, {v2.valve_id}) y = {y_val}; z = {z_val}")

print(status)
print(total_flow.x)
