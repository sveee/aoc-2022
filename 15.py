import re

from utils import get_input


def get_impossible_range(sensor, beacon, y):
    manhattan = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    range_x, range_y = (
        sensor[0] - manhattan + abs(sensor[1] - y),
        sensor[0] + manhattan - abs(sensor[1] - y),
    )
    if range_y >= range_x:
        return range_x, range_y


def do_intersect(left, right):
    return not (left[1] + 1 < right[0] or right[1] + 1 < left[0])


def get_impossible_ranges(y):
    return union(
        [
            impossible_range
            for sensor, beacon in sensor_and_beacons
            if (impossible_range := get_impossible_range(sensor, beacon, y))
        ]
    )


def union(range_set):
    range_set = sorted(range_set)
    left = range_set[0]
    result = []
    for right in range_set[1:]:
        if do_intersect(left, right):
            left = min(left[0], right[0]), max(left[1], right[1])
        else:
            result.append(left)
            left = right
    result.append(left)
    return result


text = get_input(day=15, year=2022)
sensor_and_beacons = []
for line in text.splitlines():
    sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall('(-?\d+)', line))
    sensor_and_beacons.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))

# part 1
y = 2000000
impossible_range = get_impossible_ranges(y)[0]
beacon_xs_in_range = {
    beacon[0]
    for _sensor, beacon in sensor_and_beacons
    if impossible_range[0] <= beacon[0] <= impossible_range[1] and beacon[1] == y
}
print(impossible_range[1] - impossible_range[0] + 1 - len(beacon_xs_in_range))

# part 2
max_y = 4000000
for y in range(max_y + 1):
    range_set = get_impossible_ranges(y)
    if len(range_set) > 1:
        print(4000000 * (range_set[0][1] + 1) + y)
        break
