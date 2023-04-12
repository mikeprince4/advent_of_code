import pandas as pd
from dataclasses import dataclass
from typing import Set

data = list(pd.read_csv("data/aoc - day15.csv").dummy)
#data = list(pd.read_csv("data/aoc - day15e.csv").dummy)
print(data[-1])
y = 2000000


sensors = {}
beacons = {}
sensor_dist = {}

for idx, row in enumerate(data):
    space_split = row.split(" ")
    sensor_x = int(space_split[2].split("=")[1].replace(',', ""))
    sensor_y = int(space_split[3].split("=")[1].replace(':', ""))

    beacon_x = int(space_split[8].split("=")[1].replace(',', ""))
    beacon_y = int(space_split[9].split("=")[1])

    sensors[idx] = (sensor_x, sensor_y)
    beacons[idx] = (beacon_x, beacon_y)

    sensor_dist[idx] = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

    print(
        f"sensor_x = {sensor_x}; sensor_y = {sensor_y}; beacon_x = {beacon_x}; beacon_y = {beacon_y}; sensor_dist[idx] = {sensor_dist[idx]}")


min_x = min([sensor[0] for sensor in sensors.values()])
max_x = max([sensor[0] for sensor in sensors.values()])


min_x = min(min([beacon[0] for beacon in beacons.values()]), min_x)
max_x = max(max([beacon[0] for beacon in beacons.values()]), max_x)


print(f"min_x = {min_x}")
print(f"max_x = {max_x}")

total = 0

y = 2000000

stupid = False
if stupid:
    for y in range(0, 4_000_001):

        for x in range(0, 4_000_001):
            if x % 100000 == 0:
                print(f"x = {x}")

            counts = 0
            potential_beacon = (x, y)
            for idx, sensor in sensors.items():

                if potential_beacon not in beacons.values():
                    dist = abs(sensor[0] - potential_beacon[0]) + \
                        abs(sensor[1] - potential_beacon[1])

                    # print(
                    #    f"comparing {x}, {y} to {sensor}; dist = {dist}; sensor_dist[idx] = {sensor_dist[idx]}")
                    if dist <= sensor_dist[idx]:
                        counts = 1
                        # print(
                        #    f"{potential_beacon} would be closer to {sensor} with a dist of {dist} than {beacons[idx]} which has a dist of {sensor_dist[idx]}")
                        break

            if counts == 0 and potential_beacon not in beacons.values():
                print(potential_beacon)
                print(potential_beacon[0]*4000000+potential_beacon[1])
                quit()

        total += counts

if stupid:
    impossible_locations = set()

    print(len(impossible_locations))
    for idx, sensor in sensors.items():

        for x in range(sensor[0] - sensor_dist[idx], sensor[0] + sensor_dist[idx]):
            x_dist = abs(x-sensor[0])
            for y in range(sensor_dist[idx]-x_dist, sensor[1] + x_dist):
                impossible_locations.add((x, y))

    print(len(impossible_locations))


pt = (0, 0)

for idx, sensor in sensors.items():
    min_diff = 4_000_000*2
    dist = abs(sensor[0] - pt[0]) + abs(sensor[1] - pt[1])

    diff = dist - sensor_dist[idx]

    print(f"distance to beacon = {dist}; sensor_dist = {sensor_dist[idx]}")
    if dist < sensor_dist[idx]:
        print(
            f"Can't be here or anywhere between {pt} and {sensor} which has closest beacon = {beacons[idx]}")

        pt = sensor[0] + 
    # if diff < min_diff:
    #    min_diff = diff
    #    print(
    #        f"min_diff = {min_diff}; dist = {dist} sensor_dist = {sensor_dist[idx]}")


print(min_diff)
