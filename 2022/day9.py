
from helpers import get_data

example = False

data = get_data(example)

pos = {}
for i in range(10):
    pos[i] = [0, 0]


positions = set()
positions.add((pos[9][0], pos[9][1]))

for steps in data:
    splitted = steps.split(" ")
    direction = splitted[0]
    count = int(splitted[1])
    # print()
    # print(steps)
    for i in range(count):
        if direction == "U":
            pos[0][1] += 1
        elif direction == "D":
            pos[0][1] -= 1
        elif direction == "L":
            pos[0][0] -= 1
        else:
            pos[0][0] += 1

        for i in range(1, 10):

            if pos[i-1][0] == pos[i][0] + 2:
                pos[i][0] += 1

                if abs(pos[i-1][1] - pos[i][1]) == 1:
                    pos[i][1] = pos[i-1][1]
                elif pos[i-1][1] == pos[i][1] + 2:
                    pos[i][1] += 1
                elif pos[i-1][1] == pos[i][1] - 2:
                    pos[i][1] -= 1

            if pos[i-1][0] == pos[i][0] - 2:
                pos[i][0] -= 1

                if abs(pos[i-1][1] - pos[i][1]) == 1:
                    pos[i][1] = pos[i-1][1]
                elif pos[i-1][1] == pos[i][1] + 2:
                    pos[i][1] += 1
                elif pos[i-1][1] == pos[i][1] - 2:
                    pos[i][1] -= 1

            if pos[i-1][1] == pos[i][1] + 2:
                pos[i][1] += 1

                if abs(pos[i-1][0] - pos[i][0]) == 1:
                    pos[i][0] = pos[i-1][0]
                elif pos[i-1][0] == pos[i][0] + 2:
                    pos[i][0] += 1
                elif pos[i-1][0] == pos[i][0] - 2:
                    pos[i][0] -= 1

            if pos[i-1][1] == pos[i][1] - 2:
                pos[i][1] -= 1

                if abs(pos[i-1][0] - pos[i][0]) == 1:
                    pos[i][0] = pos[i-1][0]
                elif pos[i-1][0] == pos[i][0] + 2:
                    pos[i][0] += 1
                elif pos[i-1][0] == pos[i][0] - 2:
                    pos[i][0] -= 1

        #print((T_pos[0], T_pos[1]))
        positions.add((pos[9][0], pos[9][1]))

        # for i in range(10):
        #   print(f"{i}: {pos[i]}")

        # print()
# for i in range(10):
    #print(f"{i}: {pos[i]}")

print(len(positions))
