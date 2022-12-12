from collections import deque

from utils import get_input

text = get_input(day=12, year=2022)
heatmap = text.splitlines()
n, m = len(heatmap), len(heatmap[0])
directions = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def get_elevation(position):
    elevation = heatmap[position[0]][position[1]]
    return 'a' if elevation == 'S' else 'z' if elevation == 'E' else elevation


def can_climb(start, end):
    return ord(get_elevation(end)) - ord(get_elevation(start)) <= 1


def get_neighbours(position):
    neighbours = []
    for direction in directions:
        new_position = position[0] + direction[0], position[1] + direction[1]
        if (
            0 <= new_position[0] < n
            and 0 <= new_position[1] < m
            and can_climb(new_position, position)
        ):
            neighbours.append(new_position)
    return neighbours


e_position = next((x, y) for x in range(n) for y in range(m) if heatmap[x][y] == 'E')
s_position = next((x, y) for x in range(n) for y in range(m) if heatmap[x][y] == 'S')

queue = deque([e_position])
shortest_distance = {e_position: 0}
while len(queue) > 0:
    position = queue.popleft()
    for neighbour in get_neighbours(position):
        if not neighbour in shortest_distance:
            shortest_distance[neighbour] = shortest_distance[position] + 1
            queue.append(neighbour)

print(shortest_distance[s_position])
print(
    min(
        shortest_distance[(x, y)]
        for x in range(n)
        for y in range(m)
        if (x, y) in shortest_distance
        if get_elevation((x, y)) == 'a'
    )
)
