import os
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

SESSION = os.environ.get('SESSION')


def get_input(day: int, year: Optional[int], test: bool = False) -> str:
    if test:
        soup = BeautifulSoup(
            requests.get(f'https://adventofcode.com/{year}/day/{day}').text,
            features='html.parser',
        )
        for pre in soup.find_all('pre'):
            if code := pre.find('code'):
                input_text = code.text
                break
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
