from copy import deepcopy
from functools import reduce

from utils import get_input

text = get_input(day=11, year=2022)
worry_levels = []
update_level = []
divisors = []
true_monkeys = []
false_monkeys = []
for monkey_block in text.split('\n\n'):
    _, items, operation, division, true_case, false_case = monkey_block.splitlines()
    worry_levels.append(
        list(
            map(
                lambda x: int(x.strip()),
                items[len('  Starting items:') :].strip().split(','),
            )
        )
    )
    update_level.append(eval(f'lambda old: ' + operation[len('  Operation: new =') :]))
    divisors.append(int(division.split()[-1]))
    true_monkeys.append(int(true_case.split()[-1]))
    false_monkeys.append(int(false_case.split()[-1]))


def play_rounds(n_rounds, relief):
    current_worry_levels = deepcopy(worry_levels)
    n_inspected = [0] * len(worry_levels)
    mod = reduce(lambda x, y: x * y, divisors)
    for _round in range(n_rounds):
        for monkey in range(len(current_worry_levels)):
            n_inspected[monkey] += len(current_worry_levels[monkey])
            for worry_level in current_worry_levels[monkey]:
                new_worry_level = update_level[monkey](worry_level)
                if relief:
                    new_worry_level //= 3
                else:
                    new_worry_level %= mod
                new_monkey = (
                    true_monkeys[monkey]
                    if new_worry_level % divisors[monkey] == 0
                    else false_monkeys[monkey]
                )
                current_worry_levels[new_monkey].append(new_worry_level)
            current_worry_levels[monkey] = []
    n_inspected = sorted(n_inspected)
    return n_inspected[-2] * n_inspected[-1]


print(play_rounds(20, True))
print(play_rounds(10000, False))
