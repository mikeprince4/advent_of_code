
example = False

if example:
    data = list(map(str.strip, open(f"data/day2e.txt").readlines()))
else:
    data = list(map(str.strip, open(f"data/day2.txt").readlines()))


score = 0

for line in data:
    if line == "A Y":
        score += 4
    elif line == "A X":
        score += 3
    elif line == "A Z":
        score += 8
    elif line == "B Y":
        score += 5
    elif line == "B X":
        score += 1
    elif line == "B Z":
        score += 9
    elif line == "C Y":
        score += 6
    elif line == "C X":
        score += 2
    elif line == "C Z":
        score += 7

print(score)
