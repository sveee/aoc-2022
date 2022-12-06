from utils import get_input

text = get_input(day=2, year=2022)

choices = ['rock', 'paper', 'scissors']
outcomes = ['lost', 'draw', 'win']
choice_score = dict(zip(choices, [1, 2, 3]))
outcome_score = dict(zip(outcomes, [0, 3, 6]))
what_beats = dict(zip(choices, choices[1:] + choices[:1]))
first_map = dict(zip(['A', 'B', 'C'], choices))
second_map1 = dict(zip(['X', 'Y', 'Z'], choices))
second_map2 = dict(zip(['X', 'Y', 'Z'], outcomes))


def match_outcome(c1, c2):
    return 'draw' if c1 == c2 else 'win' if what_beats[c2] == c1 else 'lost'


score1 = 0
score2 = 0
for line in text.splitlines():
    first, second = line.split()
    you, me = first_map[first], second_map1[second]
    score1 += choice_score[me] + outcome_score[match_outcome(me, you)]
    me = next(
        choice
        for choice in choices
        if match_outcome(choice, you) == second_map2[second]
    )
    score2 += choice_score[me] + outcome_score[second_map2[second]]
print(score1)
print(score2)
