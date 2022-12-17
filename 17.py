from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle
from typing import List

from utils import get_input

jet_pattern = get_input(day=17, year=2022, test=False, test_index=1)


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


def print_tower(tower, rock):
    from itertools import chain

    grid = [['.'] * 7 for _ in range(rock.height() + 1)]
    for point in chain(tower, rock.points):
        grid[point[1]][point[0]] = '#'

    for line in grid[::-1]:
        print(''.join(line))
    print()


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
n_rocks = 0
tower = set()
tower_height = 0
for instruction in cycle(jet_pattern):

    if instruction == '<':
        current_rock.move_left(tower)
    else:
        current_rock.move_right(tower)

    if not current_rock.move_down(tower):
        tower_height = max(tower_height, current_rock.height())
        tower.update(current_rock.to_tower())
        rock_index = (rock_index + 1) % len(rocks)
        n_rocks += 1

        current_rock = deepcopy(rocks[rock_index])
        current_rock.move_to_height(tower_height + 4)
        current_rock.move_to_width(2)

    if n_rocks == 2022:
        print(tower_height + 1)
        break
