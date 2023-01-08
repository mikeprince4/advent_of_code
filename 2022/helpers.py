import sys


def get_data(example: bool):

    day_num = sys.argv[0].strip(".py").strip("day")

    suffix = "e" if example else ""

    return list(map(str.strip, open(f"data/day{day_num}{suffix}.txt").readlines()))
