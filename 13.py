from functools import cmp_to_key

from utils import get_input

text = get_input(day=13, year=2022)


def compare_packets(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return -1 if p1 < p2 else 0 if p1 == p2 else 1
    elif isinstance(p1, list) and isinstance(p2, list):
        n = min(len(p1), len(p2))
        for i in range(n):
            r = compare_packets(p1[i], p2[i])
            if r != 0:
                return r
        return -1 if len(p1) < len(p2) else 0 if len(p1) == len(p2) else 1
    elif isinstance(p1, list) and isinstance(p2, int):
        return compare_packets(p1, [p2])
    elif isinstance(p1, int) and isinstance(p2, list):
        return compare_packets([p1], p2)
    else:
        raise RuntimeError(f'Unknown types: {p1}, {p2}')


index_sum = 0
dividers = [[[2]], [[6]]]
packets = dividers
for index, pair_of_packets in enumerate(text.split('\n\n')):
    packet1, packet2 = pair_of_packets.split()
    packet1, packet2 = eval(packet1), eval(packet2)
    packets.append(packet1)
    packets.append(packet2)
    if compare_packets(packet1, packet2) == -1:
        index_sum += index + 1
packets = sorted(packets, key=cmp_to_key(compare_packets))
print(index_sum)
print((packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1))
