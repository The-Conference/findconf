import re
import datetime
from dateparser import parse


def normalize_string(string: str) -> str:
    """Normalizes spaces and removes junk."""
    try:
        # dash, hyphen, minus, etc.
        string = re.sub(r'[\u002D\u058A\u05BE\u1400\u1806'
                        r'\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40'
                        r'\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D–-]', '-', string)
    except TypeError as e:
        e.add_note("Attempted to normalize a non-string object. This most likely means "
                   "that a text field didn't get parsed properly. Is your selector wrong?")
        raise
    string = string.replace('&nbsp;', ' ').replace('\xa0', ' ') \
        .replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace('\u200b', '')
    return ' '.join(string.split()).strip()


def find_date_in_string(string: str) -> list[datetime.date]:
    """This function can be used for processing dates, though
    :func:`~conf_spiders.parsing.get_dates` should be preferred wherever possible.
    See tests for supported formats.
    Since the input is natural language, edge cases may not be handled properly.

    Args:
        string (str): Any string. It is, however, advisable to remove unnecessary data to increase detection rate.

    Returns:
        A list of 0, 1 or 2 date objects.
    """
    string = normalize_string(string)
    string = re.sub(r'[пд]о', '-', string)
    pattern = re.compile(
        r'(?i)(\d+(?:\s?-\s?\d+)?)\s?'
        r'(?:(январ[ьея]|феврал[ьея]|март[еа]?'
        r'|апрел[ьея]|ма[йея]|ию[нл][яье]'
        r'|август[еа]?|(?:сент|окт|но|дек)[ая]бр[яье])'
        r'|[-\\/.\s](\d\d?)[-\\/.\s])'  # I know, I know. Feel free to improve.
        r'\s?(\d+)?'
    )
    year = None
    dates = []
    for date in re.finditer(pattern, string):
        day, month_name, month_number, year = date.groups()
        if month_number and not 1 <= int(month_number) <= 12:
            break
        month = month_name or month_number
        if '-' in day:
            day1, day2 = day.split('-')
            # Assuming that the second part of a double date always has a month and a year
            dates.extend(({'day': day1, 'month': month, 'year': year},
                          {'day': day2, 'month': month, 'year': year}))
        else:
            dates.append({'day': day, 'month': month, 'year': year})

    for d in dates:
        if not d.get('year'):
            d['year'] = year or str(datetime.datetime.now().year)
    result = [parse(' '.join(_date.values()),
                    settings={'DEFAULT_LANGUAGES': ['ru'],
                              'DATE_ORDER': 'DMY'}
                    ) for _date in dates]
    return [i.date() for i in result if i is not None]


def parse_vague_dates(string: str) -> list[datetime.date]:
    """Parse dates that consist only of a month or month + year, though
    :func:`~conf_spiders.parsing.get_dates` should be preferred wherever possible.
    Will likely generate inaccurate results if input contains other data.

    Args:
        string (str): A string containing dates. See tests for supported formats.

    Returns:
        A list of 0, 1 or 2 date objects.
    """
    string = normalize_string(string)
    pattern = re.compile(
        r'(?i)январь|февраль|март|апрель|май|июнь|июль|август|(?:сент|окт|но|дек)[ая]брь'
        r'|\d{4}?'
    )
    matches = re.findall(pattern, string)
    month2 = year = ''
    last = matches.pop()
    try:
        year = int(last)
    except ValueError:
        month2 = last

    if year and len(matches) == 2:
        month1, month2 = matches
    elif len(matches) == 1:
        month1 = matches
    else:
        month1 = month2

    formatted = (f'01 {month1} {year}', f'{month2 or month1} {year}')
    return [parse(part, settings={'DEFAULT_LANGUAGES': ['ru'],
                                  'DATE_ORDER': 'DMY',
                                  'PREFER_DAY_OF_MONTH': 'last'}).date() for part in formatted]
