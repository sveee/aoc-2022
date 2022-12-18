from utils import get_input

text = get_input(day=18, year=2022)

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
        if all(-2 <= position[k] + direction[k] <= 21 for k in range(3))
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
for line in text.splitlines():
    droplet.add(tuple(map(int, line.split(','))))


air = find_air((20, 20, 20))
surface_area1 = 0
surface_area2 = 0
for posiiton in droplet:
    for neighbour in get_neighbours(posiiton):
        surface_area1 += neighbour not in droplet
        surface_area2 += neighbour in air

print(surface_area1)
print(surface_area2)
