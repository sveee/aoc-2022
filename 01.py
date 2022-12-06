from utils import get_input

text = get_input(day=1, year=2022)
calories = list(sum(map(int, group.split())) for group in text.split('\n\n'))
print(max(calories))
print(sum(sorted(calories)[-3:]))
