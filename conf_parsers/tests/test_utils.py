from datetime import date, datetime
from unittest import TestCase
from conf_parsers.utils import find_date_in_string, parse_vague_dates, normalize_string


class TestDateFinder(TestCase):
    def test_datefinder_single_words(self):
        cases = [
            'c 02 января 2023 г',
            '02 Января 2023',
            '02 ЯНВАРЯ 2023 в 9:30',
            '2 ЯНВАРЬ 2023',
            'начало2января2023года',
        ]
        for case in cases:
            self.assertEqual([date(2023, 1, 2)], find_date_in_string(case))

    def test_datefinder_single_digits(self):
        cases = [
            'до 02 01 2023 г',
            '02.01.2023',
            '02/01/2023',
            '02\\01\\2023',
            '02-01-2023',
            '02.01.23',
            '02 1 2023',  # *sigh*
        ]
        for case in cases:
            self.assertEqual([date(2023, 1, 2)], find_date_in_string(case))

    def test_datefinder_double(self):
        cases = [
            'состоится 02-20 января 2023 г',
            '02-20.01.2023',
            '02-20 01 2023',
            '02-20/01/2023',
            '02-20\\01\\2023',
            '02-20-01-2023',
            'с 2 января 2023 до 20 января 2023',
            '2 января 2023 – 20 января 2023',
            'c 2 по 20 января 2023 г',
            'c2до20января2023г',
            '02   –  20    января    2023'
        ]
        for case in cases:
            self.assertEqual([date(2023, 1, 2), date(2023, 1, 20)], find_date_in_string(case))

    def test_datefinder_no_match(self):
        cases = [
            '70-летию',
            'тест – 2023',
            'до 35 лет',
            '2020-2021',
            '2023',
            'https://forms.yandex.ru/u/63c563285056901e70f9180d/'
        ]
        for case in cases:
            self.assertEqual([], find_date_in_string(case))

    def test_datefinder_no_year(self):
        current_year = datetime.now().year
        cases = [
            '26 апреля',
            '26 апреля в 10.00 в конференц –зале',  # OMG who does this
        ]
        for case in cases:
            self.assertEqual([date(current_year, 4, 26)], find_date_in_string(case))
        self.assertEqual([date(current_year, 5, 26), date(current_year, 5, 27)],
                         find_date_in_string('26-27 мая'))


class TestVagueDateParser(TestCase):
    def test_vague_date_only_month(self):
        current_year = datetime.now().year
        self.assertEqual([date(current_year, 7, 1), date(current_year, 7, 31)],
                         parse_vague_dates('июль'))

    def test_vague_date_month_range(self):
        current_year = datetime.now().year
        self.assertEqual([date(current_year, 7, 1), date(current_year, 8, 31)],
                         parse_vague_dates('июль - август'))

    def test_vague_date_month_year(self):
        self.assertEqual([date(2023, 7, 1), date(2023, 7, 31)],
                         parse_vague_dates('июль 2023'))

    def test_vague_date_month_year_range(self):
        self.assertEqual([date(2023, 7, 1), date(2023, 8, 31)],
                         parse_vague_dates('июль - август 2023'))


class TestStringNormalizer(TestCase):
    def test_normalize_string(self):
        cases = [
            ' test\n\t\t test\r\n ',
            'test\xa0&nbsp;test',
        ]
        for case in cases:
            self.assertEqual('test test', normalize_string(case))
