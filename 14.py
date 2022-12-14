from copy import deepcopy

from utils import get_input

text = get_input(day=14, year=2022)


def get_line(start, end):
    start_x, end_x = sorted([start[0], end[0]])
    start_y, end_y = sorted([start[1], end[1]])
    return [
        (x, y) for x in range(start_x, end_x + 1) for y in range(start_y, end_y + 1)
    ]


def fill_cave(position, cave, max_y):
    if position[1] == INF:
        return True
    down = (position[0], position[1] + 1)
    if down[1] < max_y and down not in cave and fill_cave(down, cave, max_y):
        return True
    left = (position[0] - 1, position[1] + 1)
    if left[1] < max_y and left not in cave and fill_cave(left, cave, max_y):
        return True
    right = (position[0] + 1, position[1] + 1)
    if right[1] < max_y and right not in cave and fill_cave(right, cave, max_y):
        return True
    cave.add(position)
    return False


cave = set()
for line in text.splitlines():
    points = list(map(lambda x: tuple(map(int, x.split(','))), line.split(' -> ')))
    for index in range(len(points) - 1):
        cave.update(get_line(points[index], points[index + 1]))

INF = max(y for x, y in cave) + 3
for max_y in [INF + 1, max(y for x, y in cave) + 2]:
    new_cave = deepcopy(cave)
    fill_cave((500, 0), new_cave, max_y)
    print(len(new_cave) - len(cave))
