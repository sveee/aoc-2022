from collections import deque
from functools import partial
from multiprocessing import Pool
from typing import NamedTuple, Tuple

from tqdm import tqdm

from utils import get_input

text = get_input(day=24, year=2022, test=True, test_index=6)
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


def fewest_minutes(start_time, start, end, grid_size, blizzards_at_time):
    queue = deque([State(start, start_time)])
    visited = set([State(start, start_time)])
    while len(queue) != 0:
        state = queue.popleft()
        if state.position == end:
            return start_time, state.time - start_time
        mod_time = (state.time + 1) % len(blizzards_at_time)
        blizzards = blizzards_at_time[mod_time]
        for neighbor in get_neighbors(state.position, grid_size):
            visit_state = State(neighbor, mod_time)
            if neighbor not in blizzards and visit_state not in visited:
                queue.append(State(neighbor, state.time + 1))
                visited.add(visit_state)


grid = [list(line) for line in text.splitlines()]
grid_size = GridSize(len(grid[0]), len(grid))
position1 = (1, 0)
position2 = (grid_size.width - 2, grid_size.height - 1)

initial_blizzards = get_initial_blizzards(grid)
blizzards_at_time = calculate_blizzard_positions_at_time(initial_blizzards, grid_size)
cycle_size = len(blizzards_at_time)

forward_search = partial(
    fewest_minutes,
    start=position1,
    end=position2,
    grid_size=grid_size,
    blizzards_at_time=blizzards_at_time,
)
backward_search = partial(
    fewest_minutes,
    start=position2,
    end=position1,
    grid_size=grid_size,
    blizzards_at_time=blizzards_at_time,
)
with Pool() as pool:
    start_to_end_min_times = dict(
        result
        for result in tqdm(
            pool.imap(forward_search, range(cycle_size)), total=cycle_size
        )
    )
    end_to_start_min_times = dict(
        result
        for result in tqdm(
            pool.imap(backward_search, range(cycle_size)), total=cycle_size
        )
    )


print(
    min(
        start_time + time_to_travel
        for start_time, time_to_travel in start_to_end_min_times.items()
    )
)
best_overall_time = 10**10
for start_delay1 in range(cycle_size):
    for end_delay in range(cycle_size):
        for start_delay2 in range(cycle_size):
            first_end_visit_time = start_delay1 + start_to_end_min_times[start_delay1]
            second_start_visit_time = (
                first_end_visit_time
                + end_delay
                + end_to_start_min_times[
                    (first_end_visit_time + end_delay) % cycle_size
                ]
            )
            second_end_visit_time = (
                second_start_visit_time
                + start_delay2
                + start_to_end_min_times[
                    (second_start_visit_time + start_delay2) % cycle_size
                ]
            )
            best_overall_time = min(best_overall_time, second_end_visit_time)
print(best_overall_time)
