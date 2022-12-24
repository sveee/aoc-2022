from collections import deque
from typing import NamedTuple, Tuple

from utils import get_input

text = get_input(day=24, year=2022, test=False, test_index=6)
directions = {
    '>': (1, 0),
    '^': (0, -1),
    '<': (-1, 0),
    'v': (0, 1),
}


class State(NamedTuple):
    position: Tuple[int, int]
    time: int


class Blizzard(NamedTuple):
    position: Tuple[int, int]
    direction: Tuple[int, int]


class GridSize(NamedTuple):
    width: int
    height: int


def move(position, direction, grid_size):

    x = position[0] + direction[0]
    y = position[1] + direction[1]
    if x == 0:
        x = grid_size.width - 2
    elif x == grid_size.width - 1:
        x = 1

    if y == 0:
        y = grid_size.height - 2
    if y == grid_size.height - 1:
        y = 1

    return (x, y)


def calculate_blizzard_positions_at_time(blizzards, grid_size):
    start_blizzards = blizzards
    blizzard_positions_at_time = {0: {blizzard.position for blizzard in blizzards}}
    time = 0
    while True:
        time += 1
        blizzards = {
            Blizzard(
                move(blizzard.position, blizzard.direction, grid_size),
                blizzard.direction,
            )
            for blizzard in blizzards
        }
        if blizzards == start_blizzards:
            break
        blizzard_positions_at_time[time] = {blizzard.position for blizzard in blizzards}
    return blizzard_positions_at_time


def get_neighbors(position, grid_size):
    neighbors = set()
    start = (1, 0)
    end = (grid_size.width - 2, grid_size.height - 1)
    for direction in directions.values():
        new_position = (
            position[0] + direction[0],
            position[1] + direction[1],
        )
        if new_position not in [start, end] and (
            new_position[0] <= 0
            or new_position[0] >= grid_size.width - 1
            or new_position[1] <= 0
            or new_position[1] >= grid_size.height - 1
        ):
            continue
        neighbors.add(new_position)
    neighbors |= set([position])
    return neighbors


def get_initial_blizzards(grid):
    return {
        Blizzard((x, y), directions[value])
        for y, line in enumerate(grid)
        for x, value in enumerate(line)
        if value not in ['.', '#']
    }


def fewest_minutes(grid):
    grid_size = GridSize(len(grid[0]), len(grid))
    start = (1, 0)
    end = (grid_size.width - 2, grid_size.height - 1)
    initial_blizzards = get_initial_blizzards(grid)
    blizzards_at_time = calculate_blizzard_positions_at_time(
        initial_blizzards, grid_size
    )
    queue = deque([State(start, 0)])
    visited = set([State(start, 0)])
    while len(queue) != 0:
        state = queue.popleft()
        # print(state)
        # if state.time == 3:
        #     return
        if state.position == end:
            return state.time
        mod_time = (state.time + 1) % len(blizzards_at_time)
        blizzards = blizzards_at_time[mod_time]
        for neighbor in get_neighbors(state.position, grid_size):
            visit_state = State(neighbor, mod_time)
            if neighbor not in blizzards and visit_state not in visited:
                queue.append(State(neighbor, state.time + 1))
                visited.add(visit_state)


print(text)

grid = [list(line) for line in text.splitlines()]
print(fewest_minutes(grid))

# blizzards = get_initial_blizzards(grid)
# #
# grid_size = GridSize(len(grid[0]), len(grid))
# t = calculate_blizzard_positions_at_time(blizzards, grid_size)

# print(t)
# print(len(t))
# for key, value in t.items():
#     print(key, value)
