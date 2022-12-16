import re
from itertools import product

from utils import get_input

text = get_input(day=16, year=2022, test=False)


cache = {}


def get_neighbours(node, opened_valves):
    return neighbours[node] + [node] if node in opened_valves else neighbours[node]


def find_most_pressure1(node, remaining_time, opened_valves):

    state = (node, remaining_time, tuple(sorted(opened_valves)))

    if state in cache:
        return cache[state]

    if remaining_time == 0:
        return 0

    result = 0
    for next_node in get_neighbours(node, opened_valves):
        remove = {node} if next_node == node else set()
        remaining_pressure = (
            pressure[node] * (remaining_time - 1) if next_node == node else 0
        )
        result = max(
            result,
            find_most_pressure1(next_node, remaining_time - 1, opened_valves - remove)
            + remaining_pressure,
        )

    cache[state] = result
    return result


def find_most_pressure2(nodes, remaining_time, opened_valves):

    state = (nodes, remaining_time, tuple(sorted(opened_valves)))

    if state in cache:
        return cache[state]

    if remaining_time == 0:
        return 0

    result = 0
    for next_node0, next_node1 in product(
        get_neighbours(nodes[0], opened_valves), get_neighbours(nodes[1], opened_valves)
    ):
        if next_node0 == nodes[0] and next_node1 == nodes[1] and nodes[0] == nodes[1]:
            continue
        remove = set()
        remaining_pressure = 0
        if next_node0 == nodes[0]:
            remaining_pressure += pressure[nodes[0]] * (remaining_time - 1)
            remove.add(next_node0)
        if next_node1 == nodes[1]:
            remaining_pressure += pressure[nodes[1]] * (remaining_time - 1)
            remove.add(next_node1)

        result = max(
            result,
            find_most_pressure2(
                (next_node0, next_node1),
                remaining_time - 1,
                opened_valves - remove,
            )
            + remaining_pressure,
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

# print(find_most_pressure(('AA', 'AA'), 30, opened_valves))
# print(find_most_pressure1('AA', 30, opened_valves))
print(find_most_pressure2(('AA', 'AA'), 26, opened_valves))
