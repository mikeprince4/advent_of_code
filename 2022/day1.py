
example = False

if example:
    data = list(open(f"data/day1e.txt").readlines())
else:
    data = list(open(f"data/day1.txt").readlines())

d = {}
d[0] = []

for line in data:
    if line == "\n":
        d[len(d)] = []
    else:
        d[len(d)-1].append(int(line))


sums = {}

for key, lst in d.items():
    sums[key] = sum(lst)


print(f"max = {max(sums.values())}")


lst = list(sums.values())
lst.sort(reverse=True)

print(f"top 3 = {sum(lst[0:3])}")
