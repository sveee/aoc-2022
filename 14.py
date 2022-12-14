from copy import deepcopy

from utils import get_input

text = get_input(day=14, year=2022)
INF = 10**8


def get_line(start, end):
    start_x, end_x = sorted([start[0], end[0]])
    start_y, end_y = sorted([start[1], end[1]])
    return [
        (x, y) for x in range(start_x, end_x + 1) for y in range(start_y, end_y + 1)
    ]


def fill_cave(position, cave, max_y):
    lowest_y = min(
        [y for x, y in cave if x == position[0] and y >= position[1]], default=max_y
    )
    if lowest_y == INF:
        return True
    lowest_position = position[0], lowest_y - 1
    left = (lowest_position[0] - 1, lowest_position[1] + 1)
    right = (lowest_position[0] + 1, lowest_position[1] + 1)
    if left[1] < max_y and left not in cave and fill_cave(left, cave, max_y):
        return True
    if right[1] < max_y and right not in cave and fill_cave(right, cave, max_y):
        return True
    cave.add(lowest_position)
    for y in range(position[1], lowest_position[1]):
        if fill_cave((position[0], y), cave, max_y):
            return True

    return False


cave = set()
for line in text.splitlines():
    points = list(map(lambda x: tuple(map(int, x.split(','))), line.split(' -> ')))

    for index in range(len(points) - 1):
        cave.update(get_line(points[index], points[index + 1]))

for max_y in [INF, max(y for x, y in cave) + 2]:
    new_cave = deepcopy(cave)
    fill_cave((500, 0), new_cave, max_y)
    print(len(new_cave) - len(cave))
