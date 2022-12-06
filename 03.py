from utils import get_input

text = get_input(day=3, year=2022)


def score_common(common_items):
    return sum(
        ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27
        for item in common_items
    )


backpacks = text.splitlines()
total_priority1 = sum(
    score_common(
        set(backback[: len(backback) // 2]) & set(backback[len(backback) // 2 :])
    )
    for backback in backpacks
)
total_priority2 = sum(
    score_common(set(backpacks[i]) & set(backpacks[i + 1]) & set(backpacks[i + 2]))
    for i in range(0, len(backpacks), 3)
)
print(total_priority1)
print(total_priority2)
