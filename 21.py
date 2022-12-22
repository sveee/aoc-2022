import re
from dataclasses import dataclass
from typing import Optional

from utils import get_input

text = get_input(day=21, year=2022, test=False)


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
            return self.left.compute() // self.right.compute()

    def compute(self):
        if self.value is None:
            self.value = self._compute()
        return self.value


node_by_name = {}
for line in text.splitlines():
    name, right = line.split(':')

    if match := re.search(' ([a-z]+) ([\+\-\*\/]) ([a-z]+)', line):
        node = node_by_name.setdefault(name, Node())
        node.left = node_by_name.setdefault(match.group(1), Node())
        node.right = node_by_name.setdefault(match.group(3), Node())
        node.operation = match.group(2)

    elif match := re.search(' (\d+)', line):
        node = node_by_name.setdefault(name, Node())
        node.value = int(match.group(1))
    else:
        raise ValueError(f'Unknown pattern {line}')

print(node_by_name['root'].compute())
