from copy import deepcopy

from utils import get_input

directions = [
    (0, 1),
    (-1, 1),
    (1, 1),
]


def get_line(start, end):
    start_x, end_x = sorted([start[0], end[0]])
    start_y, end_y = sorted([start[1], end[1]])
    return [
        (x, y) for x in range(start_x, end_x + 1) for y in range(start_y, end_y + 1)
    ]


def initialize_cave():
    cave = set()
    for line in text.splitlines():
        points = list(map(lambda x: tuple(map(int, x.split(','))), line.split(' -> ')))
        for index in range(len(points) - 1):
            cave.update(get_line(points[index], points[index + 1]))
    return cave


def fill_cave(position, cave, max_y):
    if position[1] == INF:
        return True
    for direction in directions:
        next_position = position[0] + direction[0], position[1] + direction[1]
        if (
            next_position[1] < max_y
            and next_position not in cave
            and fill_cave(next_position, cave, max_y)
        ):
            return True
    cave.add(position)
    return False


text = get_input(day=14, year=2022)
cave = initialize_cave()
max_y = max(y for x, y in cave)
INF = max_y + 100
for max_y in [INF + 1, max_y + 2]:
    new_cave = deepcopy(cave)
    fill_cave((500, 0), new_cave, max_y)
    print(len(new_cave) - len(cave))
