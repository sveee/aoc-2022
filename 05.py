import re
from copy import deepcopy

from utils import get_input

text = get_input(day=5, year=2022)

stacks, moves = text.split('\n\n')
stack_lines = stacks.splitlines()
stacks = [[] for _ in range(len([c for c in stack_lines[-1] if c != ' ']))]

for index in range(len(stack_lines) - 2, -1, -1):
    line = stack_lines[index]
    for number, value in zip(stack_lines[-1], line):
        if value.isalpha():
            stacks[int(number) - 1].append(value)


def do_move(stacks, count, from_index, to_index, reverse):
    stacks[to_index].extend(
        reversed(stacks[from_index][-count:])
        if reverse
        else stacks[from_index][-count:]
    )
    stacks[from_index] = stacks[from_index][:-count]


stacks1 = deepcopy(stacks)
stacks2 = deepcopy(stacks)
for move in moves.splitlines():
    count, from_index, to_index = map(int, re.findall('\d+', move))
    from_index -= 1
    to_index -= 1
    do_move(stacks1, count, from_index, to_index, reverse=True)
    do_move(stacks2, count, from_index, to_index, reverse=False)

print(''.join(stack[-1] for stack in stacks1))
print(''.join(stack[-1] for stack in stacks2))
