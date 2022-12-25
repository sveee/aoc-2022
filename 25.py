from utils import get_input

text = get_input(day=25, year=2022)


digit_map = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
reverse_digit_map = {value: key for key, value in digit_map.items()}


def snafu_to_decimal(s):
    result = 0
    five = 1
    for digit in s[::-1]:
        result += five * digit_map[digit]
        five *= 5
    return result


def decimal_to_snafu(n):
    digits = []
    carry = 0
    while n != 0:
        r = n % 5 + carry
        if r > 2:
            carry = 1
            r -= 5
        else:
            carry = 0
        digits.append(reverse_digit_map[r])
        n //= 5
    if carry:
        digits.append(reverse_digit_map[carry])

    return ''.join(digits[::-1])


print(decimal_to_snafu(sum(snafu_to_decimal(line) for line in text.splitlines())))
