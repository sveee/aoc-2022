from collections import Counter, defaultdict
from itertools import combinations

from utils import get_input

text = get_input(day=18, year=2022, test=False)

directions = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


def get_neighbours(position):
    return [
        tuple((position[k] + direction[k] for k in range(3)))
        for direction in directions
    ]


cube_positions = set()
for line in text.splitlines():
    cube_positions.add(tuple(map(int, line.split(','))))

area = 0
for posiiton in cube_positions:
    for neighbour in get_neighbours(posiiton):
        area += neighbour not in cube_positions

print(area)
