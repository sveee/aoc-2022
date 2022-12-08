from dataclasses import dataclass
from typing import List, Optional

from utils import get_input

text = get_input(day=7, year=2022)


@dataclass
class Folder:
    file_size: int
    children: List['Folder']
    parent: Optional['Folder']
    folder_size: int = 0


lines = text.splitlines()


def construct_tree(index, node):
    if index >= len(lines):
        return

    line = lines[index]
    if line.startswith('$ cd ..'):
        construct_tree(index + 1, node.parent)
    elif line.startswith('$ cd'):
        child = Folder(0, [], node)
        node.children.append(child)
        construct_tree(index + 1, child)
    elif line.startswith('$ ls'):
        index += 1
        while index < len(lines) and not lines[index].startswith('$'):
            size, _ = lines[index].split()
            if size != 'dir':
                node.file_size += int(size)
            index += 1
        construct_tree(index, node)


def calculate_folder_size(node):
    for child in node.children:
        calculate_folder_size(child)
    node.folder_size = (
        sum(child.folder_size for child in node.children) + node.file_size
    )


def get_folder_sizes(node):
    return [node.folder_size] + [
        folder_size
        for child in node.children
        for folder_size in get_folder_sizes(child)
    ]


root = Folder(0, [], None)
construct_tree(1, root)
calculate_folder_size(root)
folder_sizes = get_folder_sizes(root)
print(sum(folder_size for folder_size in folder_sizes if folder_size <= 100000))
print(
    min(
        folder_size
        for folder_size in folder_sizes
        if root.folder_size - folder_size <= 40000000
    )
)
