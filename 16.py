import re

from utils import get_input

text = get_input(day=16, year=2022, test=False)


cache = {}


def find_most_pressure(node, remaining_time, opened_valves):

    state = (node, remaining_time, tuple(sorted(opened_valves)))

    if state in cache:
        return cache[state]

    if remaining_time == 0:
        return 0

    result = 0
    if node in opened_valves:
        result = max(
            result,
            (
                find_most_pressure(node, remaining_time - 1, opened_valves - {node})
                + pressure[node] * (remaining_time - 1)
            ),
        )

    for next_node in neighbours[node]:
        result = max(
            result, find_most_pressure(next_node, remaining_time - 1, opened_valves)
        )

    cache[state] = result
    return result


pressure = {}
opened_valves = set()
neighbours = {}
for line in text.splitlines():
    print(line)
    node, value, last = re.search(
        'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line
    ).groups()
    pressure[node] = int(value)
    neighbours[node] = last.split(', ')

    if pressure[node] > 0:
        opened_valves.add(node)

print(find_most_pressure('AA', 30, opened_valves))
