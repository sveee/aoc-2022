import re

from utils import get_input

text = get_input(day=15, year=2022)


def get_impossible_range(s, b, y):
    m = abs(s[0] - b[0]) + abs(s[1] - b[1])
    rx, ry = (s[0] - m + abs(s[1] - y), s[0] + m - abs(s[1] - y))
    if ry >= rx:
        return rx, ry
    return None


def do_intersect(left, right):
    return not (left[1] + 1 < right[0] or right[1] + 1 < left[0])


def get_impossible_ranges(y):
    range_set = [
        r
        for sensor, beacon in sensor_and_beacons
        if (r := get_impossible_range(sensor, beacon, y))
    ]
    return union(range_set)


def union(range_set):
    range_set = sorted(range_set)
    left = range_set[0]
    result = []
    for right in range_set[1:]:
        if not do_intersect(left, right):
            result.append(left)
            left = right
        else:
            left = min(left[0], right[0]), max(left[1], right[1])
    result.append(left)
    return result


y = 2000000
max_y = 4000000
sensor_and_beacons = []
for line in text.splitlines():
    s_x, s_y, b_x, b_y = map(int, re.findall('(-?\d+)', line))
    sensor_and_beacons.append(((s_x, s_y), (b_x, b_y)))


impossible_range = get_impossible_ranges(y)[0]
beacon_xs_in_range = {
    beacon[0]
    for _s, beacon in sensor_and_beacons
    if impossible_range[0] <= beacon[0] <= impossible_range[1] and beacon[1] == y
}
print(impossible_range[1] - impossible_range[0] + 1 - len(beacon_xs_in_range))

for y in range(max_y + 1):
    range_set = get_impossible_ranges(y)
    if len(range_set) > 1:
        print(4000000 * (range_set[0][1] + 1) + y)
        break
