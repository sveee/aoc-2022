import os
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

SESSION = os.environ.get('SESSION')


def get_input(
    day: int, year: Optional[int], test: bool = False, test_index: int = 0
) -> str:
    if test:
        soup = BeautifulSoup(
            requests.get(f'https://adventofcode.com/{year}/day/{day}').text,
            features='html.parser',
        )
        input_text = soup.find_all('pre')[test_index].text
    else:
        if year is None:
            year = datetime.now().year
        input_text = requests.get(
            f'https://adventofcode.com/{year}/day/{day}/input',
            cookies=dict(session=SESSION),
        ).text
    if input_text.endswith('\n'):
        input_text = input_text[:-1]
    return input_text
