"""Common parsing logic shared by most parsers.

Intended for use with any given website, with the most abstract rules so that they apply anywhere.
More accurate, site-specific rules can be added to spiders on top of these functions.
"""
from itertools import zip_longest
import re
from collections.abc import Generator

from scrapy import Selector
from scrapy.loader import ItemLoader
# from scrapy.linkextractors import IGNORED_EXTENSIONS TODO
from w3lib.html import remove_tags, remove_tags_with_content
import pdfplumber
import logging
from io import BytesIO

from .utils import find_date_in_string, parse_vague_dates
from .items import ConferenceItem

# pdfplumber logs are extremely verbose
logging.getLogger("pdfminer").setLevel(logging.WARNING)


def default_parser_xpath(selector: Selector | str, new_item: ItemLoader) -> ItemLoader:
    """Main starting point for generic data parsing & collection.
    Appends every supplied line of text to the description field.

    Args:
        selector: A selector item with text and tags, as it comes from the response.
            Can also accept plain text, but links won't be parsed.
        new_item: ItemLoader object to append discovered data to.

    Returns:
        Populated ItemLoader object.
    """
    if isinstance(selector, str):
        line = selector
        link = None
    else:
        line = selector.get()
        link = selector.xpath(".//a/@href").get()

    # remove inline <script>
    clean_line = remove_tags(remove_tags_with_content(line, ('script',)))
    lowercase = clean_line.casefold()

    if ('заяв' in lowercase
            or 'принимаютс' in lowercase
            or 'участия' in lowercase
            or 'регистр' in lowercase):
        if dates := find_date_in_string(lowercase):
            if ('до' in lowercase or 'оконч' in lowercase or 'срок' in lowercase) and len(dates) == 1:
                new_item.add_value('reg_date_end', dates[0])
            else:
                new_item.add_value('reg_date_begin', dates[0])
                new_item.add_value('reg_date_end', dates[1] if 1 < len(dates) else None)

        if (link and '.pdf' not in link and
                '.doc' not in link and
                '.xls' not in link and
                'mailto' not in link):
            new_item.add_value('reg_href', link)

    new_item.add_value('description', clean_line)

    if ('тел.' in lowercase
            or 'контакт' in lowercase
            or 'mail' in lowercase
            or 'почт' in lowercase):
        new_item.add_value('contacts', clean_line)

    if emails := re.search(r'\S+@\S+\.\S+', lowercase):
        new_item.add_value('contacts', emails.group(0))

    if isinstance(new_item.item, ConferenceItem):
        return parse_conf(clean_line, new_item, lowercase, link)
    return new_item


def parse_conf(line: str,
               new_item: ItemLoader,
               lowercase: str = None,
               link: str = None) -> ItemLoader:
    """Parse conference-specific fields and populate the supplied ItemLoader object with the results.

    Args:
        line: Text to parse, stripped from tags, normalization is not required (handled by the loader).
        lowercase: Same text, casefolded for comparisons.
        new_item: ItemLoader object to append discovered data to.
        link: URL, if any, contained it the parsed block.

    Returns:
        Populated ItemLoader object.
    """
    if lowercase is None:
        lowercase = line.casefold()

    if ('онлайн' in lowercase
            or 'трансляц' in lowercase
            or 'подключит' in lowercase
            or 'гибридн' in lowercase
            or 'дистанц' in lowercase
            or 'ссылка' in lowercase):
        new_item.add_value('online', True)
        if link:
            new_item.add_value('conf_href', link)

    if 'ринц' in lowercase:
        new_item.add_value('rinc', True)
    if 'scopus' in lowercase:
        new_item.add_value('scopus', True)
    if 'ВАК' in line:
        new_item.add_value('vak', True)
    if 'wos' in lowercase or 'web of science' in lowercase:
        new_item.add_value('wos', True)

    if ('состоится' in lowercase
            or 'состоятся' in lowercase
            or 'открытие' in lowercase
            or 'проведен' in lowercase
            or 'дата' in lowercase
            or 'пройд' in lowercase
            or 'проход' in lowercase
            or 'провод' in lowercase):
        new_item = get_dates(lowercase, new_item)

    if ('место' in lowercase
            or 'адрес' in lowercase
            or 'город' in lowercase
            or 'гибридн' in lowercase
            or 'очно' in lowercase):
        new_item.add_value('conf_address', line)
        new_item.add_value('offline', True)

    return new_item


def get_dates(string: str, new_item: ItemLoader, is_vague: bool = False) -> ItemLoader:
    """Search a string for dates, convert them to datetime format,
    and append to the supplied ItemLoader object.
    See :class:`tests<conf_spiders.tests.test_utils.TestDateFinder>` for a list of supported date formats.
    For a more general solution, see :py:func:`conf_spiders.utils.find_date_in_string`.

    Args:
        string: A string that may or may not contain dates.
        new_item: An ItemLoader object to write dates to.
        is_vague: Use this option to handle uncertain dates, e.g. just month.
            Warning: use this only if the string is certain to contain a date,
            otherwise false positives and/or unforeseen errors may occur.

    Returns:
        ItemLoader object with dates appended (if found).
    """
    dates = find_date_in_string(string)
    if not dates and is_vague:
        dates = parse_vague_dates(string)
    new_item.add_value('conf_date_begin', dates[0] if dates else None)
    new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 and dates[1] != dates[0] else None)
    return new_item


def parse_pdf_table(file: bytes) -> Generator[list[str]]:
    """Parse tables in PDF format.
    Accuracy is reasonably high, but not 100% - some rows can be erroneously split by pdfplumber.

    Args:
        file: Bytes from response.body

    Returns:
        List of row contents, split by columns.
    """

    # Here be dragons
    # These settings are extremely finicky, do test every PDF parser if you change anything.
    settings = {"join_tolerance": 8,
                "snap_tolerance": 8,
                "intersection_tolerance": 0.5,
                }

    pdf = pdfplumber.open(BytesIO(file))
    end_of_page = []
    for page in pdf.pages:
        rows = page.extract_table(table_settings=settings)
        page_len = len(rows) - 1
        for i, row in enumerate(rows):
            row = ['' if j is None else j for j in row]
            if end_of_page:
                if row[0]:
                    yield end_of_page
                else:
                    row = list(map(' '.join, zip_longest(end_of_page, row, fillvalue='')))
                end_of_page = []
            if i == page_len:
                end_of_page = row
                continue
            yield row
