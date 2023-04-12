from mip import Model, minimize, BINARY, CONTINUOUS
import pandas as pd

data = list(pd.read_csv("data/aoc - day15.csv").dummy)
print(data[-1])

# Read sensors, beacons, and calculate distances
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


# ************************************************************************************************
# First create the model
# ************************************************************************************************
m = Model("AOC Day 15")

# ************************************************************************************************
# Now create the variables
# ************************************************************************************************
# Create the (x,y) variables which will be used to specify the beacon's location
x = m.add_var(var_type=CONTINUOUS)
y = m.add_var(var_type=CONTINUOUS)

# x_bar and x_hat will be used to represent the absolute values (x-sensor_x)
x_bar = [m.add_var(var_type=CONTINUOUS) for i in sensors.keys()]
x_hat = [m.add_var(var_type=CONTINUOUS) for i in sensors.keys()]

# y_bar and y_hat will be used to represent the absolute values (y-sensor_y)
y_bar = [m.add_var(var_type=CONTINUOUS) for i in sensors.keys()]
y_hat = [m.add_var(var_type=CONTINUOUS) for i in sensors.keys()]

# Binary variables which will be used to ensure that either x_bar or x_hat is 0, and same thing for y_bar and y_hat
xx = [m.add_var(var_type=BINARY) for i in sensors.keys()]
yy = [m.add_var(var_type=BINARY) for i in sensors.keys()]


# ************************************************************************************************
# Now create the constraints
# ************************************************************************************************

# Upper bound on x, y is 4_000_000
ub = 4_000_000

# Add constraints which constraint x, y between 0 and 4_000_000
m += x >= 0
m += x <= ub

m += y >= 0
m += y <= ub

# Loop through the sensors and add constraints to the model for each
for i, sensor in sensors.items():
    # Specify that x_bar and x_hat must be between 0 and 4_000_000
    # Additionally, since xx_i is binary, this pair of constraint constraint forces either (1) x_bar_i to be 0 or (2) x_hat_i to be 0
    m += 0 <= x_bar[i] <= ub * xx[i]
    m += 0 <= x_hat[i] <= ub * (1-xx[i])

    # Same thing for the y variables
    m += 0 <= y_bar[i] <= ub * yy[i]
    m += 0 <= y_hat[i] <= ub * (1-yy[i])

    # Add the following constraint: (x_bar_i - x_hat_i) == (sensor_x - x)
    #   - For example, let's say sensor_x = 10 and x = 2.  This will result in the following values
    #       -- x_bar = 8
    #       -- x_hat = 0
    #
    #   - Alternatively, let, let's say sensor_x = 2 and x = 10.   This will force the following values
    #       -- x_bar = 0
    #       -- x_hat = 8
    m += x_bar[i] - x_hat[i] == sensor[0] - x

    # Similar constraint but for y
    m += y_bar[i] - y_hat[i] == sensor[1] - y

    # Now add the constraint that forces the sensor's manhattan distance to the beacon to be greater than the sensor's closest beacon
    #   For example:
    #      - Let's say we have sensor_i == (2, 15) with its closest beacon == (10, 10) for a manhattan distance of 13
    #      - Now let's see if, for instance, (x, y) = (7, 12) would be feasible location for the beacon
    #      
    #       From the above constraints, we have the following:
    #            - x_bar_i = 0
    #            - x_hat_i = 5     (i.e. abs(2-7))
    #            - y_bar_i = 3     (i.e. abs(15-12))
    #            - y_hat_i = 0
    # 
    #       The following constraint would then be (0 + 5) + (3 + 0) >= 13 + 1
    #           This constraint is violated, and therefore (7, 12) is NOT a valid location for the beacon
    # 
    m += (x_bar[i] + x_hat[i]) + (y_bar[i] + y_hat[i]) >= sensor_dist[i] + 1

# Solve the model
m.optimize()

print(f"x = {x.x}; y = {y.x}; tot = {int(x.x*4_000_000 + y.x)}")

quit()

print_vals = False
if print_vals:
    for idx, x_bar_ in enumerate(x_bar):
        print(f"x_bar {idx} = {x_bar_.x}")

    for idx, x_hat_ in enumerate(x_hat):
        print(f"x_hat {idx} = {x_hat_.x}")

    for idx, y_bar_ in enumerate(y_bar):
        print(f"y_bar {idx} = {y_bar_.x} ")

    for idx, y_hat_ in enumerate(y_hat):
        print(f"y_hat {idx} = {y_hat_.x} ")


for idx, sensor in sensors.items():

    abs_x = abs(sensor[0] - x.x)
    other_abs_x = x_bar[idx].x + x_hat[idx].x

    abs_y = abs(sensor[1] - y.x)
    other_abs_y = y_bar[idx].x + y_hat[idx].x

    dist_to_beacon = abs_x + abs_y

    print(
        f"idx = {idx}; abs_x = {abs_x}; other_abs_x = {other_abs_x}; abs_y = {abs_y}; other_abs_y = {other_abs_y}; sensor = {sensor}; dist = {sensor_dist[idx]}; dist to beacon = {dist_to_beacon}; {dist_to_beacon < sensor_dist[idx]}")

    if abs_x != other_abs_x or abs_y != other_abs_y or dist_to_beacon < sensor_dist[idx]:
        print(
            f"y_bar[idx] - y_bar[idx] = sensor[1] - y.x:  {y_bar[idx].x} -{y_hat[idx].x} = {sensor[1]} - {y.x}")

        print(
            f"y_bar[idx] - y_bar[idx] = sensor[1] - y.x:  {y_bar[idx].x - y_hat[idx].x} = {sensor[1] - y.x}")

        print(x_bar[idx].x)
        print(x_hat[idx].x)
        print(y_bar[idx].x)
        print(y_hat[idx].x)
