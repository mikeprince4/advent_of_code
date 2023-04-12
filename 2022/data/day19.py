
from mip import Model, minimize, BINARY, CONTINUOUS, INTEGER, maximize, xsum
import pandas as pd
from dataclasses import dataclass
from typing import Set


data = list(pd.read_csv("data/aoc - day19.csv").dummy)
#data = ["Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."]
#data.append("Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.")

blueprints = {}
for idx, row in enumerate(data):

    splt = row.split()
    bp_id = int(splt[1].replace(":", ""))

    costs = {"ore": {"ore": int(splt[6])},
             "clay": {"ore": int(splt[12])},
             "obsidian": {"ore": int(splt[18]), "clay": int(splt[21])},
             "geode": {"ore": int(splt[27]), "obsidian": int(splt[30])},
             }
    blueprints[bp_id] = costs

    if idx == 2:
        break
"""

Sets
___________________________

Let R = {"ore", "clay", "obsidian", "geode"} represent the set of rocks and robots
Let T = {1, ...., 24} represent the set of time periods

Parameters
___________________________
n_{r, r'} = the amount of rock of type r' needed to produce a robot of type r



Variables
___________________________
Let c_rt represent the volume of rock that's been collected at time t
Let x_rt represent the number of robots of type r produced at time ime t
Let y_rt represent the number of robots of type r which exist at time t


Constraints
______________________________

x_{ore, 1} = 1                                       -- We start with 1 ore collecting robot
x_{r, 1} = 0 for r \in R \ ore                       -- And no other robots

y_{r, t} = y_{r, t-1}  + x_{r, t}

sum_{r \in R} n_r, r' * x_{r, t} <= c_{r', t}   \ forlall r \in R, r' \in R, t \in T -- The number of rocks of type r' used to produce robots of type r cannot exceed what has been collected

c_{r', t} = c_{r', t-1} + x_{r', t-1} - sum_{r \in R} n_r, r' * x_{r, t}   -- The amount of rock r' at time t equals the amount from the previous period - the amount used to create robots + the amount collected



"""

rock_we_want = 3
num_minutes = 32

R = {"ore": 0, "clay": 1,  "obsidian": 2, "geode": 3}
I = ["ore", "clay", "obsidian", "geode"]
T = [i for i in range(0, num_minutes+1)]

total_quality = 1


for bp_id, costs in blueprints.items():

    m = Model("AOC Day 19")

    c = [[m.add_var(var_type=INTEGER) for t in T] for r in R]
    x = [[m.add_var(var_type=INTEGER) for t in T] for r in R]
    y = [[m.add_var(var_type=INTEGER) for t in T] for r in R]

    # Maximize the # of geodes at time 24
    m.objective = maximize(c[rock_we_want][num_minutes])

    # Nothing exists at time 0 or at time 1, other than 1 ore robot at time 1
    for r in R.values():
        for t in [0, 1]:
            if r != 0:
                m += c[r][t] == 0
                m += x[r][t] == 0
                m += y[r][t] == 0

    # One ore robot exists at time 1
    m += y[0][0] == 1
    m += y[0][1] == 1
    m += c[0][0] == 0

    # The # of robots at time t = the # from the previous time period + the number produced
    for r in R.values():
        for t in T:
            if t > 0:
                m += y[r][t] == y[r][t-1] + x[r][t-1]

    # The number of rock r' used to produce robots in a time period cannot exceed what exists
    for rock, rock_idx in R.items():
        for t in T:
            if t > 0:
                m += xsum(costs[robot][rock]*x[robot_idx][t]
                          for robot, robot_idx in R.items() if rock in costs[robot]) <= c[rock_idx][t-1]

    # The number of rocks r' which have been collected but not used at time t equals (the amount from the previous period) + (the number of the robots which produce that type) - (those that are used to produce other robots)
    for rock, rock_idx in R.items():
        for t in T:
            if t > 0:
                m += c[rock_idx][t] == c[rock_idx][t-1] + y[rock_idx][t-1] + x[rock_idx][t-1] - xsum(costs[robot][rock]*x[robot_idx][t]
                                                                                                     for robot, robot_idx in R.items() if rock in costs[robot])
    # Force same solution for bp_1
    #m += x[1][12] == 1
    #m += x[1][19] == 0

    # At most 1 robot can be produced per period
    for t in T:
        m += xsum(x[robot_idx][t] for robot, robot_idx in R.items()) <= 1

    status = m.optimize()

    for t in T:
        if t > 0:
            print(f"Minute {t}")
            for rock, rock_idx in R.items():
                if y[rock_idx][t].x + c[rock_idx][t].x + x[rock_idx][t].x > 0:
                    print(
                        f"   {rock}: # robots {y[rock_idx][t].x}; # created {x[rock_idx][t].x}; # collected = {c[rock_idx][t].x} (spent = {c[rock_idx][t].x - c[rock_idx][t-1].x - y[rock_idx][t-1].x - x[rock_idx][t-1].x}; added = {y[rock_idx][t-1].x + x[rock_idx][t-1].x})")

            print()

    print(
        f"bp_id = {bp_id}; status = {status}; # collected {I[rock_we_want]} = {c[rock_we_want][num_minutes].x}")

    total_quality *= c[rock_we_want][num_minutes].x

print(f"total_quality = {total_quality}")
