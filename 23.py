from collections import Counter

from utils import get_input

text = get_input(day=23, year=2022)

directions = [
    [(-1, -1), (0, -1), (1, -1)],  # north
    [(-1, 1), (0, 1), (1, 1)],  # south
    [(-1, -1), (-1, 0), (-1, 1)],  # west
    [(1, -1), (1, 0), (1, 1)],  # east
]
all_directions = {
    direction for direction_set in directions for direction in direction_set
}


def move(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def has_no_neighbours(elf, elves):
    return all(move(elf, direction) not in elves for direction in all_directions)


def first_available_direction(elf, direction_index, elves):
    for index in [(direction_index + index) % 4 for index in range(4)]:
        are_neighbors_free = all(
            move(elf, direction) not in elves for direction in directions[index]
        )
        if are_neighbors_free:
            return directions[index][1]


def do_round(elves, direction_index):
    proposed_moves = {}
    for elf in elves:
        if has_no_neighbours(elf, elves):
            proposed_moves[elf] = elf
        else:
            direction = first_available_direction(elf, direction_index, elves)
            proposed_moves[elf] = move(elf, direction) if direction else elf

    counter = Counter(proposed_moves.values())
    for elf in proposed_moves:
        if counter[proposed_moves[elf]] > 1:
            proposed_moves[elf] = elf

    next_elves = set(proposed_moves.values())
    next_direction_index = (direction_index + 1) % 4
    return next_elves, next_direction_index


def calculate_empty_tiles(elves):
    min_x = min(elf[0] for elf in elves)
    min_y = min(elf[1] for elf in elves)
    max_x = max(elf[0] for elf in elves)
    max_y = max(elf[1] for elf in elves)
    area = (max_x - min_x + 1) * (max_y - min_y + 1)
    return area - len(elves)


elves = {
    (x, y)
    for y, line in enumerate(text.splitlines())
    for x, value in enumerate(line)
    if value == '#'
}
direction_index = 0

round = 1
for round in range(1, 10000):
    next_elves, direction_index = do_round(elves, direction_index)
    if elves == next_elves:
        break
    elves = next_elves
    if round == 10:
        print(calculate_empty_tiles(elves))
print(round)
