import re
import datetime
from dateparser import parse


def normalise_str(string):
    string = ' '.join(string.split())
    return string.strip().replace('&nbsp;', ' ').replace('\xa0', ' ').replace('\r', ''). \
        replace('\n', '').replace('\t', '')


def find_date_in_string(string: str) -> list[datetime.date]:
    string = normalise_str(string)
    string = re.sub(r'\s?([пд]о|–|-)\s?', '-', string)
    pattern = re.compile(
        r'(?i)(\d+(?:-?\d+)?)\s?'
        r'(январ[ьея]|феврал[ьея]|март[еа]?'
        r'|апрел[ьея]|ма[йея]|ию[нл][яье]'
        r'|август[еа]?|(?:сент|окт|но|дек)[ая]бр[яье]'
        r'|\W\d\d\W)'
        r'\s?(\d+)?'
    )
    dates = []
    for date in re.finditer(pattern, string):
        date_parts = date.groups()
        if date_parts[0] and '-' in date_parts[0]:
            remainder = ' '.join(filter(None, date_parts[1:]))
            dates.extend([f'{i} {remainder}' for i in date_parts[0].split('-')])
        else:
            dates.append(date.group())
    result = [parse(date, settings={'DEFAULT_LANGUAGES': ['ru'],
                                    'DATE_ORDER': 'DMY'}
                    ) for date in dates]
    return [i.date() for i in result if i is not None]


def parse_vague_dates(string: str) -> list[datetime.date]:
    string = re.sub(r'[\u002D\u058A\u05BE\u1400\u1806'
                    r'\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40'
                    r'\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D]', '-', string)
    string = normalise_str(string)

    pattern = re.compile(
        r'(?i)январь|февраль|март|апрель|май|июнь|июль|август?|(?:сент|окт|но|дек)[ая]брь'
        r'|\d{4}?'
    )
    matches = re.findall(pattern, string)
    month1 = month2 = year = ''
    last = matches.pop()
    try:
        year = int(last)
    except ValueError:
        month2 = last

    if year and len(matches) == 2:
        month1, month2 = matches
    elif len(matches) == 1:
        month1 = matches
    elif not matches:
        month1 = month2

    formatted = (f'01 {month1} {year}', f'{month2 or month1} {year}')
    return [parse(part, settings={'DEFAULT_LANGUAGES': ['ru'],
                                  'DATE_ORDER': 'DMY',
                                  'PREFER_DAY_OF_MONTH': 'last'}).date() for part in formatted]
