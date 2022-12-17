import re
from dataclasses import dataclass
from itertools import chain, combinations
from typing import Set

from tqdm.auto import tqdm

from utils import get_input

text = get_input(day=16, year=2022)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_neighbours(node, opened_valves):
    return neighbours[node] + [node] if node in opened_valves else neighbours[node]


def find_most_pressure(node, remaining_time, opened_valves):
    state = (node, remaining_time, tuple(sorted(opened_valves)))
    if state in cache:
        return cache[state]
    if remaining_time == 0:
        return 0
    most_pressure = 0
    for next_node in get_neighbours(node, opened_valves):
        remove = {node} if next_node == node else set()
        remaining_pressure = (
            pressure[node] * (remaining_time - 1) if next_node == node else 0
        )
        most_pressure = max(
            most_pressure,
            find_most_pressure(next_node, remaining_time - 1, opened_valves - remove)
            + remaining_pressure,
        )

    cache[state] = most_pressure
    return most_pressure


pressure = {}
opened_valves = set()
neighbours = {}
cache = {}
for line in text.splitlines():
    node, value, last = re.search(
        'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line
    ).groups()
    pressure[node] = int(value)
    neighbours[node] = last.split(', ')

    if pressure[node] > 0:
        opened_valves.add(node)

# part 1
print(find_most_pressure('AA', 30, opened_valves))

# part 2
for subset in tqdm(list(powerset(opened_valves))):
    find_most_pressure('AA', 26, set(subset))
print(
    max(
        find_most_pressure('AA', 26, set(subset))
        + find_most_pressure('AA', 26, opened_valves - set(subset))
        for subset in powerset(opened_valves)
    )
)
