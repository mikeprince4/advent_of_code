from typing import Any
from dataclasses import dataclass
from helpers import get_data

example = False

data = get_data(example)


@dataclass
class Directory:
    parent_dir: Any
    name: str
    files: list
    directories: dict


def calc_total_size(directory):

    return sum(directory.files) + sum([calc_total_size(sub_dir) for sub_dir in directory.directories.values()])


# Create list for all directories
directories = []

# Create top directory and append to list
top_dir = Directory(None, "/", [], {})
directories.append(top_dir)

# Set current directory to top_dir
current_dir = top_dir

# Iterate through
for command in data:
    if command[0: 4] == '$ cd':
        next_dir = command.split(" ")[2]

        # Change directory
        if next_dir == '..':
            current_dir = current_dir.parent_dir
        elif next_dir == '/':
            current_dir = top_dir
        else:
            current_dir = current_dir.directories[next_dir]

    elif command[0: 4] == '$ ls':
        pass
    elif command[0: 3] == 'dir':
        name = command.split(" ")[1]

        # Add as subdirectory
        new_directory = Directory(current_dir, name, [], {})
        current_dir.directories[name] = new_directory

        # Add to list of all directories
        directories.append(new_directory)
    else:
        size = int(command.split(" ")[0])
        current_dir.files.append(size)


# Sum the sizes of those under 100000
tot_size = 0
for directory in directories:
    total_size = calc_total_size(directory)
    if total_size <= 100000:
        tot_size += total_size

# Print the size of those under 100000
print(tot_size)

# Print the entire systems size
print(calc_total_size(top_dir))


# Calculate the amount we need to free up
need_to_free = 30000000 - (70000000 - 42558312)
print(need_to_free)

# Find the single smallest directory that's large enough to free the necessary space
best = 10000000000
for directory in directories:
    this_dir_size = calc_total_size(directory)
    if this_dir_size >= need_to_free and this_dir_size <= best:
        best = this_dir_size


print(best)
