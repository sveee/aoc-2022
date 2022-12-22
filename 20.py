from dataclasses import dataclass
from typing import Optional

from utils import get_input

text = get_input(day=20, year=2022, test=False)
sequence = list(map(int, text.splitlines()))


@dataclass
class Node:
    index: int
    value: int
    left: Optional['Node'] = None
    right: Optional['Node'] = None


def remove(node):
    left = node.left
    right = node.right
    left.right = node.right
    right.left = node.left
    return left


def add(left, node):
    right = left.right
    node.left = left
    node.right = right
    left.right = node
    right.left = node


def move(node, steps, length):
    if steps > 0:
        steps %= length
        while steps:
            node = node.right
            steps -= 1
    else:
        steps = -steps
        steps %= length
        while steps:
            node = node.left
            steps -= 1
    return node


def find(value, node):

    if node.value == value:
        return node

    current = node.right
    while current.value != value:
        current = current.right
    if current != node:
        return current


def print_list(start):
    sequence = []
    current = start.right
    sequence.append(start.value)
    while current != start:
        sequence.append(current.value)
        current = current.right
    print(sequence)


def find_groove_sum(n_rounds, key):
    start = end = None
    ordered_nodes = []
    n = len(sequence)
    for index, value in enumerate(sequence):
        node = Node(index, value * key)
        if start is None:
            start = node
            start.left = start.right = start
        else:
            add(end, node)
        end = node
        ordered_nodes.append(node)

    for _round in range(n_rounds):
        for node in ordered_nodes:
            left = remove(node)
            left = move(left, node.value, n - 1)
            add(left, node)

    zero_node = find(0, start)
    return (
        move(zero_node, 1000, n).value
        + move(zero_node, 2000, n).value
        + move(zero_node, 3000, n).value
    )


print(find_groove_sum(1, 1))
print(find_groove_sum(10, 811589153))
