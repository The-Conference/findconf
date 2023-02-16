from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
import requests
import urllib3
from datetime import datetime


result = []

cookies = {
    'session-cookie': '1741ceae7b9dffd3b10c8a2ebeb261f55e5764f631050173957cfd2e8283925d6b6d8f9341f606789e04256b706df1c1',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'session-cookie=1741ceae7b9dffd3b10c8a2ebeb261f55e5764f631050173957cfd2e8283925d6b6d8f9341f606789e04256b706df1c1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def make_parse_ssmu(un_id, url, filter_date):
    try:
        session = requests.session()
        tasks = []
        try:
            urllib3.disable_warnings()
            resp = session.get(url=url, cookies=cookies, headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return

            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find('div', class_='content')
            cur_year = date.today().year

            try:
                year = main_container.find('p').text
                year = int(year[year.find('планируемые на ') + 15:].split()[0])
            except:
                raise Exception(f'Год материалов конференций не определен, принадлежность не установлена.')

            if year != cur_year:
                raise Exception(f'Не найден материал конференций текущего {cur_year} года.')

            print(f'{resp.status_code} Обрабатываем {year} год, {url}')
            conf_block = main_container.find_all('tr')

            for n, conf in enumerate(conf_block):
                if conf.find('td') == 'Дата проведения':
                    continue

                fields = conf.find_all('td')
                conf_name = normalise_str(fields[1].text)
                dates = find_date_in_string(f"{normalise_str(fields[0].text)} {year}")

                if 'конфер' in conf_name.lower():

                    un_name = 'СибГМУ'
                    local = False if 'международн' in conf_name.lower() else True

                    conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
                    conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

                    conf_id = f"{un_id}_{conf_date_begin}_{conf_date_end}"
                    hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                    conf_card_href = ''
                    conf_address = normalise_str(fields[2].text)

                    conf_s_desc = conf_name
                    conf_desc = conf_name

                    reg_date_begin = ''
                    reg_date_end = ''
                    reg_href = ''

                    forth_field = fields[3].find_all('p')
                    org_name = ' '.join([normalise_str(forth_field[i].text) for i in range(0, 2)])
                    contacts = ' '.join([normalise_str(forth_field[i].text) for i in range(2, len(forth_field))])

                    themes = ''
                    online = False
                    conf_href = ''
                    offline = False
                    themes = ''
                    rinc = False

                    if 'онлайн' in conf_address or 'гибридн' in conf_address:
                        online = True

                    if 'офлайн' in conf_address or 'гибридн' in conf_address:
                        offline = True

                    if (conf_date_begin != '' and datetime.strptime(conf_date_begin,
                                                                    '%Y-%m-%d') >= filter_date) or conf_date_begin == '':
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

def parser_ssmu(un_id, urls, date_):
    try:
        for url in urls:
            make_parse_ssmu(un_id, url, date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_ssmu('ssmu', ['https://ssmu.ru/ru/nauka/activity/'], datetime.strptime('2023.01.01', '%Y.%m.%d')))
