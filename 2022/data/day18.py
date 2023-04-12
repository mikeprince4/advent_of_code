import pandas as pd
from dataclasses import dataclass
from typing import Set


data = list(pd.read_csv("data/aoc - day18.csv").dummy)
#data = list(pd.read_csv("data/aoc - day18e.csv").dummy)
print(data[-1])

matrix = {}


@dataclass
class Cube:
    x: int
    y: int
    z: int
    is_lava: bool
    has_path: bool

    def is_adjacent(self, other_cube):

        return abs(self.x - other_cube.x) + abs(self.y - other_cube.y) + abs(self.z - other_cube.z) == 1


# ***************************************************************************************
# Read in the lava cubes
# ***************************************************************************************
cubes = {}
for cube in data:
    splt = cube.split(",")
    x, y, z = int(splt[0]), int(splt[1]), int(splt[2])

    cubes[(x, y, z)] = Cube(x, y, z, True, False)

# ***************************************************************************************
# Get the max value and then create a bunch of air cubes in that same overall cube
# ***************************************************************************************
max_x = max([cube.x for cube in cubes.values()])
max_y = max([cube.y for cube in cubes.values()])
max_z = max([cube.z for cube in cubes.values()])
print(f"max_x = {max_x}")
print(f"max_y = {max_y}")
print(f"max_z = {max_z}")

print(
    f"# cubes = {len(cubes)}; total air = {(max_x+1)*(max_y+1)*(max_z+1) - len(cubes)}")

for x in range(0, max_x+1):
    for y in range(0, max_y+1):
        for z in range(0, max_z+1):
            if (x, y, z) not in cubes:
                has_path = x == 0 or y == 0 or z == 0 or x == max_x or y == max_y or z == max_z
                cubes[(x, y, z)] = Cube(
                    x, y, z, is_lava=False, has_path=has_path)

print(f"# cubes = {len(cubes)}")
print(f"total has path = {sum([c.has_path for c in cubes.values()])}")


# ***************************************************************************************
# Look through air cubes and set has_path to true for any air cube adjacent to another air cube with has_path = True
# ***************************************************************************************
air_cubes = [c for c in cubes.values() if not c.is_lava]

print(f"# air cubes = {len(air_cubes)}")

while len(air_cubes) > 0:
    cubes_with_path = [c for c in air_cubes if c.has_path]

    if len(cubes_with_path) > 0:
        air_cube = cubes_with_path[0]
        air_cubes.remove(air_cube)
    else:
        print(f"breaking even though there are {len(air_cubes)}")
        break

    print(f"Selected one with path = {air_cube}")

    for (x, y, z) in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
        adj_x = air_cube.x + x
        adj_y = air_cube.y + y
        adj_z = air_cube.z + z

        if (adj_x, adj_y, adj_z) in cubes:
            cube = cubes[(adj_x, adj_y, adj_z)]
            if not cube.is_lava:
                print(f"   updating adjacent cubes = {cube}")
                cube.has_path = True

print(f"total has path = {sum([c.has_path for c in cubes.values()])}")
print(cubes[(2, 2, 5)])

# ***************************************************************************************
# Look through the lava cubes to see which sides are adjacent to air cubes that have a path to the edge
# ***************************************************************************************

lava_cubes = [c for c in cubes.values() if c.is_lava]

surface_area = 6*len(lava_cubes)
for cube in lava_cubes:
    for other_cube in cubes.values():
        if cube.is_adjacent(other_cube):
            if other_cube.is_lava or not other_cube.has_path:
                surface_area -= 1


print(
    f"# cubes = {len(cubes)}; # sides = {6*len(cubes)}; surface_area = {surface_area}")
