from utils import get_input

text = get_input(day=9, year=2022)
directions = {
    'R': (0, 1),
    'U': (1, 0),
    'L': (0, -1),
    'D': (-1, 0),
}
motions = text.splitlines()


def move(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def follow(tail, head):
    diff = head[0] - tail[0], head[1] - tail[1]
    normalize = lambda x: (-1 if x < 0 else 1) * min(abs(x), 1)
    direction = (
        (0, 0)
        if abs(diff[0]) <= 1 and abs(diff[1]) <= 1  # are neighbours
        else (normalize(diff[0]), normalize(diff[1]))
    )
    return move(tail, direction)


def find_n_tail_visits(rope_length):
    rope = [(0, 0)] * rope_length
    tail_positions = set()
    for motion in motions:
        direction, times = motion.split()
        times = int(times)
        for _ in range(times):
            rope[0] = move(rope[0], directions[direction])
            for index in range(1, rope_length):
                rope[index] = follow(rope[index], rope[index - 1])
            tail_positions.add(rope[-1])
    return len(tail_positions)


print(find_n_tail_visits(2))
print(find_n_tail_visits(10))
