import re
from bs4 import Tag
from scrapy.loader import ItemLoader
from .utils import find_date_in_string


def default_parser_bs(line: Tag, new_item: ItemLoader) -> ItemLoader:
    lowercase = line.text.lower()

    new_item.add_value('conf_desc', line.get_text(separator=" "))
    if 'ринц' in lowercase:
        new_item.add_value('rinc', True)
    if 'scopus' in lowercase:
        new_item.add_value('scopus', True)
    if 'ВАК' in line.text:
        new_item.add_value('vak', True)
    if 'wos' in lowercase:
        new_item.add_value('wos', True)

    if ('состоится' in lowercase
            or 'открытие' in lowercase
            or 'проведен' in lowercase
            or 'дата' in lowercase
            or 'пройд' in lowercase
            or 'проход' in lowercase
            or 'провод' in lowercase):
        if dates := find_date_in_string(lowercase):
            new_item.add_value('conf_date_begin', dates[0])
            new_item.add_value('conf_date_end', dates[1] if len(dates) > 1 else dates[0])

    if ('заявк' in lowercase
            or 'принимаютс' in lowercase
            or 'участия' in lowercase
            or 'регистр' in lowercase):
        if dates := find_date_in_string(lowercase):
            new_item.add_value('reg_date_begin', dates[0])
            new_item.add_value('reg_date_end', dates[1] if 1 < len(dates) else None)
        try:
            new_item.add_value(
                'reg_href', line.find('a').get('href')
                if line.find('a') and (
                        'http:' in line.find('a').get('href') or 'https:' in line.find('a').get('href')) and (
                           '.pdf' not in line.find('a').get('href') or
                           '.doc' not in line.find('a').get('href') or
                           '.xls' not in line.find('a').get('href')) else None)
        except TypeError:
            pass

    if 'организатор' in lowercase:
        new_item.add_value('org_name', line.get_text(separator=" "))

    if ('онлайн' in lowercase
            or 'трансляц' in lowercase
            or 'гибридн' in lowercase
            or 'дистанц' in lowercase
            or 'ссылка' in lowercase):
        new_item.add_value('conf_href', line.find('a').get('href') if line.find('a') else None)
        new_item.add_value('online', True)

    if ('место' in lowercase
            or 'адрес' in lowercase
            or 'город' in lowercase
            or 'очно' in lowercase):
        new_item.add_value('conf_address', line.text)
        new_item.add_value('offline', True)

    if ('тел.' in lowercase
            or 'контакт' in lowercase
            or 'mail' in lowercase
            or 'почт' in lowercase):
        new_item.add_value('contacts', line.text)

    if emails := re.search(r'\S+@\S+\.\S+', lowercase):
        new_item.add_value('contacts', emails.group(0))

    return new_item
