import pandas as pd
from dataclasses import dataclass
from typing import Set, Any

data = list(pd.read_csv("data/aoc - day21.csv").dummy)
#data = list(pd.read_csv("data/aoc - day21e.csv").dummy)

print(data[-1])


@dataclass
class Monkey:
    name: str
    number: float
    prev_monkey_1: Any
    operation: str
    prev_monkey_2: Any

    def __hash__(self):
        return hash(self.name)

    def get_number(self):
        if self.number:
            return self.number
        else:
            if self.operation == "+":
                return monkeys[self.prev_monkey_1].get_number() + monkeys[self.prev_monkey_2].get_number()
            elif self.operation == "*":
                return monkeys[self.prev_monkey_1].get_number() * monkeys[self.prev_monkey_2].get_number()
            elif self.operation == "/":
                return monkeys[self.prev_monkey_1].get_number() / monkeys[self.prev_monkey_2].get_number()
            elif self.operation == "-":
                return monkeys[self.prev_monkey_1].get_number() - monkeys[self.prev_monkey_2].get_number()
            else:
                print(f"operation = {self.operation}")
                quit()

    def is_match(self):

        num_1 = monkeys[self.prev_monkey_1].get_number()
        num_2 = monkeys[self.prev_monkey_2].get_number()
        print(f"num_1 = {num_1}; num_2 = {num_2}")

        return num_1, num_2


monkeys = {}
for row in data:
    splt = row.split()

    name = splt[0].replace(":", "")

    if len(splt) == 2:
        monkeys[name] = Monkey(name, int(splt[1]), None, None, None)
    else:
        monkeys[name] = Monkey(name, None, splt[1], splt[2], splt[3])

lb = 0
ub = 276156919469632


while True:
    my_num = (lb + ub) // 2

    monkeys["humn"].number = my_num

    num_1, num_2 = monkeys["root"].is_match()

    if num_1 == num_2:
        print(f"Winning my_num ={my_num}")
        break
    elif num_1 < num_2:
        ub = my_num
    else:
        lb = my_num
