import re

from utils import get_input

text = get_input(day=15, year=2022, test=False)
# print(text)


def get_cannot_be_present(s, b, y):
    m = abs(s[0] - b[0]) + abs(s[1] - b[1])
    l = [s[0] - m + abs(s[1] - y), s[0] + m - abs(s[1] - y)]
    return [(l_x, y) for l_x in range(l[0], l[1] + 1)]


y = 2000000
# y = 10
# print(len(text.splitlines()))
no_beacon_posisions = set()
beacons = set()
for line in text.splitlines():
    s_x, s_y, b_x, b_y = map(int, re.findall('(-?\d+)', line))
    # print(len(no_beacon_posisions))
    # print(s_x, s_y, b_x, b_y)
    beacons.add((b_x, b_y))
    no_beacon_posisions.update(get_cannot_be_present((s_x, s_y), (b_x, b_y), y))

print(len(no_beacon_posisions - beacons))
# print(get_cannot_be_present((8, 7), (2, 10), -3))
# print(get_cannot_be_present((8, 7), (2, 10), 8))
