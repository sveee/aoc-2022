from utils import get_input

text = get_input(day=6, year=2022)


def find_marker(n_chars):
    for marker in range(n_chars, len(text)):
        s = text[marker - n_chars : marker]
        if len(set(s)) == len(s):
            return marker


print(find_marker(4))
print(find_marker(14))
