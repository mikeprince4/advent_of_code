
from helpers import get_data

example = False

data = get_data(example)

s = {}

s[1] = list("MJCBFRLH")
s[2] = list("ZCD")
s[3] = list("HJFCNGW")
s[4] = list("PJDMTSB")
s[5] = list("NCDRJ")
s[6] = list("WLDQPJGZ")
s[7] = list("PZTFRH")
s[8] = list("LVMG")
s[9] = list("CBGPFQRJ")

for step in data:
    splitted = step.split(" ")
    num = int(splitted[1])
    fr = int(splitted[3])
    to = int(splitted[5])

    # print(f"moving {num} from {fr} to {to}")
    i = 0
    temp = []
    while i < num:
        temp.append(s[fr].pop())
        i += 1

    # print(temp)
    i = 0
    while i < num:
        s[to].append(temp.pop())
        i += 1

    # print(s)


string = ""

for key, val in s.items():
    string += val[-1]
    print(key)

print(string)
