from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
import requests


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

result = []
confer = []

def parser_szgmu_pages(un_id, url, date_):

    def date_str_prep(str_):
        names = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ',
                 ' july ', ' august ', ' september ', ' october ', ' november ', ' december ']
        nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        months = dict(zip(nums, names))
        for k, v in months.items():
            if f'-{k}-' in str_:
                str_ = str_.replace(f'-{k}-', f'{v}')
        return str_


    year = date_.year
    month = date_.month - 1
    try:
        session = requests.session()
        while year <= date.today().year + 1:
            while True:
                if month == 12:
                    month = 0
                    break
                else:
                    month += 1
                params = {
                    'eventer_year': f'{year}',
                    'eventer_month': f'{month}',
                    'tip': '1',
                }
                try:
                    resp = session.get(url=url, headers=headers, params=params, timeout=20)
                    if resp.status_code == 404:
                        print(f'{resp.status_code} - Нет такой страницы {url}')
                        return
                    print(f'{resp.status_code} - Обработка {month} месяц {year} года')
                    soup = BeautifulSoup(resp.text, 'lxml')
                    if soup.find('div', class_='event-details-items-wrapper'):
                        main_containers = soup.find_all('div', class_='event-details-items-wrapper')
                    else:
                        print(f'Нет событий в {month} месяце {year} года, ищем дальше.')
                        continue

                    un_name = 'Северо-Западный государственный медицинский университет имени И.И. Мечникова'
                    for conteiner in main_containers:
                        main_container = conteiner.find_all('div', class_='event-item-content')
                        for conf in main_container:
                            # print(conf)
                            conf_name = normalise_str(conf.find('h1', class_='event-heading').text)
                            if 'конфер' in conf_name:
                                conf_s_desc = conf_name
                                local = False if 'международн' in conf_name.lower() or 'международн' in conf_s_desc.lower() else True
                                conf_id = f"{un_id}_{''.join(conf_name.split())}"
                                hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                                conf_card_href = ''

                                conf_date_begin = str(find_date_in_string(date_str_prep(normalise_str(conf.find(
                                    class_='meta-item start-date-label').text)))[0].date()) if \
                                    find_date_in_string(normalise_str(conf.find(
                                        class_='meta-item start-date-label').text)) else ''
                                conf_date_end = str(find_date_in_string(date_str_prep(normalise_str(conf.find(
                                    class_='meta-item end-date-label').text)))[0].date()) if \
                                    find_date_in_string(normalise_str(conf.find(
                                        class_='meta-item end-date-label').text)) else ''

                                reg_date_begin = ''
                                reg_date_end = ''
                                reg_href = ''
                                conf_desc = ''
                                org_name = ''
                                themes = ''
                                conf_href = ''
                                contacts = ''
                                conf_address = ''
                                online = False
                                offline = True
                                rinc = False

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
                                     'themes': themes.strip(),
                                     'online': online,
                                     'conf_href': conf_href,
                                     'offline': offline,
                                     'conf_address': conf_address,
                                     'contacts': contacts.strip(),
                                     'rinc': rinc,
                                     }
                                )
                except Exception as e:
                    print(f'Ошибка загрузки данных для {month} месяца {year} года.')

            year += 1

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')
def parser_szgmu(un_id, url, date_):
    try:
        parser_szgmu_pages(un_id, url, date_)
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_szgmu('szgmu', 'https://szgmu.ru/modules/ev/index.php',
                       datetime.strptime('2023.01.01', '%Y.%m.%d')))
