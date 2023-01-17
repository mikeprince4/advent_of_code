
from helpers import get_data

example = False

data = get_data(example)


contains = 0

for row in data:
    split = row.split(",")
    elf1 = split[0].split("-")
    elf2 = split[1].split("-")

    e10 = int(elf1[0])
    e11 = int(elf1[1])
    
    e20 = int(elf2[0])
    e21 = int(elf2[1])
    
    if (e10 <= e20 and e11 >= e20) or (e10 <= e21 and e11 >= e21):
        contains += 1
    
    elif (e20 <= e10 and e21 >= e10) or (e20 <= e11 and e21 >= e11):
        contains += 1
        

        
        
print(contains)