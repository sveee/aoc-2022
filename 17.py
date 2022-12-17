from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle
from typing import Dict, List

from utils import get_input

jet_pattern = get_input(day=17, year=2022)


@dataclass
class Rock:
    points: List[List[int]]

    def to_tower(self):
        return {tuple(point) for point in self.points}

    def height(self):
        return max(point[1] for point in self.points)

    def move_left(self, tower):
        for point in self.points:
            if point[0] <= 0 or (point[0] - 1, point[1]) in tower:
                return False
        for point in self.points:
            point[0] -= 1
        return True

    def move_right(self, tower):
        for point in self.points:
            if point[0] >= 6 or (point[0] + 1, point[1]) in tower:
                return False
        for point in self.points:
            point[0] += 1
        return True

    def move_down(self, tower):
        for point in self.points:
            if point[1] < 1 or (point[0], point[1] - 1) in tower:
                return False

        for point in self.points:
            point[1] -= 1

        return True

    def move_to_height(self, height):
        min_height = min(point[1] for point in self.points)
        for point in self.points:
            point[1] += height - min_height

    def move_to_width(self, width):
        min_width = min(point[0] for point in self.points)
        for point in self.points:
            point[0] += width - min_width

    @staticmethod
    def from_str(s):
        lines = s.splitlines()

        return Rock(
            [
                [x, len(lines) - 1 - y]
                for x in range(len(lines[0]))
                for y in range(len(lines))
                if lines[y][x] == '#'
            ]
        )


@dataclass
class Pattern:
    base_n_rocks: int
    base_height: int
    n_rocks_increment: int
    height_increment: int
    delta: List[int]


@dataclass
class Match:
    n_rocks: int
    height: int


def print_tower(tower, rock):
    from itertools import chain

    height = max(rock.height(), max([point[1] for point in tower], default=0))
    grid = [['.'] * 7 for _ in range(height + 1)]
    for point in chain(tower, rock.points):
        grid[point[1]][point[0]] = '#'

    for line in grid[::-1]:
        print(''.join(line))
    print()


def find_match(height):
    row = height - 1
    for prev_row in range(row - 1, -1, -1):
        match = all(
            tower_by_row[row - k] == tower_by_row[prev_row - k] for k in range(20)
        )
        if match:
            return prev_row + 1


shapes = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##'''

rocks = [Rock.from_str(shape) for shape in shapes.split('\n\n')]

rock_index = 0
current_rock = deepcopy(rocks[0])
current_rock.move_to_height(3)
current_rock.move_to_width(2)
current_n_rocks = 0
tower = set()
tower_by_row = defaultdict(set)
height = -1

height_per_n_rocks = {}
prev_match = None
pattern = None
for instruction in cycle(jet_pattern):

    if instruction == '<':
        current_rock.move_left(tower)
    else:
        current_rock.move_right(tower)

    if not current_rock.move_down(tower):
        height = max(height, current_rock.height() + 1)
        tower.update(current_rock.to_tower())
        for point in current_rock.points:
            tower_by_row[point[1]].add(point[0])

        current_n_rocks += 1
        rock_index = (rock_index + 1) % len(rocks)
        current_rock = deepcopy(rocks[rock_index])
        current_rock.move_to_height(height + 3)
        current_rock.move_to_width(2)
        height_per_n_rocks[current_n_rocks] = height

        if not prev_match:
            if prev_height := find_match(height):
                prev_match = Match(current_n_rocks, height)
        elif not pattern:
            if (prev_height := find_match(height)) and prev_height == prev_match.height:
                pattern = Pattern(
                    base_n_rocks=prev_match.n_rocks,
                    base_height=prev_match.height,
                    n_rocks_increment=current_n_rocks - prev_match.n_rocks,
                    height_increment=height - prev_height,
                    delta=[
                        height_per_n_rocks[n_rocks] - prev_match.height
                        for n_rocks in range(prev_match.n_rocks, current_n_rocks + 1)
                    ],
                )

    if current_n_rocks == 10000:
        break


def get_tower_height(n_rocks):
    assert n_rocks >= pattern.base_n_rocks and pattern
    q = (n_rocks - pattern.base_n_rocks) // pattern.n_rocks_increment
    r = (n_rocks - pattern.base_n_rocks) % pattern.n_rocks_increment
    return pattern.base_height + pattern.height_increment * q + pattern.delta[r]


print(get_tower_height(2022))
print(get_tower_height(1_000_000_000_000))
