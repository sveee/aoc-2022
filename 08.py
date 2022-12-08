from functools import reduce

from utils import get_input

text = get_input(day=8, year=2022)


def move(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def is_valid(position):
    return 0 <= position[0] < n and 0 <= position[1] < n


def value_at(position):
    return grid[position[0]][position[1]]


def is_visible_from(position, direction):
    current_position = move(position, direction)
    while is_valid(current_position):
        if value_at(current_position) >= value_at(position):
            return False
        current_position = move(current_position, direction)
    return True


def is_visible(position):
    return any(is_visible_from(position, diretion) for diretion in directions)


def viewing_distance(position, direction):
    current_position = move(position, direction)
    viewing_distance = 0
    while is_valid(current_position):
        if value_at(current_position) >= value_at(position):
            viewing_distance += 1
            break
        viewing_distance += 1
        current_position = move(current_position, direction)
    return viewing_distance


def scenec_score(posiiton):
    return reduce(
        lambda x, y: x * y,
        (viewing_distance(posiiton, direction) for direction in directions),
    )


directions = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]
grid = text.split()
n = len(grid)
print(sum(is_visible((x, y)) for x in range(n) for y in range(n)))
print(max(scenec_score((x, y)) for x in range(n) for y in range(n)))
