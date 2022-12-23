import re
from dataclasses import dataclass
from typing import Optional

from utils import get_input

text = get_input(day=21, year=2022)
lines = text.splitlines()


@dataclass
class Node:
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    value: Optional[int] = None
    operation: Optional[str] = None

    def _compute(self):
        assert (
            self.operation is not None
            and self.left is not None
            and self.right is not None
        )
        if self.operation == '+':
            return self.left.compute() + self.right.compute()
        elif self.operation == '-':
            return self.left.compute() - self.right.compute()
        elif self.operation == '*':
            return self.left.compute() * self.right.compute()
        elif self.operation == '/':
            return self.left.compute() / self.right.compute()

    def compute(self):
        if self.value is None:
            self.value = self._compute()
        return self.value


def construct_compute_graph(humn=None):
    node_by_name = {}
    for line in lines:
        name, right = line.split(':')

        if match := re.search(' ([a-z]+) ([\+\-\*\/]) ([a-z]+)', right):
            node = node_by_name.setdefault(name, Node())
            node.left = node_by_name.setdefault(match.group(1), Node())
            node.right = node_by_name.setdefault(match.group(3), Node())
            node.operation = match.group(2)

        elif match := re.search(' (\d+)', right):
            node = node_by_name.setdefault(name, Node())
            value = humn if humn is not None and name == 'humn' else int(match.group(1))
            node.value = value
        else:
            raise ValueError(f'Unknown pattern {right}')
    return node_by_name


def root_children_difference(humn):
    graph = construct_compute_graph(humn)
    root = graph['root']
    return root.left.compute() - root.right.compute()


def sign(v):
    return -1 if v < 0 else 0 if v == 0 else 1


def binary_search(left, right):
    right_sign = sign(root_children_difference(right))
    while left <= right:
        mid = (left + right) // 2
        value = root_children_difference(mid)
        if value == 0:
            return mid
        elif sign(value) == right_sign:
            right = mid - 1
        else:
            left = mid + 1


print(int(construct_compute_graph()['root'].compute()))
print(binary_search(1, 10**18))
