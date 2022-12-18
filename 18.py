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
        if all(min_pos <= position[k] + direction[k] <= max_pos for k in range(3))
    ]


def find_air(position):
    stack = [position]
    air = set()
    while len(stack) > 0:
        position = stack.pop()
        if position in air or position in droplet:
            continue
        air.add(position)
        for neighbour in get_neighbours(position):
            stack.append(neighbour)
    return air


droplet = set()
min_pos, max_pos = 10**10, 0
for line in text.splitlines():
    point = tuple(map(int, line.split(',')))
    max_pos = max(max_pos, max(point) + 1)
    min_pos = min(min_pos, min(point) - 1)
    droplet.add(tuple(map(int, line.split(','))))
air = find_air((min_pos, min_pos, min_pos))

area1, area2 = 0, 0
for posiiton in droplet:
    for neighbour in get_neighbours(posiiton):
        area1 += neighbour not in droplet
        area2 += neighbour in air
print(area1)
print(area2)
