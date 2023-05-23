import re
import datetime
from dateparser import parse


def normalise_str(string):
    string = ' '.join(string.split())
    return string.strip().replace('&nbsp;', ' ').replace('\xa0', ' ').replace('\r', ''). \
        replace('\n', '').replace('\t', '')


def find_date_in_string(string: str) -> list[datetime.date | None]:
    string = normalise_str(string)
    string = re.sub(r'\s?[пд]о\s?|–', '-', string)
    pattern = re.compile(
        r'(?i)(?:\s+)?(\d+(?:-?\d+)?)\s?'
        r'(январ[ьея]|феврал[ьея]|март[еа]?'
        r'|апрел[ьея]|ма[йея]|ию[нл][яье]'
        r'|август[еа]?|(?:сент|окт|но|дек)[ая]бр[яье]'
        r'|\W\d\d\W)'
        r'\s?(\d+)?'
    )
    dates = []
    for date in re.finditer(pattern, string):
        date_parts = date.groups()
        if '-' in date_parts[0]:
            remainder = ' '.join(filter(None, date_parts[1:]))
            dates.extend([f'{i} {remainder}' for i in date_parts[0].split('-')])
        else:
            dates.append(date.group())
    return [parse(date, settings={'DEFAULT_LANGUAGES': ['ru'], 'DATE_ORDER': 'DMY'}
                  ).date() for date in dates]
