import re
from dataclasses import dataclass

from utils import get_input

text = get_input(day=22, year=2022)
board_text, instructions_text = text.split('\n\n')


directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


@dataclass
class CubeEdge:
    column: int
    row: int
    direction: int
    reverse: bool = False


def get_board(text):
    board = list(map(list, text.splitlines()))
    max_row_lenth = max(map(len, board))
    for row in board:
        row.extend([' '] * (max_row_lenth - len(row)))
    return board


def get_value(position, board):
    return board[position[1]][position[0]]


def move(position, direction, steps, board, warping):
    height = len(board)
    width = len(board[0])
    for _step in range(steps):
        next_position = (
            position[0] + directions[direction][0],
            position[1] + directions[direction][1],
        )
        next_direction = direction
        if (
            next_position[0] < 0
            or next_position[0] >= width
            or next_position[1] < 0
            or next_position[1] >= height
            or get_value(next_position, board) == ' '
        ):
            next_position, next_direction = warping[position, direction]

        if get_value(next_position, board) == '#':
            break
        position = next_position
        direction = next_direction
    return position, direction


def calculate_flat_warping():
    height = len(board)
    width = len(board[0])
    flat_warping = {}
    for y in range(height):
        for x in range(width):
            position = (x, y)
            for direction in range(4):
                next_position = (
                    (position[0] + directions[direction][0] + width) % width,
                    (position[1] + directions[direction][1] + height) % height,
                )
                while get_value(next_position, board) == ' ':
                    next_position = (
                        (next_position[0] + directions[direction][0] + width) % width,
                        (next_position[1] + directions[direction][1] + height) % height,
                    )
                flat_warping[position, direction] = next_position, direction
    return flat_warping


def get_points_from_edge(edge, size):
    if edge.direction == 3:
        points = [
            (x, edge.row * size)
            for x in range(edge.column * size, (edge.column + 1) * size)
        ]
    elif edge.direction == 1:
        points = [
            (x, (edge.row + 1) * size - 1)
            for x in range(edge.column * size, (edge.column + 1) * size)
        ]
    elif edge.direction == 2:
        points = [
            (edge.column * size, y)
            for y in range(edge.row * size, (edge.row + 1) * size)
        ]
    elif edge.direction == 0:
        points = [
            ((edge.column + 1) * size - 1, y)
            for y in range(edge.row * size, (edge.row + 1) * size)
        ]
    if edge.reverse:
        points = points[::-1]
    return points


def calculate_cube_warping():
    neighboring_edges = [
        # side 0
        (CubeEdge(1, 0, 0), CubeEdge(2, 0, 2)),
        (CubeEdge(1, 0, 1), CubeEdge(1, 1, 3)),
        (CubeEdge(1, 0, 2), CubeEdge(0, 2, 2, True)),
        (CubeEdge(1, 0, 3), CubeEdge(0, 3, 2)),
        # side 1
        (CubeEdge(2, 0, 0), CubeEdge(1, 2, 0, True)),
        (CubeEdge(2, 0, 1), CubeEdge(1, 1, 0)),
        (CubeEdge(2, 0, 2), CubeEdge(1, 0, 0)),
        (CubeEdge(2, 0, 3), CubeEdge(0, 3, 1)),
        # side 2
        (CubeEdge(1, 1, 0), CubeEdge(2, 0, 1)),
        (CubeEdge(1, 1, 1), CubeEdge(1, 2, 3)),
        (CubeEdge(1, 1, 2), CubeEdge(0, 2, 3)),
        (CubeEdge(1, 1, 3), CubeEdge(1, 0, 1)),
        # side 3
        (CubeEdge(0, 2, 0), CubeEdge(1, 2, 2)),
        (CubeEdge(0, 2, 1), CubeEdge(0, 3, 3)),
        (CubeEdge(0, 2, 2), CubeEdge(1, 0, 2, True)),
        (CubeEdge(0, 2, 3), CubeEdge(1, 1, 2)),
        # side 4
        (CubeEdge(1, 2, 0), CubeEdge(2, 0, 0, True)),
        (CubeEdge(1, 2, 1), CubeEdge(0, 3, 0)),
        (CubeEdge(1, 2, 2), CubeEdge(0, 2, 0)),
        (CubeEdge(1, 2, 3), CubeEdge(1, 1, 1)),
        # side 5
        (CubeEdge(0, 3, 0), CubeEdge(1, 2, 1)),
        (CubeEdge(0, 3, 1), CubeEdge(2, 0, 3)),
        (CubeEdge(0, 3, 2), CubeEdge(1, 0, 3)),
        (CubeEdge(0, 3, 3), CubeEdge(0, 2, 1)),
    ]
    cube_warping = {}
    for edge1, edge2 in neighboring_edges:
        points1 = get_points_from_edge(edge1, 50)
        points2 = get_points_from_edge(edge2, 50)
        for point1, point2 in zip(points1, points2):
            cube_warping[point1, edge1.direction] = point2, (edge2.direction + 2) % 4
    return cube_warping


def find_leftmost_open(board):
    for y, line in enumerate(board):
        for x, value in enumerate(line):
            if value == '.':
                return (x, y)
    raise ValueError('Open tile not found')


def calculate_password(board, instructions, warping):
    direction_index = 0
    position = find_leftmost_open(board)
    for instruction in instructions:
        if instruction == 'R':
            direction_index = (direction_index + 1) % 4
        elif instruction == 'L':
            direction_index = (direction_index + 3) % 4
        else:
            steps = int(instruction)
            position, direction_index = move(
                position, direction_index, steps, board, warping
            )
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction_index


board = get_board(board_text)
instructions = re.findall('\d+|L|R', instructions_text)
flat_warping = calculate_flat_warping()
cube_warping = calculate_cube_warping()


print(calculate_password(board, instructions, flat_warping))
print(calculate_password(board, instructions, cube_warping))
