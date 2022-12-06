from dataclasses import dataclass

from utils import get_input

text = get_input(day=4, year=2022)


@dataclass
class Selection:
    start: int
    end: int

    def from_str(s: str) -> 'Selection':
        return Selection(*map(int, s.split('-')))


def is_contained(s1, s2):
    return (
        s1.start <= s2.start
        and s2.end <= s1.end
        or s2.start <= s1.start
        and s1.end <= s2.end
    )


def do_overlap(s1, s2):
    return not (s1.end < s2.start or s2.end < s1.start)


total1 = 0
total2 = 0
overlap = 0
for line in text.splitlines():
    first, second = line.split(',')
    s1 = Selection.from_str(first)
    s2 = Selection.from_str(second)
    total1 += is_contained(s1, s2)
    total2 += do_overlap(s1, s2)

print(total1)
print(total2)
