from utils import get_input

text = get_input(day=10, year=2022)
lines = text.splitlines()


def part1():
    x = 1
    xs = [0]
    for instruction in text.splitlines():
        xs.append(x)
        if instruction.startswith('addx'):
            xs.append(x)
            x += int(instruction.split()[1])
    return sum(cycle * xs[cycle] for cycle in range(20, len(xs), 40))


def part2():
    x = 1
    image = ''
    instructions = lines[::-1]
    stack = instructions.pop().split()
    for crt in range(240):
        crt %= 40
        if crt == 0 and image:
            image += '\n'
        image += '#' if abs(x - crt) <= 1 else '.'
        instruction = stack.pop(0)
        if instruction not in ['noop', 'addx']:
            x += int(instruction)
        if len(stack) == 0 and len(instructions) > 0:
            stack = instructions.pop().split()
    return image


print(part1())
print(part2())
