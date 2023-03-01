from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
import requests
import urllib3
from datetime import datetime


result = []

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

def make_parse_ggtu(un_id, url, filter_date):
    try:
        session = requests.session()
        try:
            urllib3.disable_warnings()
            resp = session.get(url=url, headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find('div', class_='art-article').find('tbody')
            # print(main_container)
            for line in main_container.find_all('tr'):
                if 'мероприятие' in line.find('td').text.lower():
                    continue
                if line.find_all('td')[0].text == line.find_all('td')[-1].text:
                    continue
                # print(line)
                if 'конфер' in line.find_all('td')[0].text.lower():
                    conf_name = normalise_str(line.find_all('td')[0].text)
                    dates = find_date_in_string(line.find_all('td')[-1].text)

                    if (len(dates) > 1 and dates[1].date() < filter_date.date()) or \
                            (len(dates) > 0 and dates[0].date() < filter_date.date()):
                        continue

                    un_name = 'Государственный гуманитарно-технологический университет'
                    local = False if 'международн' in conf_name.lower() else True

                    conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
                    conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

                    conf_id = f"{un_id}_{''.join(line.find_all('td')[0].text.split())}_{conf_date_begin}_{conf_date_end}"
                    hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                    conf_card_href = ''
                    conf_address = ''

                    conf_s_desc = conf_name
                    conf_desc = conf_name

                    reg_date_begin = ''
                    reg_date_end = ''
                    reg_href = ''

                    org_name = ''
                    contacts = ''

                    themes = ''
                    online = False
                    conf_href = ''
                    offline = True
                    themes = ''
                    rinc = False

                    if 'онлайн' in conf_address or 'дистанцион' in conf_address or 'интернет' in conf_address:
                        online = True

                    result.append(
                        {'conf_id': conf_id,
                         'hash': hash_,
                         'un_name': un_name,
                         'local': local,
                         'reg_date_begin': reg_date_begin,
                         'reg_date_end': reg_date_end,
                         'conf_date_begin': conf_date_begin,
                         'conf_date_end': conf_date_end,
                         'conf_card_href': conf_card_href,
                         'reg_href': reg_href,
                         'conf_name': conf_name,
                         'conf_s_desc': conf_s_desc,
                         'conf_desc': conf_desc,
                         'org_name': org_name,
                         'themes': themes,
                         'online': online,
                         'conf_href': conf_href,
                         'offline': offline,
                         'conf_address': conf_address,
                         'contacts': contacts.strip(),
                         'rinc': rinc,
                         }
                    )

        except Exception as e:
            raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')

def parser_ggtu(un_id, urls, date_):
    try:
        for url in urls:
            make_parse_ggtu(un_id, url, date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_ggtu('ggtu', ['https://www.ggtu.ru/index.php?option=com_content&view=article&id=9230&Itemid=810'],
                      datetime.strptime('2023.01.01', '%Y.%m.%d')))
