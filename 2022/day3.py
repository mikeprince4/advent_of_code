
from helpers import get_data

example = False

data = get_data(example)


alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

total = 0

for idx, line in enumerate(data):
    if idx % 3 == 0:
        group1 = line

    if idx % 3 == 1:
        group2 = line

    if idx % 3 == 2:
        group3 = line

        shared = set(group1).intersection(group2).intersection(group3)

        assert len(shared) == 1

        shared = list(shared)[0]

        total += alphabet.index(shared) + 1

print(total)
