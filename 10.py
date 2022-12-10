from utils import get_input

text = get_input(day=10, year=2022, test=False, test_index=1)
lines = text.splitlines()


x = 1
xs = []
for instruction in text.splitlines():
    xs.append(x)
    if instruction.startswith('addx'):
        xs.append(x)
        x += int(instruction.split()[1])

image = ''
for crt in range(240):
    if crt % 40 == 0 and image:
        image += '\n'
    image += '#' if abs(xs[crt] - (crt % 40)) <= 1 else '.'

print(sum((cycle + 1) * xs[cycle] for cycle in range(19, len(xs), 40)))
print(image)
