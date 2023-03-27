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

def make_parse_mpei(un_id, url, filter_date):
    def date_str_prep(str_):
        words = str_.split()
        for n, word in enumerate(words):
            if '-' in word:
                words.insert(n, words[-2])
                words.insert(n + 1, words[-1])
                break
        str_ = ' '.join(words)
        return str_

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
            main_container = soup.find('div', class_='page-events')
            # print(main_container)
            year = 0

            if main_container.find('h2'):
                year = int(normalise_str(main_container.find('h2').text.lower().split()[0]))
                if year < filter_date.year:
                    print(f'Не найдено данных за {filter_date.year()} год и новее')
                    return

            for conf in main_container.find_all('div', class_='event-card'):

                dates_ = normalise_str(conf.find('div', class_='event-blue-block').find('div', class_='event-date').text)
                conf_name = normalise_str(conf.find('div', class_='event-blue-block').text)
                conf_name = conf_name.replace(dates_, '')
                dates_ = date_str_prep(f"{dates_} {year}")

                if 'конфер' in conf_name.lower():
                    # print(conf_name)
                    # print(dates_)
                    un_name = 'Национальный исследовательский университет «МЭИ»'
                    local = False if 'международн' in conf_name.lower() else True

                    dates = find_date_in_string(dates_)
                    conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
                    conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''
                    # print(dates)
                    # print(conf_date_begin, conf_date_end)
                    # print('-----------------------')

                    conf_id = f"{un_id}_{''.join(conf_name.split())}_{conf_date_begin}_{conf_date_end}"
                    hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                    conf_card_href = ''

                    info = conf.find_all('div', class_='event-info')
                    conf_address = normalise_str(info[0].text) if len(info) > 0 else ''
                    contacts = ''
                    for _ in range(1, len(info)):
                        contacts = f"{contacts} {normalise_str(info[_].text)}"

                    conf_s_desc = conf_name
                    conf_desc = conf_name

                    reg_date_begin = ''
                    reg_date_end = ''
                    reg_href = ''
                    org_name = ''

                    themes = ''
                    online = False
                    conf_href = ''
                    offline = True
                    themes = ''
                    rinc = False

                    if 'онлайн' in conf_name or 'дистанцион' in  conf_name or 'интернет' in  conf_name:
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

def parser_mpei(un_id, urls, date_):
    try:
        for url in urls:
            make_parse_mpei(un_id, url, date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_mpei('mpei', ['https://mpei.ru/Science/ScientificEvents/Pages/default.aspx'], datetime.strptime('2023.01.01', '%Y.%m.%d')))
