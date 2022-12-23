import re
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from functools import reduce
from typing import List, Set

from tqdm import tqdm

from utils import get_input

text = get_input(day=19, year=2022)


def construct_blueprint(line):
    (
        _blueprint_id,
        ore_for_ore,
        clay_for_ore,
        obsidian_for_ore,
        obsidian_for_clay,
        geode_for_ore,
        geode_for_obsidian,
    ) = map(
        int,
        re.search(
            'Blueprint (\d+): Each ore robot costs (\d+) ore. '
            'Each clay robot costs (\d+) ore. '
            'Each obsidian robot costs (\d+) ore and (\d+) clay. '
            'Each geode robot costs (\d+) ore and (\d+) obsidian.',
            line,
        ).groups(),
    )
    return [
        (0, 0, 0, 0),
        (ore_for_ore, 0, 0, 0),
        (clay_for_ore, 0, 0, 0),
        (obsidian_for_ore, obsidian_for_clay, 0, 0),
        (geode_for_ore, 0, geode_for_obsidian, 0),
    ]


def subtract(left, right):
    return tuple(left[i] - right[i] for i in range(len(left)))


def add(left, right):
    return tuple(left[i] + right[i] for i in range(len(left)))


def multiply(left, right):
    return tuple(left * right[i] for i in range(len(right)))


def can_buy(left, right):
    return all(left[i] >= right[i] for i in range(len(left)))


@dataclass
class SearchParameters:
    robot_costs: List[int]
    max_time: List[int]
    max_robots: List[int]
    greedy_nodes: Set[int]


def find_max_geodes(time, resources, robots, parameters, cache):

    state = (time, resources, robots)
    if state in cache:
        return cache[state]

    if time == parameters.max_time + 1:
        return resources[-1]

    new_resources = copy(resources)
    for robot_index, n_robots_per_resource in enumerate(robots):
        new_resources = add(
            new_resources,
            multiply(n_robots_per_resource, robot_increments[robot_index + 1]),
        )

    max_geodes = 0
    for robot_index in reversed(range(5)):
        if (
            robot_index > 0
            and parameters.max_robots[robot_index - 1] == robots[robot_index - 1]
        ):
            continue
        robot_cost = parameters.robot_costs[robot_index]
        if can_buy(resources, robot_cost) > 0:
            max_geodes = max(
                max_geodes,
                find_max_geodes(
                    time + 1,
                    subtract(new_resources, robot_cost),
                    add(robots, robot_increments[robot_index]),
                    parameters,
                    cache,
                ),
            )
            if robot_index in parameters.greedy_nodes:
                break
    cache[state] = max_geodes
    return max_geodes


robot_increments = [[0] * 4] + [
    tuple(1 if i == j else 0 for j in range(4)) for i in range(4)
]
blueprints = [construct_blueprint(line) for line in text.splitlines()]


def calculate_max_geodes(blueprints, max_time, greedy_nodes):
    max_geodes = []
    for blueprint in tqdm(blueprints):
        max_robots = list(map(max, zip(*blueprint)))
        max_robots[-1] = 10**10
        search_parameters = SearchParameters(
            blueprint, max_time, max_robots, greedy_nodes
        )
        max_geodes.append(
            find_max_geodes(1, (0, 0, 0, 0), (1, 0, 0, 0), search_parameters, {})
        )
        print(max_geodes)
    return max_geodes


max_geodes1 = calculate_max_geodes(blueprints, 24, {})
print(
    sum(
        blueprint_index * n_geodes
        for blueprint_index, n_geodes in enumerate(max_geodes1, start=1)
    )
)
max_geodes2 = calculate_max_geodes(blueprints[:3], 32, {4, 3})
print(reduce(lambda x, y: x * y, max_geodes2))
