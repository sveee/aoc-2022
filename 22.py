import re

from utils import get_input

text = get_input(day=22, year=2022, test=False)
board_text, instructions_text = text.split('\n\n')


directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def get_board(text):
    board = list(map(list, text.splitlines()))
    max_row_lenth = max(map(len, board))
    for row in board:
        row.extend([' '] * (max_row_lenth - len(row)))
    return board


def get_value(position, board):
    return board[position[1]][position[0]]


def move(position, direction, steps, board):
    height = len(board)
    width = len(board[0])
    for _step in range(steps):
        next_position = (
            (position[0] + direction[0] + width) % width,
            (position[1] + direction[1] + height) % height,
        )
        while get_value(next_position, board) == ' ':
            next_position = (
                (next_position[0] + direction[0] + width) % width,
                (next_position[1] + direction[1] + height) % height,
            )
        if get_value(next_position, board) == '#':
            break
        position = next_position
    return position


def find_leftmost_open(board):
    for y, line in enumerate(board):
        for x, value in enumerate(line):
            if value == '.':
                return (x, y)
    raise ValueError('Open tile not found')


board = get_board(board_text)
instructions = re.findall('\d+|L|R', instructions_text)
direction_index = 0
position = find_leftmost_open(board)
for instruction in instructions:
    if instruction == 'R':
        direction_index = (direction_index + 1) % 4
    elif instruction == 'L':
        direction_index = (direction_index + 3) % 4
    else:
        steps = int(instruction)
        position = move(position, directions[direction_index], steps, board)
print(1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction_index)
