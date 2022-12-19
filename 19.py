import re
from collections import defaultdict
from copy import copy

from utils import get_input

text = get_input(day=19, year=2022, test=False)
text = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''
print(text)


def subtract(left, right):
    return tuple(left[i] - right[i] for i in range(len(left)))


def add(left, right):
    return tuple(left[i] + right[i] for i in range(len(left)))


def multiply(left, right):
    return tuple(left * right[i] for i in range(len(right)))


def quotient(left, right):
    return min(left[i] // right[i] for i in range(len(left)) if right[i] > 0)


def find_max_n_geodes(time, n_resources, n_robots, robot_costs, best_geodes):

    if time in best_geodes and n_resources[-1] < best_geodes[time]:
        print(best_geodes)
        return 0

    if time == MAX_TIME + 1:
        return n_resources[-1]

    new_n_resources = copy(n_resources)
    for robot_index, n_robots_per_resource in enumerate(n_robots):
        new_n_resources = add(
            new_n_resources, multiply(n_robots_per_resource, eye[robot_index])
        )

    max_n_geodes = 0
    for robot_index, robot_cost in reversed(list(enumerate(robot_costs))):
        max_n_can_buy = quotient(n_resources, robot_cost)
        if max_n_can_buy > 0:
            max_n_geodes = max(
                max_n_geodes,
                find_max_n_geodes(
                    time + 1,
                    subtract(new_n_resources, robot_cost),
                    add(n_robots, eye[robot_index]),
                    robot_costs,
                    best_geodes,
                ),
            )

    max_n_geodes = max(
        max_n_geodes,
        find_max_n_geodes(
            time + 1, new_n_resources, n_robots, robot_costs, best_geodes
        ),
    )
    best_geodes[time] = max(best_geodes[time], n_resources[-1])
    return max_n_geodes


def construct_blueprint(line):
    (
        blueprint_id,
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
    return blueprint_id, [
        (ore_for_ore, 0, 0, 0),
        (clay_for_ore, 0, 0, 0),
        (obsidian_for_ore, obsidian_for_clay, 0, 0),
        (geode_for_ore, 0, geode_for_obsidian, 0),
    ]


MAX_TIME = 24
eye = [tuple(1 if i == j else 0 for j in range(4)) for i in range(4)]
blueprints = {}
for line in text.splitlines():
    blueprint_id, robot_costs = construct_blueprint(line)
    blueprints[blueprint_id] = robot_costs


print(blueprints[1])

cache = defaultdict(int)
# 25 (6, 41, 8, 9) (1, 4, 2, 2)
# print(find_max_n_geodes(24, (5, 37, 6, 7), (1, 4, 2, 2), blueprints[1], cache))
# print(find_max_n_geodes(23, (4, 33, 4, 5), (1, 4, 2, 2), blueprints[1], {}))
# print(find_max_n_geodes(22, (3, 29, 2, 3), (1, 4, 2, 2), blueprints[1], {}))
# print(find_max_n_geodes(21, (4, 25, 7, 2), (1, 4, 2, 1), blueprints[1], {}))
# print(find_max_n_geodes(20, (3, 21, 5, 1), (1, 4, 2, 1), blueprints[1], {}))
# print(find_max_n_geodes(19, (2, 17, 3, 0), (1, 4, 2, 1), blueprints[1], {}))
# print(find_max_n_geodes(18, (3, 13, 8, 0), (1, 4, 2, 0), blueprints[1], {}))
# print(find_max_n_geodes(17, (2, 9, 6, 0), (1, 4, 2, 0), blueprints[1], {}))
# print(find_max_n_geodes(16, (1, 5, 4, 0), (1, 4, 2, 0), blueprints[1], {}))
# print(find_max_n_geodes(13, (1, 7, 1, 0), (1, 4, 1, 0), blueprints[1], cache))
# print(find_max_n_geodes(10, (3, 12, 0, 0), (1, 3, 0, 0), blueprints[1], cache))

# print(find_max_n_geodes(5, (2, 1, 0, 0), (1, 1, 0, 0), blueprints[1], cache))

print(find_max_n_geodes(1, (0, 0, 0, 0), (1, 0, 0, 0), blueprints[2], cache))
# print(len(cache))
